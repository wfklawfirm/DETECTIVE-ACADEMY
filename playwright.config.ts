import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "tests/e2e",
  timeout: 60_000,
  retries: 0,
  workers: 1,
  use: { baseURL: "http://127.0.0.1:3100", trace: "retain-on-failure", locale: "ar" },
  webServer: {
    command: "npm run migrate && npm run seed && npm run start",
    url: "http://127.0.0.1:3100",
    reuseExistingServer: false,
    timeout: 120_000,
    env: { ATHAR_DB_URL: "file:./data/e2e.db", ATHAR_SECRET: "e2e-secret-e2e-secret-e2e-secret-00", ATHAR_ADMIN_EMAIL: "admin@athar.local", ATHAR_ADMIN_PASSWORD: "e2e-admin-pass-123!", ATHAR_ALLOW_PREVIEW: "1", ATHAR_INSECURE_COOKIES: "1", ATHAR_PLAY_RATE: "5000", ATHAR_API_RATE: "5000" },
  },
  projects: [
    { name: "mobile", use: { ...devices["Pixel 7"], locale: "ar" } },
    { name: "desktop", use: { viewport: { width: 1366, height: 800 }, locale: "ar" } },
  ],
});
