import AxeBuilder from "@axe-core/playwright";
import { expect, test, type Page } from "@playwright/test";

async function passGate(page: Page) {
  const btn = page.getByRole("button", { name: /18 سنة/ });
  await btn.waitFor({ state: "visible", timeout: 8000 });
  await btn.click();
  await expect(btn).toBeHidden();
}
const noHScroll = async (page: Page) => { const o = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth); expect(o).toBeLessThanOrEqual(1); };

test("RTL document, age gate, and entry hook on landing", async ({ page }) => {
  await page.goto("/");
  await passGate(page);
  await expect(page.locator("html")).toHaveAttribute("dir", "rtl");
  await expect(page.locator("html")).toHaveAttribute("lang", "ar");
  await expect(page.getByLabel("تلميح الدخول")).toBeVisible();
  await noHScroll(page);
});

test("under-16 is turned away and nothing is stored", async ({ page, context }) => {
  await page.goto("/");
  await page.getByRole("button", { name: /أقل من 16/ }).click();
  await expect(page.locator("[role=alert]").filter({ hasText: "السادسة عشرة" })).toBeVisible();
  const cookies = await context.cookies();
  expect(cookies.find((c) => c.name === "athar_age")).toBeUndefined();
});

test("a new hook appears at every entry (different on consecutive visits)", async ({ page }) => {
  await page.goto("/"); await passGate(page);
  const seen = new Set<string>();
  for (let i = 0; i < 4; i++) {
    await page.goto("/home");
    const hook = page.getByLabel("تلميح الدخول");
    await expect(hook).toBeVisible();
    seen.add((await hook.locator("p").innerText()).trim());
  }
  expect(seen.size).toBeGreaterThanOrEqual(3);
});

test("onboarding → tutorial: first actions, interview, no hidden truth in network responses", async ({ page }) => {
  const bodies: string[] = [];
  page.on("response", async (r) => { if (r.url().includes("/api/play/") && !r.url().endsWith("debrief")) { try { bodies.push(await r.text()); } catch { /* */ } } });
  await page.goto("/"); await passGate(page);
  await page.goto("/start");
  await page.getByRole("button", { name: "التالي" }).click(); await page.getByRole("button", { name: "التالي" }).click();
  await page.getByRole("link", { name: "افتح الملف" }).click();
  await expect(page.getByRole("tab", { name: /الأدلة/ })).toBeVisible();
  await noHScroll(page);
  for (const label of [/اقرأ ورقة/, /سجل بوابة/, /ابحث في طلبات/]) { await expect(page.getByRole("button", { name: label })).toBeEnabled(); await page.getByRole("button", { name: label }).click(); }
  await page.getByRole("tab", { name: /الأدلة/ }).click();
  await expect(page.locator("article.paper").first()).toBeVisible();
  // interview and ask
  await page.getByRole("tab", { name: /الملف/ }).click();
  await page.getByRole("button", { name: /ابدأ مقابلة د. جمال/ }).click();
  await expect(page.getByRole("heading", { name: /جمال/ })).toBeVisible();
  await page.locator("button.topic-btn").first().click();
  await expect(page.locator(".bubble").nth(1)).toBeVisible();
  // before submission: no debrief text
  expect(bodies.join("")).not.toContain("reference_answer_ar");
  expect(bodies.join("")).not.toContain("accepted_conclusions");
});

const PAGES = ["/", "/start", "/home", "/cases", "/case/c000_lost_notebook", "/academy", "/academy/A1", "/challenges", "/profile", "/account", "/privacy", "/report", "/review/ABC123", "/knowledge", "/knowledge/KO-RS-05-001", "/sources", "/labs", "/labs/SAFE_LABS-01", "/skills", "/gallery", "/credits", "/studio", "/sounds", "/icons", "/season", "/glossary", "/methods", "/biases", "/reasoning", "/rulebook", "/atlas", "/archetypes", "/heritage", "/heritage/poe-rue-morgue", "/books", "/books/BK-741", "/books/drills", "/labs/SAFE_LABS-30", "/academy/educators", "/no-such-page"];
const setTheme = (page: Page, t: "dark" | "light") => page.addInitScript((v) => { try { localStorage.setItem("athar.theme", v); } catch { /* */ } }, t);
const serious = (res: { violations: { id: string; impact?: string | null; nodes: unknown[] }[] }) => res.violations.filter((v) => ["serious", "critical"].includes(v.impact ?? ""));

