"use client";
import { useState } from "react";
import type { Lab } from "@/engine/labs";
import { Button } from "./ui/button";
import { Card } from "./ui/card";
import { ChoiceGroup } from "./ui/form";

export function LabRunner({ lab }: { lab: Lab }) {
  const [pick, setPick] = useState<Record<string, string>>({});
  const [done, setDone] = useState(false);
  const all = lab.items.every((i) => pick[i.id]);
  const right = lab.items.filter((i) => pick[i.id] === i.answer).length;
  return (
    <div className="stack">
      {lab.items.map((it) => {
        const mine = pick[it.id];
        const states = done ? ({ [it.answer]: "correct", ...(mine && mine !== it.answer ? { [mine]: "wrong" } : {}) } as Record<string, "correct" | "wrong">) : undefined;
        return (
          <fieldset key={it.id} className="card" disabled={done}>
            <legend className="text-label">معلومة</legend>
            <p>{it.text_ar}</p>
            <ChoiceGroup label={it.text_ar} name={`lab-${it.id}`} value={mine ?? null} states={states} onChange={(v) => setPick({ ...pick, [it.id]: v })} options={lab.categories.map((c) => ({ value: c.id, label: c.label_ar }))} />
            {done && <p className="small" role="status"><b>{mine === it.answer ? "أصبت. " : `الأقرب: «${lab.categories.find((c) => c.id === it.answer)?.label_ar}». `}</b>{it.why_ar}</p>}
          </fieldset>
        );
      })}
      {!done ? <Button variant="primary" size="lg" block disabled={!all} onClick={() => setDone(true)}>اكشف التعليق</Button> : (
        <Card as="section" aria-live="polite">
          <p><b>{right} من {lab.items.length}</b> وافقت تصنيف المختبر. الغرض هنا فهم الفكرة، والنتيجة لا تُحفظ ولا تدخل في ملفك.</p>
          <p>{lab.transfer_ar}</p>
          <p className="small dim">حدود المختبر: {lab.boundary_ar}</p>
          <Button variant="secondary" onClick={() => { setPick({}); setDone(false); }}>أعد المحاولة</Button>
        </Card>
      )}
    </div>
  );
}
