import { readFileSync } from "node:fs";
import { join } from "node:path";
import { z } from "zod";

const Schema = z.object({
  version: z.string(),
  sets: z.array(z.object({ key: z.string(), name: z.string(), license: z.string(), count: z.number(), license_file: z.string() })),
  icons: z.array(z.object({ set: z.string(), name: z.string(), file: z.string().startsWith("/assets/icons/") })),
});
export type IconCatalog = z.infer<typeof Schema>;
export function loadIcons(root = process.cwd()): IconCatalog { return Schema.parse(JSON.parse(readFileSync(join(root, "content/icons.json"), "utf8"))); }
