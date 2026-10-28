"use client";
import { useState } from "react";
import type { LabOf } from "@/engine/labs";
import { Button } from "../ui/button";
import { ChoiceGroup } from "../ui/form";
import { LabEnd } from "./common";

export function Classify({ lab }: { lab: LabOf<"classify"> }) {
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
      {!done ? <Button variant="primary" size="lg" block disabled={!all} onClick={() => setDone(true)}>اكشف التعليق</Button>
        : <LabEnd lab={lab} onRetry={() => { setPick({}); setDone(false); }} summary={<><b>{right} من {lab.items.length}</b> وافقت تصنيف المختبر.</>} />}
    </div>
  );
}
