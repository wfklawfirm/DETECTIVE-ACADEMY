"use client";
import { useState } from "react";
import type { LabOf } from "@/engine/labs";
import { Button } from "../ui/button";
import { ChoiceGroup } from "../ui/form";
import { LabEnd } from "./common";

const VERDICT: Record<string, string> = { best: "استنتاج مسوَّغ", overreach: "مبالغة: يتجاوز ما تدعمه المعطيات", too_weak: "تحفّظ زائد: يهمل ما تدعمه المعطيات", off_topic: "لا يجيب عن السؤال المطروح" };

export function Conclude({ lab }: { lab: LabOf<"conclude"> }) {
  const [pick, setPick] = useState<Record<string, string>>({});
  const [done, setDone] = useState(false);
  const all = lab.scenarios.every((s) => pick[s.id]);
  const best = (s: (typeof lab.scenarios)[number]) => s.options.find((o) => o.verdict === "best")!;
  const right = lab.scenarios.filter((s) => pick[s.id] === best(s).id).length;
  return (
    <div className="stack">
      {lab.scenarios.map((s) => {
        const mine = s.options.find((o) => o.id === pick[s.id]);
        const states = done ? ({ [best(s).id]: "correct", ...(mine && mine.verdict !== "best" ? { [mine.id]: "wrong" } : {}) } as Record<string, "correct" | "wrong">) : undefined;
        return (
          <fieldset key={s.id} className="card" disabled={done}>
            <legend className="text-label">معطيات</legend>
            <p>{s.facts_ar}</p>
            <p><b>{s.question_ar}</b></p>
            <ChoiceGroup label={s.question_ar} name={`lab-${s.id}`} value={mine?.id ?? null} states={states} onChange={(v) => setPick({ ...pick, [s.id]: v })} options={s.options.map((o) => ({ value: o.id, label: o.text_ar }))} />
            {done && mine && (
              <div className="stack-sm" role="status">
                <p className="small"><b>اختيارك: {VERDICT[mine.verdict]}. </b>{mine.why_ar}</p>
                {mine.verdict !== "best" && <p className="small"><b>الأقرب: «{best(s).text_ar}». </b>{best(s).why_ar}</p>}
              </div>
            )}
          </fieldset>
        );
      })}
      {!done ? <Button variant="primary" size="lg" block disabled={!all} onClick={() => setDone(true)}>اكشف التعليق</Button>
        : <LabEnd lab={lab} onRetry={() => { setPick({}); setDone(false); }} summary={<><b>{right} من {lab.scenarios.length}</b> اخترتَ فيها الاستنتاج المسوَّغ.</>} />}
    </div>
  );
}
