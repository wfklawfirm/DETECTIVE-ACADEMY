import { readFileSync } from "node:fs";
import type { HookDef, RiddleDef } from "../engine/hooks";

type G = typeof globalThis & { __atharHooks?: { hooks: HookDef[]; riddles: RiddleDef[] } };
export function hookData(): { hooks: HookDef[]; riddles: RiddleDef[] } {
  const g = globalThis as G;
  g.__atharHooks ??= {
    hooks: (JSON.parse(readFileSync("content/hooks/global.json", "utf8")) as { hooks: HookDef[] }).hooks,
    riddles: (JSON.parse(readFileSync("content/hooks/riddles.json", "utf8")) as { riddles: RiddleDef[] }).riddles,
  };
  return g.__atharHooks;
}
