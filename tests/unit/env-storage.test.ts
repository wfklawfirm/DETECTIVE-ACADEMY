import { describe, it, expect, afterEach } from "vitest";
import { env } from "@/server/env";

const keep = { v: process.env.VERCEL, u: process.env.ATHAR_DB_URL };
afterEach(() => {
  if (keep.v === undefined) delete process.env.VERCEL; else process.env.VERCEL = keep.v;
  if (keep.u === undefined) delete process.env.ATHAR_DB_URL; else process.env.ATHAR_DB_URL = keep.u;
});

describe("env.dbEphemeral", () => {
  it("is ephemeral on Vercel with no DB url (defaults to /tmp)", () => {
    process.env.VERCEL = "1"; delete process.env.ATHAR_DB_URL;
    expect(env.dbEphemeral).toBe(true);
  });
  it("is ephemeral on Vercel with a file: url", () => {
    process.env.VERCEL = "1"; process.env.ATHAR_DB_URL = "file:/tmp/x.db";
    expect(env.dbEphemeral).toBe(true);
  });
  it("is persistent on Vercel with a remote libsql url", () => {
    process.env.VERCEL = "1"; process.env.ATHAR_DB_URL = "libsql://example.turso.io";
    expect(env.dbEphemeral).toBe(false);
  });
  it("is persistent for a local file DB off Vercel", () => {
    delete process.env.VERCEL; delete process.env.ATHAR_DB_URL;
    expect(env.dbEphemeral).toBe(false);
  });
});
