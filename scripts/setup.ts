import { randomBytes } from "node:crypto";
import { existsSync, writeFileSync } from "node:fs";
if (existsSync(".env.local")) { console.log(".env.local already exists — left untouched."); process.exit(0); }
const pw = randomBytes(12).toString("base64url");
const body = [
  `ATHAR_SECRET=${randomBytes(48).toString("base64url")}`,
  "ATHAR_DB_URL=file:./data/athar.db",
  "ATHAR_ADMIN_EMAIL=admin@athar.local",
  `ATHAR_ADMIN_PASSWORD=${pw}`,
  "# Preview lets un-reviewed (not yet approved) cases be played, clearly labelled. Remove for production.",
  "ATHAR_ALLOW_PREVIEW=1",
  "ATHAR_INSECURE_COOKIES=1",
  "ATHAR_AI_PROVIDER=local",
  "",
].join("\n");
writeFileSync(".env.local", body, { mode: 0o600 });
console.log(`created .env.local\nadmin: admin@athar.local / ${pw}\n(change before any non-local use)`);
