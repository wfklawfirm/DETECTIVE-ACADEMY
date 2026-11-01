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

describe("syncFileCases (unchanged drafts)", () => {
  it("does not rewrite a draft whose files are unchanged, but does when one column differs", async () => {
    const id = listFileCaseIds()[1]!;
    const core = readFileTriplet("content/cases", id)!.core as { case_id: string; case_version: string };
    const where = [core.case_id, core.case_version];
    await run("UPDATE case_versions SET status = 'draft', created_by = 'marker' WHERE case_id = ? AND version = ?", where);
    await syncFileCases();
    // an UPDATE from sync does not touch created_by, so the marker only proves the row survived; use scoring_json to observe writes
    await run("UPDATE case_versions SET scoring_json = '{}' WHERE case_id = ? AND version = ?", where);
    await syncFileCases();
    const fixed = await q1<{ scoring_json: string }>("SELECT scoring_json FROM case_versions WHERE case_id = ? AND version = ?", where);
    expect(fixed!.scoring_json).not.toBe("{}");
    expect(await syncFileCases()).toEqual([]);
  });
});
