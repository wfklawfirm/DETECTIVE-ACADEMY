import { existsSync } from "node:fs";

if (!process.env.ATHAR_SECRET && existsSync(".env.local")) {
  try { process.loadEnvFile(".env.local"); } catch { /* ignore */ }
}

function need(name: string, min = 1): string {
  const v = process.env[name];
  if (!v || v.length < min) throw new Error(`متغير البيئة ${name} مفقود أو قصير (الحد الأدنى ${min}). شغّل: npm run setup`);
  return v;
}

export const env = {
  get secret() { return need("ATHAR_SECRET", 32); },
  get dbUrl() { return process.env.ATHAR_DB_URL || (process.env.VERCEL ? "file:/tmp/athar.db" : "file:./data/athar.db"); },
  /** Serverless hosts start with an empty disk: create the schema, import the file cases and ensure the admin at boot. */
  get autoBootstrap() { return process.env.ATHAR_AUTO_BOOTSTRAP === "1" || !!process.env.VERCEL; },
  get dbToken() { return process.env.ATHAR_DB_AUTH_TOKEN || undefined; },
  get adminEmail() { return process.env.ATHAR_ADMIN_EMAIL || ""; },
  get adminPassword() { return process.env.ATHAR_ADMIN_PASSWORD || ""; },
  /** Preview mode lets un-reviewed cases be played (clearly labelled). Off => only fully-approved, published versions. */
  get allowPreview() { return process.env.ATHAR_ALLOW_PREVIEW === "1"; },
  get aiProvider() { return process.env.ATHAR_AI_PROVIDER || "local"; },
  /** per-IP requests/minute (shared NATs such as schools need headroom) */
  get playRate() { return Number(process.env.ATHAR_PLAY_RATE) || 240; },
  get apiRate() { return Number(process.env.ATHAR_API_RATE) || 300; },
  get isProd() { return process.env.NODE_ENV === "production"; },
  get secureCookies() { return process.env.ATHAR_INSECURE_COOKIES === "1" ? false : process.env.NODE_ENV === "production"; },
};