for (const theme of ["dark", "light"] as const) {
  test(`a11y (${theme}): every page has no serious/critical axe violations and no horizontal scroll`, async ({ page }) => {
    await setTheme(page, theme);
    await page.goto("/"); await passGate(page);
    await expect(page.locator("html")).toHaveAttribute("data-theme", theme);
    for (const path of PAGES) {
      await page.goto(path);
      await page.waitForLoadState("networkidle");
      await page.waitForTimeout(250);
      const res = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa"]).analyze();
      expect(serious(res).map((v) => `${path}: ${v.id} (${v.nodes.length})`), `${theme} ${path}`).toEqual([]);
      await noHScroll(page);
    }
  });
}

test("a11y: age gate sheet and open menu sheet", async ({ page }) => {
  await page.goto("/");
  const dlg = page.getByRole("dialog", { name: "قبل أن نبدأ" });
  await expect(dlg).toBeVisible();
  await expect(dlg).toHaveAttribute("aria-modal", "true");
  expect(serious(await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa"]).analyze()).map((v) => v.id)).toEqual([]);
  await passGate(page);
  await page.getByRole("button", { name: "القائمة" }).click();
  await expect(page.getByRole("dialog", { name: "القائمة" })).toBeVisible();
  expect(serious(await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa"]).analyze()).map((v) => v.id)).toEqual([]);
});

test("mobile: no horizontal scroll at 320px on every page", async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 700 });
  await page.goto("/"); await passGate(page);
  for (const path of PAGES) { await page.goto(path); await page.waitForLoadState("networkidle"); await noHScroll(page); }
  await page.goto("/play/c000_lost_notebook");
  await expect(page.getByRole("tab", { name: /الأدلة/ })).toBeVisible();
  for (const t of [/الملف/, /الأدلة/, /الشخصيات/, /اللوحة/, /الزمن/, /المفكرة/, /الاستنتاج/]) { await page.getByRole("tab", { name: t }).click(); await noHScroll(page); }
});

test("theme: toggle in the menu sheet switches data-theme and persists across reload (no flash)", async ({ page }) => {
  await page.goto("/"); await passGate(page);
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
  await page.getByRole("button", { name: "القائمة" }).click();
  await page.getByRole("radiogroup", { name: "السمة" }).getByRole("radio", { name: "فاتح" }).check();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
  const bg = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
  expect(bg).toBe("rgb(242, 239, 232)");
  await page.reload();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
  await page.getByRole("button", { name: "القائمة" }).click();
  await page.getByRole("radiogroup", { name: "السمة" }).getByRole("radio", { name: "داكن" }).check();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
});

test("menu: large text and reduce-motion toggles set root attributes", async ({ page }) => {
  await page.goto("/"); await passGate(page);
  await page.getByRole("button", { name: "القائمة" }).click();
  await page.getByRole("switch", { name: "نص أكبر" }).click();
  await page.getByRole("switch", { name: "تقليل الحركة" }).click();
  await expect(page.locator("html")).toHaveAttribute("data-text-size", "large");
  await expect(page.locator("html")).toHaveAttribute("data-motion", "off");
  await page.reload();
  await expect(page.locator("html")).toHaveAttribute("data-text-size", "large");
  const dur = await page.getByLabel("تلميح الدخول").evaluate((el) => getComputedStyle(el).animationDuration);
  expect(parseFloat(dur)).toBeLessThan(0.01);
});

test("menu sheet: opens, traps focus, closes on Escape and restores focus; holds nav, footer links and sound toggle", async ({ page }) => {
  await page.goto("/home"); await passGate(page);
  const opener = page.getByRole("button", { name: "القائمة" });
  await opener.click();
  const dlg = page.getByRole("dialog", { name: "القائمة" });
  await expect(dlg).toBeVisible();
  for (const name of ["الرئيسية", "القضايا", "الأكاديمية", "الموسوعة", "مهاراتي", "مختبرات آمنة", "المصادر والحقوق", "معرض المراجع", "الاعتمادات", "الخصوصية والسلامة", "أبلِغ عن مشكلة"]) await expect(dlg.getByRole("link", { name: new RegExp(name) })).toBeVisible();
  await expect(dlg.getByRole("switch", { name: "المؤثرات الصوتية" })).toBeVisible();
  for (let i = 0; i < 40; i++) await page.keyboard.press("Tab");
  expect(await page.evaluate(() => !!document.activeElement?.closest("[role=dialog]"))).toBe(true);
  await page.keyboard.press("Escape");
  await expect(dlg).toBeHidden();
  await expect(opener).toBeFocused();
});

test("bottom nav: five destinations on top-level screens, navigates, hidden on landing, /start and /play", async ({ page }) => {
  await page.goto("/"); await passGate(page);
  await expect(page.getByRole("navigation", { name: "التنقل الرئيسي" })).toBeHidden();
  await page.goto("/home");
  const nav = page.getByRole("navigation", { name: "التنقل الرئيسي" });
  await expect(nav.getByRole("link")).toHaveCount(5);
  await expect(nav.getByRole("link", { name: "الرئيسية" })).toHaveAttribute("aria-current", "page");
  for (const [name, url] of [["القضايا", /\/cases$/], ["الأكاديمية", /\/academy$/], ["الموسوعة", /\/knowledge$/], ["مهاراتي", /\/profile$/]] as const) {
    await nav.getByRole("link", { name }).click();
    await expect(page).toHaveURL(url);
    await expect(nav.getByRole("link", { name })).toHaveAttribute("aria-current", "page");
  }
  await page.goto("/start");
  await expect(page.getByRole("navigation", { name: "التنقل الرئيسي" })).toBeHidden();
  await page.goto("/play/c000_lost_notebook");
  await expect(page.getByRole("tab", { name: /الأدلة/ })).toBeVisible();
  await expect(page.getByRole("navigation", { name: "التنقل الرئيسي" })).toBeHidden();
  await expect(page.getByRole("tablist", { name: "أقسام التحقيق" })).toBeVisible();
});

test("manifest and icons are served", async ({ request }) => {
  const m = await request.get("/manifest.webmanifest");
  expect(m.ok()).toBe(true);
  const j = await m.json();
  expect(j.display).toBe("standalone"); expect(j.dir).toBe("rtl"); expect(j.lang).toBe("ar"); expect(j.theme_color).toBe("#0b1115");
  for (const i of j.icons) expect((await request.get(i.src)).ok()).toBe(true);
});

for (const theme of ["dark", "light"] as const) test(`a11y (${theme}): the play workspace tabs`, async ({ page }) => {
  await setTheme(page, theme);
  await page.goto("/"); await passGate(page);
  await page.goto("/play/c000_lost_notebook");
  await expect(page.getByRole("tab", { name: /الأدلة/ })).toBeVisible();
  await page.getByRole("button", { name: /اقرأ ورقة/ }).click();
  for (const t of [/الملف/, /الأدلة/, /الشخصيات/, /اللوحة/, /الزمن/, /المفكرة/, /الاستنتاج/]) {
    await page.getByRole("tab", { name: t }).click();
    const res = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa"]).analyze();
    expect(res.violations.filter((v) => ["serious", "critical"].includes(v.impact ?? "")).map((v) => `${String(t)}: ${v.id}`)).toEqual([]);
    await noHScroll(page);
  }
});

test("reduced motion removes animation", async ({ page }) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/"); await passGate(page);
  const dur = await page.getByLabel("تلميح الدخول").evaluate((el) => getComputedStyle(el).animationDuration);
  expect(parseFloat(dur)).toBeLessThan(0.01);
});

