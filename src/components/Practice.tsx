"use client";
import { useState } from "react";

export function Practice({ practice }: { practice: { prompt_ar: string; options: { id: string; text_ar: string }[]; answer_id: string; explanation_ar: string } }) {
  const [sel, setSel] = useState<string | null>(null);
  return (
    <section className="card stack" aria-labelledby="pr-h">
      <h3 id="pr-h">جرّب بنفسك</h3>
      <p>{practice.prompt_ar}</p>
      {practice.options.map((o) => {
        const done = sel !== null; const right = o.id === practice.answer_id;
        return <button key={o.id} className="btn" disabled={done} aria-pressed={sel === o.id} style={{ justifyContent: "flex-start", textAlign: "start", borderColor: done && right ? "var(--green)" : done && sel === o.id ? "var(--rose)" : undefined }} onClick={() => setSel(o.id)}>{o.text_ar}{done && right ? " ✓" : ""}</button>;
      })}
      {sel && <div role="status"><p className={sel === practice.answer_id ? "ok" : "err"}>{sel === practice.answer_id ? "إجابة صحيحة." : "ليست الإجابة الأدق."}</p><p>{practice.explanation_ar}</p></div>}
    </section>
  );
}
