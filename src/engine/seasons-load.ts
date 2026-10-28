import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { SeasonSchema, resolveSeason, type Season } from "./seasons";

/** Server only (node:fs). The client imports ./seasons instead. */
export function loadSeason(id = "season1"): Season {
  if (!/^[a-z0-9]+$/.test(id)) throw new Error("bad season id");
  return SeasonSchema.parse(JSON.parse(readFileSync(join(process.cwd(), "content", "seasons", `${id}.json`), "utf8")));
}

export function existingCaseIds(): string[] {
  const dir = join(process.cwd(), "content", "cases");
  return readdirSync(dir).filter((f) => /^c\d{3}_[a-z0-9_]+\.json$/.test(f) && !f.endsWith(".ui.json") && !f.endsWith(".scoring.json")).map((f) => f.replace(/\.json$/, "")).sort();
}

export function loadResolvedSeason(id = "season1") {
  return resolveSeason(loadSeason(id), existingCaseIds());
}
