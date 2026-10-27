import { ensureAdmin } from "../src/server/auth";
import { syncFileCases } from "../src/server/content";
import { migrate } from "../src/server/db";
await migrate();
const added = await syncFileCases();
console.log(added.length ? `imported: ${added.join(", ")}` : "cases already imported (drafts refreshed)");
const adm = await ensureAdmin();
console.log(adm ? `admin created: ${adm}` : "admin: unchanged / not configured");
