"use client";
import { useState } from "react";
import type { Lab } from "@/engine/labs";

export function LabRunner({ lab }: { lab: Lab }) {
  const [pick, setPick] = useState<Record<string, string>>({});
  const [done, setDone] = useState(false);
  const all = lab.items.every((i) => pick[i.id]);
  const right = lab.items.filter((i) => pick[i.id] === i.answer).length;
  return (
    <div className="stack">
      {lab.items.map((it) => {
        const mine = pick[it.id];
        return (
          <fieldset key={it.id} className="card stack" disabled={done} style={{ margin: 0 }}>
            <legend className="small dim">معلومة</legend>
            <p style={{ margin: 0 }}>{it.text_ar}</p>
            <div className="seg" role="radiogroup" aria-label={it.text_ar} style={{ flexWrap: "wrap", borderRadius: 16 }}>
              {lab.categories.map((c) => <button key={c.id} role="radio" aria-checked={mine === c.id} onClick={() => setPick({ ...pick, [it.id]: c.id })}>{c.label_ar}</button>)}
            </div>
            {done && <p className="small" role="status" style={{ margin: 0 }}><b>{mine === it.answer ? "أصبت. " : `الأقرب: «${lab.categories.find((c) => c.id === it.answer)?.label_ar}». `}</b>{it.why_ar}</p>}
          </fieldset>
        );
      })}
      {!done ? <button className="btn primary" disabled={!all} onClick={() => setDone(true)}>اكشف التعليق</button> : (
        <section className="card stack" aria-live="polite">
          <p style={{ margin: 0 }}><b>{right} من {lab.items.length}</b> وافقت تصنيف المختبر. الغرض هنا فهم الفكرة، والنتيجة لا تُحفظ ولا تدخل في ملفك.</p>
          <p style={{ margin: 0 }}>{lab.transfer_ar}</p>
          <p className="small dim" style={{ margin: 0 }}>حدود المختبر: {lab.boundary_ar}</p>
          <button className="btn" onClick={() => { setPick({}); setDone(false); }}>أعد المحاولة</button>
        </section>
      )}
    </div>
  );
}
