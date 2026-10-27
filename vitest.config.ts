import { defineConfig } from "vitest/config";
import path from "node:path";

export default defineConfig({
  resolve: { alias: { "@": path.resolve(__dirname, "src") } },
  test: {
    include: ["tests/unit/**/*.test.ts"],
    environment: "node",
    env: { ATHAR_SECRET: "unit-test-secret-unit-test-secret-0000", ATHAR_DB_URL: "file::memory:", ATHAR_ALLOW_PREVIEW: "1", ATHAR_ADMIN_EMAIL: "", ATHAR_ADMIN_PASSWORD: "" },
    testTimeout: 20000,
  },
});
