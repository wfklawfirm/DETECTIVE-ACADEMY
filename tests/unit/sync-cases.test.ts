import { beforeAll, describe, expect, it } from "vitest";
import { migrate, q1, run } from "@/server/db";
import { listFileCaseIds, readFileTriplet, syncFileCases } from "@/server/content";

beforeAll(async () => { await migrate(); await syncFileCases(); });

/** syncFileCases runs at every cold start; it was rewritten to one listing query. Its observable behaviour must not change. */
describe("syncFileCases", () => {
  const id = listFileCaseIds()[0]!;
  const core = readFileTriplet("content/cases", id)!.core as { case_id: string; case_version: string };
  const row = () => q1<{ ui_json: string; status: string }>("SELECT ui_json, status FROM case_versions WHERE case_id = ? AND version = ?", [core.case_id, core.case_version]);

  it("is idempotent: a second run imports nothing new", async () => {
    expect(await syncFileCases()).toEqual([]);
  });

  it("refreshes a draft row from the files", async () => {
    await run("UPDATE case_versions SET ui_json = '{}', status = 'draft' WHERE case_id = ? AND version = ?", [core.case_id, core.case_version]);
    await syncFileCases();
    expect((await row())!.ui_json).not.toBe("{}");
  });

  it("never rewrites a published row", async () => {
    await run("UPDATE case_versions SET ui_json = '{\"kept\":1}', status = 'published' WHERE case_id = ? AND version = ?", [core.case_id, core.case_version]);
    try {
      await syncFileCases();
      const r = (await row())!;
      expect(r.status).toBe("published");
      expect(r.ui_json).toBe('{"kept":1}');
    } finally {
      await run("UPDATE case_versions SET status = 'draft' WHERE case_id = ? AND version = ?", [core.case_id, core.case_version]);
      await syncFileCases(); // restore the file content for any later test in this process
    }
  });
});
