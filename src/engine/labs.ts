import { readFileSync } from "node:fs";
import { join } from "node:path";
import { z } from "zod";

export const LabSchema = z.object({
  id: z.string().regex(/^SAFE_LABS-\d{2}$/), title_ar: z.string(), skill_ar: z.string(), intro_ar: z.string(),
  categories: z.array(z.object({ id: z.string(), label_ar: z.string() })).min(2).max(4),
  items: z.array(z.object({ id: z.string(), text_ar: z.string(), answer: z.string(), why_ar: z.string() })).min(3).max(8),
  transfer_ar: z.string(), boundary_ar: z.string(),
}).superRefine((l, ctx) => {
  const ids = new Set(l.categories.map((c) => c.id));
  l.items.forEach((it, i) => { if (!ids.has(it.answer)) ctx.addIssue({ code: "custom", message: `item ${it.id}: unknown answer category`, path: ["items", i] }); });
});
export type Lab = z.infer<typeof LabSchema>;
export const LabsFileSchema = z.object({
  version: z.string(),
  catalogue: z.array(z.object({ id: z.string(), title_ar: z.string(), interaction_ar: z.string(), skill_ar: z.string(), boundary_ar: z.string(), playable: z.boolean() })),
  playable: z.array(LabSchema),
});
export function loadLabs(root = process.cwd()) {
  const f = LabsFileSchema.parse(JSON.parse(readFileSync(join(root, "content/labs/labs.json"), "utf8")));
  const ids = new Set(f.catalogue.map((c) => c.id));
  for (const l of f.playable) if (!ids.has(l.id)) throw new Error(`playable lab ${l.id} missing from catalogue`);
  return f;
}
