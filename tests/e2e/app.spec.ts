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

test("a11y: key public pages have no serious/critical axe violations", async ({ page }) => {
  await page.goto("/"); await passGate(page);
  for (const path of ["/", "/cases", "/academy", "/academy/A1", "/challenges", "/privacy", "/account", "/start", "/knowledge", "/knowledge/KO-RS-05-001", "/sources", "/labs", "/labs/SAFE_LABS-01", "/skills", "/gallery", "/credits"]) {
    await page.goto(path);
    await page.waitForLoadState("networkidle");
    const res = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa"]).analyze();
    const bad = res.violations.filter((v) => ["serious", "critical"].includes(v.impact ?? ""));
    expect(bad.map((v) => `${path}: ${v.id} (${v.nodes.length})`), path).toEqual([]);
    await noHScroll(page);
  }
});

test("a11y: the play workspace tabs", async ({ page }) => {
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
