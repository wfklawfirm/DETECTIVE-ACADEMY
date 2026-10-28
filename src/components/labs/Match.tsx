"use client";
import { useId, useState } from "react";
import type { LabOf } from "@/engine/labs";
import { Button } from "../ui/button";
import { LabEnd } from "./common";

export function Match({ lab }: { lab: LabOf<"match"> }) {
  const uid = useId();
  const [pick, setPick] = useState<Record<string, string>>({});
  const [done, setDone] = useState(false);
  const all = lab.pairs.every((p) => pick[p.id]);
  const right = lab.pairs.filter((p) => pick[p.id] === p.answer).length;
  const label = (id: string) => lab.options.find((o) => o.id === id)?.label_ar;
  return (
    <div className="stack">
      {lab.pairs.map((p) => {
        const ok = pick[p.id] === p.answer;
        return (
          <div key={p.id} className="card" data-state={done ? (ok ? "correct" : "wrong") : undefined}>
            <label htmlFor={`${uid}-${p.id}`}>{p.text_ar}</label>
            <select id={`${uid}-${p.id}`} className="select" disabled={done} value={pick[p.id] ?? ""} onChange={(e) => setPick({ ...pick, [p.id]: e.target.value })}>
              <option value="">اختر ما يطابقه…</option>
              {lab.options.map((o) => <option key={o.id} value={o.id}>{o.label_ar}</option>)}
            </select>
            {done && <p className="small" role="status"><b>{ok ? "أصبت. " : `الأقرب: «${label(p.answer)}». `}</b>{p.why_ar}</p>}
          </div>
        );
      })}
      {!done ? <Button variant="primary" size="lg" block disabled={!all} onClick={() => setDone(true)}>اكشف التعليق</Button>
        : <LabEnd lab={lab} onRetry={() => { setPick({}); setDone(false); }} summary={<><b>{right} من {lab.pairs.length}</b> أزواج صحيحة.</>} />}
    </div>
  );
}
