import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { gunzipSync } from "node:zlib";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { Markdown, safeHref } from "@/components/research/Markdown";
import { LibraryAccessError, findEntry, firstJsonRecords, libraryAccess, listLibrary, parseCsvPage, readDoc, searchLibrary } from "@/engine/research";

const anon = { user: null };
const as = (role: string) => ({ user: { role } });
const root = process.cwd();
const manifest = JSON.parse(readFileSync(join(root, "content/research/manifest.json"), "utf8")) as { files: { path: string; pack: string; sha256: string; status: string; stored_as?: string; reason?: string; duplicate_of?: string; type: string; size: number; desc?: string; sensitive?: boolean }[]; stats: Record<string, number> };

describe("research library: admin-only guard", () => {
  it("only the admin role passes; anonymous must log in; every other role is forbidden", () => {
    expect(libraryAccess(anon)).toBe("login");
    for (const r of ["player", "editor", "reviewer"]) expect(libraryAccess(as(r))).toBe("forbidden");
    expect(libraryAccess(as("admin"))).toBe("ok");
  });
  it("every reader refuses anonymous and non-admin actors (a page that forgets the gate still cannot leak)", () => {
    const some = manifest.files.find((f) => f.status === "copied" && f.type === "md")!;
    for (const actor of [anon, as("player"), as("editor"), as("reviewer")]) {
      expect(() => listLibrary(actor)).toThrow(LibraryAccessError);
      expect(() => searchLibrary(actor, { q: "athar" })).toThrow(LibraryAccessError);
      expect(() => findEntry(actor, some.path.split("/"))).toThrow(LibraryAccessError);
      expect(() => readDoc(actor, some as never)).toThrow(LibraryAccessError);
    }
    const err = (() => { try { listLibrary(anon); } catch (e) { return e as LibraryAccessError; } })();
    expect(err?.access).toBe("login");
  });
  it("the admin can list, find and read a document; competitor intelligence is among the readable docs", () => {
    const lib = listLibrary(as("admin"));
    expect(lib.entries.length).toBe(manifest.files.length);
    const comp = manifest.files.find((f) => f.path.startsWith("09_COMPETITIVE_INTELLIGENCE/") && f.status === "copied" && f.type === "md")!;
    const e = findEntry(as("admin"), comp.path.split("/"))!;
    expect(e).toBeTruthy();
    expect(readDoc(as("admin"), e)!.length).toBeGreaterThan(100);
    expect(comp.sensitive).toBe(true);
  });
  it("paths resolve only through the manifest: traversal and unknown paths find nothing", () => {
    const a = as("admin");
    for (const p of [["..", "package.json"], ["01_SOURCE_CATALOG", "..", "..", "package.json"], [".", "x"], ["", "x"], ["a\\b"], ["x\0y"], ["nope", "nope.md"]]) expect(findEntry(a, p)).toBeNull();
  });
  it("the library pages are gated by LibraryGate and render no raw HTML", () => {
    for (const f of ["src/app/studio/library/page.tsx", "src/app/studio/library/[...path]/page.tsx"]) {
      const src = readFileSync(join(root, f), "utf8");
      expect(src).toContain("<LibraryGate");
      expect(src).not.toContain("dangerouslySetInnerHTML");
    }
    expect(readFileSync(join(root, "src/components/research/Markdown.tsx"), "utf8")).not.toContain("dangerouslySetInnerHTML");
    expect(readFileSync(join(root, "src/components/research/LibraryGate.tsx"), "utf8")).toContain("libraryAccess");
  });
});

