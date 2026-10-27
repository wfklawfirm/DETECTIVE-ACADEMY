import { createClient, type Client, type InValue, type ResultSet } from "@libsql/client";
import { mkdirSync, readdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { env } from "./env";

type G = typeof globalThis & { __atharDb?: Promise<Client> };
const g = globalThis as G;

export function getDb(): Promise<Client> {
  g.__atharDb ??= (async () => {
    const url = env.dbUrl;
    if (url.startsWith("file:")) {
      const p = url.slice(5).replace(/^\/\//, "");
      if (p && p !== ":memory:") mkdirSync(dirname(p), { recursive: true });
    }
    const c = createClient({ url, authToken: env.dbToken });
    await c.execute("PRAGMA foreign_keys = ON");
    return c;
  })();
  return g.__atharDb;
}

export async function q<T = Record<string, unknown>>(sql: string, args: InValue[] = []): Promise<T[]> {
  const c = await getDb();
  const r = await c.execute({ sql, args });
  return r.rows.map((row) => Object.fromEntries(Object.keys(row).filter((k) => isNaN(Number(k))).map((k) => [k, row[k]])) as T);
}
export async function q1<T = Record<string, unknown>>(sql: string, args: InValue[] = []): Promise<T | null> {
  return (await q<T>(sql, args))[0] ?? null;
}
export async function run(sql: string, args: InValue[] = []): Promise<ResultSet> {
  const c = await getDb();
  return c.execute({ sql, args });
}

export async function migrate(dir = "migrations"): Promise<string[]> {
  const c = await getDb();
  await c.execute("CREATE TABLE IF NOT EXISTS schema_migrations (version TEXT PRIMARY KEY, applied_at TEXT NOT NULL)");
  const done = new Set((await c.execute("SELECT version FROM schema_migrations")).rows.map((r) => String(r.version)));
  const applied: string[] = [];
  for (const f of readdirSync(dir).filter((x) => x.endsWith(".sql")).sort()) {
    const v = f.replace(/\.sql$/, "");
    if (done.has(v)) continue;
    const sql = readFileSync(join(dir, f), "utf8");
    await c.executeMultiple(sql);
    await c.execute({ sql: "INSERT INTO schema_migrations(version, applied_at) VALUES (?, ?)", args: [v, new Date().toISOString()] });
    applied.push(v);
  }
  return applied;
}