test("studio is closed to anonymous users; admin can sign in", async ({ page, request }) => {
  const r = await request.get("/api/studio/versions");
  expect(r.status()).toBe(401);
  await page.goto("/"); await passGate(page);
  await page.goto("/account");
  await page.getByLabel("البريد الإلكتروني").fill("admin@athar.local");
  await page.getByLabel("كلمة المرور").fill("e2e-admin-pass-123!");
  await page.getByRole("button", { name: "دخول" }).click();
  await page.waitForURL(/\/home/);
  await page.goto("/studio");
  await expect(page.getByRole("heading", { name: "استوديو المحتوى" })).toBeVisible();
  await expect(page.getByText("c001_last_observation@0.1.0")).toBeVisible();
});

test("CSRF: cross-origin mutation is refused", async ({ request }) => {
  const r = await request.post("/api/report", { headers: { origin: "https://evil.example" }, data: { kind: "other", body: "hello world" } });
  expect(r.status()).toBeGreaterThanOrEqual(400);
});

test("UI: complete the tutorial through the final-deduction form to the debrief and transfer-free summary", async ({ page }) => {
  await page.goto("/"); await passGate(page);
  await page.goto("/play/c000_lost_notebook");
  await expect(page.getByRole("tab", { name: /الأدلة/ })).toBeVisible();
  // thorough exploration through the public API with the same signed device token the UI uses
  await page.evaluate(async () => {
    const key = "athar.s.c000_lost_notebook";
    const call = async (req: Record<string, unknown>) => {
      const r = await fetch("/api/play/c000_lost_notebook", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ token: localStorage.getItem(key), req }) });
      if (!r.ok) return null; const j = await r.json(); if (j.token) localStorage.setItem(key, j.token); return j.view;
    };
    let v = await call({ op: "state" });
    for (let round = 0; round < 6; round++) {
      for (const a of v.actions) v = (await call({ op: "act", action_id: a.id })) ?? v;
      for (const c of v.characters) { if (!c.interview_open) continue;
        for (const t of c.topics) v = (await call({ op: "ask", character_id: c.id, topic_id: t.id })) ?? v;
        for (const e of v.evidence) v = (await call({ op: "present", evidence_id: e.id, character_id: c.id })) ?? v; }
    }
  });
  await page.reload();
  await page.getByRole("tab", { name: /الاستنتاج/ }).click();
  await page.getByRole("button", { name: "ابدأ الاستنتاج النهائي" }).click();
  await page.getByLabel(/نقلت فنية المختبر/).check();
  const selects = page.locator("fieldset").nth(1).locator("select");
  await selects.nth(0).selectOption("supports");
  await page.getByRole("button", { name: "قدّم الاستنتاج" }).click();
  await expect(page.getByRole("heading", { name: "ما الذي حدث فعلاً؟" })).toBeVisible();
  await expect(page.getByText("هذه درجة تعليمية مبدئية")).toBeVisible();
  const res = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa"]).analyze();
  expect(res.violations.filter((v) => ["serious", "critical"].includes(v.impact ?? "")).map((v) => v.id)).toEqual([]);
});

test("safe lab: classify, reveal feedback, retry", async ({ page }) => {
  await page.goto("/"); await passGate(page);
  await page.goto("/labs/SAFE_LABS-01");
  const groups = page.getByRole("radiogroup");
  const n = await groups.count();
  for (let i = 0; i < n; i++) await groups.nth(i).getByRole("radio").first().click();
  await page.getByRole("button", { name: "اكشف التعليق" }).click();
  await expect(page.getByText(/وافقت تصنيف المختبر/)).toBeVisible();
  await page.getByRole("button", { name: "أعد المحاولة" }).click();
  await expect(page.getByRole("button", { name: "اكشف التعليق" })).toBeDisabled();
});
