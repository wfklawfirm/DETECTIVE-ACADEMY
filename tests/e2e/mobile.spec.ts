import { expect, test, type Page } from "@playwright/test";

/* Mobile behaviour: every lab kind, rotation, offline, reload, touch-target size.
   Age band is set by cookie so the gate does not interfere. */
const LABS: Record<string, string> = {
  classify: "SAFE_LABS-01", slider: "SAFE_LABS-04", conclude: "SAFE_LABS-12", order: "SAFE_LABS-24",
  spot: "SAFE_LABS-30", measure: "SAFE_LABS-36", match: "SAFE_LABS-46",
};
const VIEWPORTS = [{ w: 320, h: 640 }, { w: 390, h: 844 }, { w: 844, h: 390 }]; // last = landscape

test.beforeEach(async ({ context, baseURL }) => {
  await context.addCookies([{ name: "athar_age", value: "16-17", url: baseURL! }]);
});

const overflow = (page: Page) => page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);

const tooSmall = (page: Page) => page.evaluate(() =>
  [...document.querySelectorAll("a[href],button,input,select,textarea,[role=button],[role=tab]")]
    .filter((e) => {
      if (e.matches("input[type=radio],input[type=checkbox]")) { const l = e.closest("label"); if (l && l.getBoundingClientRect().height >= 43.5) return false; }
      const r = e.getBoundingClientRect();
      return r.width > 0 && r.height > 0 && getComputedStyle(e).visibility !== "hidden" && !e.closest(".sr-only") && (r.height < 43.5 || r.width < 43.5);
    })
    .map((e) => `${e.tagName}.${String(e.className).split(" ")[0]} ${Math.round(e.getBoundingClientRect().width)}x${Math.round(e.getBoundingClientRect().height)}`));

for (const [kind, id] of Object.entries(LABS)) {
  test(`lab kind "${kind}": renders, no horizontal scroll, touch targets ≥44px at 320/390/landscape`, async ({ page, isMobile }) => {
    test.skip(!isMobile, "touch-target sizing applies to coarse pointers (mobile project) only");
    for (const v of VIEWPORTS) {
      await page.setViewportSize({ width: v.w, height: v.h });
      await page.goto(`/labs/${id}`);
      await page.waitForLoadState("networkidle");
      await expect(page.locator("main h1")).toHaveCount(1);
      expect(await overflow(page), `${kind} ${v.w}x${v.h}`).toBeLessThanOrEqual(1);
      expect(await tooSmall(page), `${kind} ${v.w}x${v.h} small targets`).toEqual([]);
    }
  });
}

test("rotation: portrait → landscape → portrait keeps content and never scrolls sideways", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/cases"); await page.waitForLoadState("networkidle");
  const title = await page.locator("main h1").first().innerText();
  for (const v of [{ width: 844, height: 390 }, { width: 390, height: 844 }]) {
    await page.setViewportSize(v);
    await expect(page.locator("main h1").first()).toHaveText(title);
    expect(await overflow(page)).toBeLessThanOrEqual(1);
  }
});

test("reload: a lab page re-renders the same content after a reload", async ({ page }) => {
  await page.goto("/labs/SAFE_LABS-01"); await page.waitForLoadState("networkidle");
  const h1 = await page.locator("main h1").innerText();
  await page.reload(); await page.waitForLoadState("networkidle");
  await expect(page.locator("main h1")).toHaveText(h1);
});

test("offline: an already-open page stays usable and a new navigation fails gracefully (no crash)", async ({ page, context }) => {
  await page.goto("/home"); await page.waitForLoadState("networkidle");
  await context.setOffline(true);
  await expect(page.locator("main")).toBeVisible();
  expect(await overflow(page)).toBeLessThanOrEqual(1);
  // in-app navigation while offline must not leave a blank screen
  await page.getByRole("navigation", { name: "التنقل الرئيسي" }).getByRole("link").nth(1).click().catch(() => {});
  await page.waitForTimeout(1500);
  await expect(page.locator("body")).not.toBeEmpty();
  await context.setOffline(false);
});

test("cases: phone shows one filter button that opens a bottom sheet; inline filters appear from 768px", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/cases"); await page.waitForLoadState("networkidle");
  const open = page.getByRole("button", { name: /تصفية وترتيب/ });
  await expect(open).toBeVisible();
  await expect(page.getByRole("group", { name: "تصفية القضايا" })).toBeHidden();
  await open.click();
  const dlg = page.getByRole("dialog", { name: "تصفية وترتيب القضايا" });
  await expect(dlg).toBeVisible();
  await dlg.getByRole("button", { name: /مفتوحة/ }).click();
  await dlg.getByRole("button", { name: /عرض/ }).click();
  await expect(dlg).toBeHidden();
  await expect(open).toContainText("1"); // active-filter badge
  await page.setViewportSize({ width: 1024, height: 800 });
  await expect(open).toBeHidden();
  await expect(page.getByRole("group", { name: "تصفية القضايا" })).toBeVisible();
});

test("academy: first path open, other paths folded; lesson list is a real disclosure", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/academy"); await page.waitForLoadState("networkidle");
  const d = page.locator("details.track-lessons-details");
  expect(await d.count()).toBeGreaterThan(1);
  await expect(d.first()).toHaveAttribute("open", "");
  await expect(d.nth(1)).not.toHaveAttribute("open", "");
  await d.nth(1).locator("summary").click();
  await expect(d.nth(1)).toHaveAttribute("open", "");
});

test("workspace: there is always a visible way back to Home (desktop has no sidebar in /play)", async ({ page }) => {
  await page.goto("/play/c000_lost_notebook"); await page.waitForLoadState("networkidle");
  const home = page.getByRole("link", { name: "الرئيسية" }).first();
  await expect(home).toBeVisible();
  await home.click();
  await expect(page).toHaveURL(/\/home$/);
});
