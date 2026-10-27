"use client";
import { useState } from "react";
import { Card, CardTitle } from "./ui/card";
import { Callout } from "./ui/feedback";
import { ChoiceGroup } from "./ui/form";

export function Practice({ practice }: { practice: { prompt_ar: string; options: { id: string; text_ar: string }[]; answer_id: string; explanation_ar: string } }) {
  const [sel, setSel] = useState<string | null>(null);
  const done = sel !== null;
  const states: Record<string, "correct" | "wrong"> | undefined = done ? { [practice.answer_id]: "correct", ...(sel !== practice.answer_id ? { [sel]: "wrong" as const } : {}) } : undefined;
  return (
    <Card as="section" aria-labelledby="pr-h">
      <CardTitle id="pr-h" level={2}>جرّب بنفسك</CardTitle>
      <p id="pr-q">{practice.prompt_ar}</p>
      <ChoiceGroup labelledBy="pr-q" name="practice" value={sel} disabled={done} onChange={setSel} states={states} options={practice.options.map((o) => ({ value: o.id, label: o.text_ar }))} />
      {sel && <div role="status" className="stack-sm"><Callout tone={sel === practice.answer_id ? "positive" : "negative"}>{sel === practice.answer_id ? "إجابة صحيحة." : "ليست الإجابة الأدق."}</Callout><p>{practice.explanation_ar}</p></div>}
    </Card>
  );
}
