"use client";
import { useState } from "react";
import type { LabOf } from "@/engine/labs";
import { Button } from "../ui/button";
import { Field } from "../ui/form";
import { LabEnd, parseNum } from "./common";

export function Measure({ lab }: { lab: LabOf<"measure"> }) {
  const [val, setVal] = useState<Record<string, string>>({});
  const [done, setDone] = useState(false);
  const parsed = (id: string) => parseNum(val[id] ?? "");
  const all = lab.tasks.every((t) => parsed(t.id) !== null);
  const ok = (t: (typeof lab.tasks)[number]) => { const v = parsed(t.id); return v !== null && Math.abs(v - t.answer) <= t.tolerance; };
  const right = lab.tasks.filter(ok).length;
  return (
    <div className="stack">
      <p className="card">{lab.setup_ar}</p>
      {lab.tasks.map((t) => {
        const v = parsed(t.id);
        const trap = !ok(t) && v !== null ? t.traps.find((x) => Math.abs(v - x.value) <= Math.max(t.tolerance, Math.abs(x.value) * 0.01)) : undefined;
        return (
          <div key={t.id} className="card" data-state={done ? (ok(t) ? "correct" : "wrong") : undefined}>
            <Field label={t.prompt_ar} hint={`الوحدة: ${t.unit_ar}. يمكنك كتابة الأرقام بالعربية أو اللاتينية.`}>
              {(p) => <input {...p} className="input input-ltr" inputMode="decimal" autoComplete="off" disabled={done} value={val[t.id] ?? ""} onChange={(e) => setVal({ ...val, [t.id]: e.target.value })} />}
            </Field>
            {done && (
              <p className="small" role="status">
                <b>{ok(t) ? "ضمن الهامش المقبول. " : trap ? `قريب من خطأ شائع: ${trap.note_ar} ` : `خارج الهامش. القيمة المرجعية ${t.answer} ${t.unit_ar} (± ${t.tolerance}). `}</b>
                {t.why_ar}
              </p>
            )}
          </div>
        );
      })}
      {!done ? <Button variant="primary" size="lg" block disabled={!all} onClick={() => setDone(true)}>تحقق من إجاباتي</Button>
        : <LabEnd lab={lab} onRetry={() => { setVal({}); setDone(false); }} summary={<><b>{right} من {lab.tasks.length}</b> ضمن الهامش المقبول.</>} />}
    </div>
  );
}
