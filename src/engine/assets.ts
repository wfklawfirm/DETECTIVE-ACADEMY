import { readFileSync } from "node:fs";
import { join } from "node:path";
import { z } from "zod";

export const AssetSchema = z.object({
  id: z.string(), kind: z.enum(["image", "audio"]), file: z.string().startsWith("/assets/"), title: z.string(), creator: z.string(),
  date: z.string().optional(), institution: z.string().optional(), source: z.string(), license: z.string(), attribution: z.string(), use: z.string(),
  w: z.number().optional(), h: z.number().optional(), duration_s: z.number().optional(),
  tags: z.array(z.string()).optional(), collection: z.string().optional(), modified: z.string().optional(),
});
export type Asset = z.infer<typeof AssetSchema>;
/** Only CC0, public-domain and CC BY items may ship; anything else is rejected at load time. */
const OK = /(CC0|public domain|isPublicDomain|No known (copyright )?restrictions|unaware of any|CC BY(-SA)? [234]\.0|Attribution 4\.0|Public Domain Mark)/i;
const NOT_OK = /(\bNC\b|-NC|\bND\b|-ND|all rights reserved)/i;
export function loadAssets(root = process.cwd()): Asset[] {
  const f = z.object({ items: z.array(AssetSchema) }).parse(JSON.parse(readFileSync(join(root, "content/assets.json"), "utf8")));
  for (const a of f.items) if (!OK.test(a.license) || NOT_OK.test(a.license)) throw new Error(`asset ${a.id} has a licence that is not cleared for shipping: ${a.license}`);
  return f.items;
}