describe("research manifest integrity", () => {
  it("covers every pack file with a status; skipped rows carry a reason; duplicates point at a listed row", () => {
    expect(manifest.files.length).toBeGreaterThanOrEqual(890);
    const all = new Set(manifest.files.map((f) => f.path));
    for (const f of manifest.files) {
      expect(["copied", "duplicate-of", "skipped"]).toContain(f.status);
      expect(f.sha256).toMatch(/^[0-9a-f]{64}$/);
      expect(f.path).not.toMatch(/(^|\/)\.\.(\/|$)|^\//);
      if (f.status === "skipped") expect(f.reason, f.path).toBeTruthy();
      if (f.status === "duplicate-of") expect(all.has(f.duplicate_of!), f.path).toBe(true);
    }
    expect(manifest.stats.copied! + manifest.stats["duplicate-of"]! + manifest.stats.skipped!).toBe(manifest.files.length);
  });
  it("never copies executables or databases, and every executable is listed with a reason", () => {
    for (const f of manifest.files) if (["py", "mjs", "sqlite", "pyc", "lp", "yarn", "ink", "html", "png", "zip"].includes(f.type)) {
      expect(f.status, f.path).not.toBe("copied");
      if (f.status === "skipped") expect(f.reason).toMatch(/not copied|superseded/);
    }
  });
  it("copied files exist and match their recorded sha256 (decompressing .gz)", () => {
    for (const f of manifest.files.filter((x) => x.status === "copied")) {
      const p = join(root, "content/research/docs", f.stored_as!);
      expect(existsSync(p), f.path).toBe(true);
      const buf = readFileSync(p);
      const raw = f.stored_as!.endsWith(".gz") ? gunzipSync(buf) : buf;
      expect(createHash("sha256").update(raw).digest("hex"), f.path).toBe(f.sha256);
      if (f.type === "md") expect(f.desc, f.path).toBeTruthy();
    }
  });
});

describe("safe markdown renderer", () => {
  const html = (s: string) => renderToStaticMarkup(createElement(Markdown, { source: s }));
  it("escapes raw HTML and never emits script or event handlers", () => {
    const out = html('# عنوان <script>alert(1)</script>\n\n<img src=x onerror=alert(1)> **bold** and `code <b>`');
    expect(out).not.toMatch(/<script|<img/i);
    expect(out).toContain("&lt;script&gt;");
    expect(out).toContain("<strong>bold</strong>");
  });
  it("only http(s) links become anchors; javascript:/data: stay plain text", () => {
    expect(safeHref("javascript:alert(1)")).toBeNull();
    expect(safeHref("data:text/html,x")).toBeNull();
    expect(safeHref("https://example.org/a")).toBe("https://example.org/a");
    const out = html("[bad](javascript:alert(1)) [ok](https://example.org)");
    expect(out).not.toContain("javascript:");
    expect(out).toContain('rel="noopener noreferrer nofollow"');
  });
  it("renders headings, lists, tables, quotes and code fences", () => {
    const out = html("## عنوان\n\n- بند ١\n- بند ٢\n\n| أ | ب |\n|---|---|\n| 1 | 2 |\n\n> اقتباس\n\n```\ncode\n```");
    expect(out).toContain("<h3"); expect(out).toContain("<ul"); expect(out).toContain("<table"); expect(out).toContain("<blockquote"); expect(out).toContain("<pre");
  });
});

describe("csv / json helpers", () => {
  it("parses quoted fields, embedded newlines and pages", () => {
    const csv = 'a,b\n1,"x, y"\n2,"line1\nline2"\n3,z\n';
    const p0 = parseCsvPage(csv, 0, 2);
    expect(p0.header).toEqual(["a", "b"]); expect(p0.total).toBe(3);
    expect(p0.rows).toEqual([["1", "x, y"], ["2", "line1\nline2"]]);
    expect(parseCsvPage(csv, 1, 2).rows).toEqual([["3", "z"]]);
  });
  it("counts jsonl records and shows the first ones; handles json objects", () => {
    const j = firstJsonRecords('{"a":1}\n{"a":2}\n{"a":3}\n', "jsonl", 2);
    expect(j.count).toBe(3); expect(j.records).toHaveLength(2); expect(j.keys).toEqual(["a"]);
    expect(firstJsonRecords('{"x":1,"y":2}', "json", 5).count).toBe(2);
  });
});
