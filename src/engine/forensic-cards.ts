import { readFileSync } from "node:fs";
import { join } from "node:path";
import { z } from "zod";

const nonEmpty = z.string().trim().min(1);

export const ForensicCardSchema = z.object({
  ko_id: z.string().regex(/^KO-[A-Z0-9]+-\d{2}[A-Z]?-\d{3}$/),
  myth_ar: nonEmpty,
  reality_ar: nonEmpty,
  limits_ar: z.array(nonEmpty).min(2).max(4),
  safe_note_ar: nonEmpty,
});
export type ForensicCard = z.infer<typeof ForensicCardSchema>;

export const ForensicCardsFileSchema = z.object({ version: z.string(), cards: z.array(ForensicCardSchema) });

export function loadForensicCards(root = process.cwd()): ForensicCard[] {
  const f = ForensicCardsFileSchema.parse(JSON.parse(readFileSync(join(root, "content/knowledge/forensic_cards_ar.json"), "utf8")));
  return f.cards;
}

export function forensicCardFor(cards: ForensicCard[], koId: string): ForensicCard | undefined {
  return cards.find((c) => c.ko_id === koId);
}
