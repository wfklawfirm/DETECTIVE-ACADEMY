#!/usr/bin/env python3
"""Crawl Detective Academy and capture desktop/mobile/tablet screenshots with audit metadata.

Usage:
  pip install playwright
  python -m playwright install chromium
  python capture_all_pages.py --base https://detective-academy-wfklawfirms-projects.vercel.app

Optionally supply one path per line via --routes-file routes.txt, for routes that
are only discoverable from the application's source/data.

Only public same-origin GET pages are visited. No forms are submitted or mutated.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import time
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, urljoin, parse_qsl, urlencode

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

SEEDS = [
    "/", "/home", "/cases", "/academy", "/academy/educators", "/knowledge", 
    "/labs", "/glossary", "/methods", "/archetypes", "/books", "/heritage", 
    "/gallery", "/skills", "/sources", "/biases", "/reasoning", "/rulebook", 
    "/atlas", "/profile", "/academy/A1", "/labs/SAFE_LABS-01", 
    "/books/BK-741", "/knowledge/KO-FC-04-001", "/heritage/doyle-study-in-scarlet"
]
VIEWPORTS = {
    "desktop": {"width": 1440, "height": 900},
    "tablet": {"width": 768, "height": 1024},
    "mobile": {"width": 390, "height": 844},
    "small-mobile": {"width": 320, "height": 720},
}
SKIP_FILE = re.compile(r"\.(?:png|jpe?g|gif|webp|svg|ico|pdf|zip|mp4|mov|mp3|woff2?|ttf|css|js|map|json|xml|txt)$", re.I)
SKIP_PATH_PREFIXES = ("/_next/", "/assets/", "/api/", "/auth/", "/logout", "/signout", "/admin/")


def normalized_url(href: str, base: str) -> str | None:
    try:
        u = urlsplit(urljoin(base, href))
        origin = urlsplit(base)
        if u.scheme not in ("https", "http") or u.netloc.lower() != origin.netloc.lower():
            return None
        path = u.path or "/"
        if any(path.startswith(prefix) for prefix in SKIP_PATH_PREFIXES) or SKIP_FILE.search(path):
            return None
        if path != "/":
            path = path.rstrip("/")
        # Retain pagination only, to avoid duplicate URLs from arbitrary search/filter params.
        allowed_query = [(k, v) for k, v in parse_qsl(u.query, keep_blank_values=False) if k == "page"]
        return urlunsplit((origin.scheme, origin.netloc, path, urlencode(allowed_query), ""))
    except Exception:
        return None


def file_stem(url: str) -> str:
    u = urlsplit(url)
    label = (u.path.strip("/") or "root").replace("/", "__")
    label = re.sub(r"[^a-zA-Z0-9_-]", "-", label)[:105] or "route"
    return f"{label}-{hashlib.sha1(url.encode()).hexdigest()[:9]}"


def scan_dom(page):
    return page.evaluate("""() => {
      const de = document.documentElement;
      const root = document.querySelector('main') || document.body;
      const screenText = root?.innerText || '';
      const badTargets = [...document.querySelectorAll('button,a,input,select,textarea')]
        .filter(el => {
          const r = el.getBoundingClientRect();
          return r.width > 0 && r.height > 0 && (r.width < 32 || r.height < 32);
        }).length;
      const noNameButtons = [...document.querySelectorAll('button')]
        .filter(el => !((el.innerText || el.getAttribute('aria-label') || el.title || '').trim()))
        .length;
      const imgs = [...document.images];
      return {
        title: document.title, h1: [...document.querySelectorAll('h1')].map(x=>x.innerText.trim()),
        headings: [...document.querySelectorAll('h1,h2,h3')].length,
        links: document.querySelectorAll('a[href]').length,
        buttons: document.querySelectorAll('button').length,
        inputs: document.querySelectorAll('input,select,textarea').length,
        image_count: imgs.length,
        broken_images: imgs.filter(x => x.complete && x.naturalWidth === 0).length,
        content_chars: screenText.length,
        page_width: de.scrollWidth, page_height: Math.max(de.scrollHeight, document.body?.scrollHeight||0),
        viewport_width: innerWidth,
        horizontal_overflow: de.scrollWidth > innerWidth + 3,
        small_interactive_targets: badTargets,
        unnamed_buttons: noNameButtons,
        loading_visible: /جارٍ التحميل|جار التحميل|Loading[.][.][.]/i.test(screenText),
        internal_hrefs: [...new Set([...document.querySelectorAll('a[href]')].map(a=>a.href))]
      };
    }""")


def screenshot_page(page, folder: Path, prefix: str, max_full_height: int):
    height = page.evaluate("Math.max(document.documentElement.scrollHeight, document.body.scrollHeight)")
    page.evaluate("window.scrollTo(0,0)")
    page.wait_for_timeout(180)
    results = []
    if height <= max_full_height:
        target = folder / f"{prefix}-full.jpg"
        page.screenshot(path=str(target), full_page=True, type="jpeg", quality=78, animations="disabled", timeout=25000)
        results.append(str(target))
    else:
        # Long pages are intentionally captured in multiple viewport slices.
        # This also records excessive document length as a UX audit signal.
        scroll_max = max(0, height - page.viewport_size["height"])
        offsets = sorted(set([0, int(scroll_max * 0.25), int(scroll_max * 0.5), int(scroll_max * 0.75), scroll_max]))
        for i, offset in enumerate(offsets, 1):
            page.evaluate("y => window.scrollTo(0,y)", offset)
            page.wait_for_timeout(220)
            target = folder / f"{prefix}-segment-{i:02d}.jpg"
            page.screenshot(path=str(target), full_page=False, type="jpeg", quality=78, animations="disabled", timeout=25000)
            results.append(str(target))
    page.evaluate("window.scrollTo(0,0)")
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="https://detective-academy-wfklawfirms-projects.vercel.app")
    ap.add_argument("--output", default="visual_audit_output")
    ap.add_argument("--routes-file", default="")
    ap.add_argument("--max-pages", type=int, default=1200)
    ap.add_argument("--viewports", default="desktop,mobile", help="comma-separated: desktop,tablet,mobile,small-mobile")
    ap.add_argument("--full-height-limit", type=int, default=16000)
    ap.add_argument("--page-timeout", type=int, default=25000)
    ap.add_argument("--age", default="", help="pre-set the athar_age cookie (16-17 or 18+) to skip the age gate")
    ap.add_argument("--no-follow", action="store_true", help="do not enqueue links discovered on pages")
    ap.add_argument("--no-seeds", action="store_true", help="use only --routes-file")
    args = ap.parse_args()
    base = args.base.rstrip("/")
    out = Path(args.output).resolve(); out.mkdir(parents=True, exist_ok=True)
    widths = [x.strip() for x in args.viewports.split(",")]
    if not widths or any(x not in VIEWPORTS for x in widths):
        raise SystemExit(f"Invalid --viewports; choose from {', '.join(VIEWPORTS)}")
    route_candidates = [] if args.no_seeds else list(SEEDS)
    if args.routes_file:
        route_candidates += [line.strip() for line in Path(args.routes_file).read_text(encoding="utf-8").splitlines()
                             if line.strip() and not line.lstrip().startswith("#")]
    q = deque()
    queued = set()
    def add(url):
        normalized = normalized_url(url, base)
        if normalized and normalized not in queued:
            queued.add(normalized); q.append(normalized)
    for route in route_candidates:
        add(route)
    output = []
    begun = time.monotonic()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path=shutil.which("chromium") or shutil.which("google-chrome") or None)
        for idx in range(args.max_pages):
            if not q:
                break
            url = q.popleft()
            row = {"url": url, "screenshots": {}, "viewports": {}, "errors": [], "console_errors": [], "captured_at": datetime.now(timezone.utc).isoformat()}
            print(f"[{idx + 1}/{args.max_pages}] {url}", flush=True)
            for vp in widths:
                context = browser.new_context(viewport=VIEWPORTS[vp], device_scale_factor=1, locale="ar-LB", color_scheme="light")
                if args.age:
                    context.add_cookies([{"name": "athar_age", "value": args.age, "url": base}])
                page = context.new_page()
                page.on("pageerror", lambda error, r=row: r["console_errors"].append(str(error)[:300]))
                try:
                    response = page.goto(url, wait_until="domcontentloaded", timeout=args.page_timeout)
                    row[f"status_{vp}"] = response.status if response else None
                    try:
                        page.wait_for_load_state("networkidle", timeout=5000)
                    except PWTimeout:
                        pass
                    page.wait_for_timeout(1000)
                    info = scan_dom(page)
                    # Wait once longer if hydration is still showing its loading placeholder.
                    if info["loading_visible"]:
                        page.wait_for_timeout(5000)
                        info = scan_dom(page)
                    if vp == "desktop":
                        for href in info.pop("internal_hrefs"):
                            if not args.no_follow:
                                add(href)
                    else:
                        info.pop("internal_hrefs")
                    row["viewports"][vp] = info
                    folder = out / "screenshots" / vp
                    folder.mkdir(parents=True, exist_ok=True)
                    prefix = file_stem(url)
                    row["screenshots"][vp] = [str(Path(x).relative_to(out)) for x in
                        screenshot_page(page, folder, prefix, args.full_height_limit)]
                    if info["horizontal_overflow"]:
                        row["errors"].append(f"{vp}: horizontal overflow {info['page_width']}px > {info['viewport_width']}px")
                    if info["loading_visible"]:
                        row["errors"].append(f"{vp}: loading placeholder remains after extra wait")
                    if info["broken_images"]:
                        row["errors"].append(f"{vp}: {info['broken_images']} broken images")
                except Exception as error:
                    row["errors"].append(f"{vp}: {type(error).__name__}: {str(error)[:240]}")
                    try:
                        folder = out / "screenshots" / vp; folder.mkdir(parents=True, exist_ok=True)
                        error_shot = folder / f"{file_stem(url)}-error.jpg"
                        page.screenshot(path=str(error_shot), type="jpeg", quality=70, timeout=6000)
                        row["screenshots"][vp] = [str(error_shot.relative_to(out))]
                    except Exception:
                        pass
                finally:
                    context.close()
            output.append(row)
            (out / "audit-results.json").write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
        browser.close()
    with (out / "audit-summary.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["URL", "desktop status", "mobile status", "desktop chars", "desktop height", "mobile overflow", "missing button names desktop", "errors"])
        for r in output:
            d = r["viewports"].get("desktop", {}); m = r["viewports"].get("mobile", {})
            writer.writerow([r["url"], r.get("status_desktop"), r.get("status_mobile"), d.get("content_chars"), d.get("page_height"), m.get("horizontal_overflow"), d.get("unnamed_buttons"), " | ".join(r["errors"])])
    issue_count = sum(bool(r["errors"]) for r in output)
    md = ["# Detective Academy — Screenshot & Technical Audit", "", f"Captured: {datetime.now(timezone.utc).isoformat()}", f"Routes reviewed: {len(output)}", f"Routes with flagged problems: {issue_count}", f"Run time (seconds): {int(time.monotonic()-begun)}", "", "This is an AUTOMATED evidence inventory. Visual judgment and functional state testing must be performed manually or by Claude Code.", ""]
    for r in output:
        md.extend([f"## {r['url']}", "", f"- HTTP desktop/mobile: {r.get('status_desktop')} / {r.get('status_mobile')}", f"- Findings: {'; '.join(r['errors']) or 'No automatic flags (not proof of visual quality)'}"])
        for v, paths in r["screenshots"].items():
            md.append(f"- {v} screenshots: " + ", ".join(f"`{path}`" for path in paths))
        md.append("")
    (out / "SCREENSHOT_INDEX.md").write_text("\n".join(md), encoding="utf-8")
    print(f"\nFinished {len(output)} pages. {issue_count} flagged. Files in {out}")
    print("Next: inspect screenshots, review results, fix code, recapture before/after and run E2E tests.")

if __name__ == "__main__":
    main()
