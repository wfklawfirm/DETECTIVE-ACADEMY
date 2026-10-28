"use client";
import { useId, useMemo, useState } from "react";
import type { LabOf } from "@/engine/labs";
import { Button } from "../ui/button";
import { CardTitle } from "../ui/card";
import { ChoiceGroup } from "../ui/form";
import { LabEnd } from "./common";
import { evalExpr } from "./expr";

const fmt = (n: number, d: number) => n.toLocaleString("ar-EG", { minimumFractionDigits: d, maximumFractionDigits: d });

export function Slider({ lab }: { lab: LabOf<"slider"> }) {
  const uid = useId();
  const start = () => Object.fromEntries(lab.controls.map((c) => [c.id, c.value]));
  const [guess, setGuess] = useState<string | null>(null);
  const [locked, setLocked] = useState(false);
  const [vals, setVals] = useState<Record<string, number>>(start);
  const [done, setDone] = useState(false);
  const outs = useMemo(() => lab.outputs.map((o) => {
    let v = NaN; try { v = evalExpr(o.expr, vals); } catch { /* validated at load */ }
    return { o, v, read: o.read_ar?.find((b) => v <= b.max)?.text_ar ?? o.read_ar?.[o.read_ar.length - 1]?.text_ar };
  }), [lab, vals]);
  const ch = outs.find((x) => x.o.id === lab.challenge.output)!;
  const met = ch.v >= lab.challenge.min && ch.v <= lab.challenge.max;
  const guessOk = guess === lab.predict.answer;
  return (
    <div className="stack">
      <fieldset className="card" disabled={locked}>
        <legend className="text-label">أولاً: توقّع قبل أن تجرّب</legend>
        <p><b>{lab.predict.question_ar}</b></p>
        <ChoiceGroup label={lab.predict.question_ar} name={`${uid}-g`} value={guess} onChange={setGuess}
          states={done ? ({ [lab.predict.answer]: "correct", ...(guess && !guessOk ? { [guess]: "wrong" } : {}) } as Record<string, "correct" | "wrong">) : undefined}
          options={lab.predict.options.map((o) => ({ value: o.id, label: o.label_ar }))} />
        {!locked && <Button variant="primary" disabled={!guess} onClick={() => setLocked(true)}>ثبّت توقعي وافتح المنزلقات</Button>}
      </fieldset>

      {locked && (
        <section className="card" aria-label="النموذج">
          <CardTitle level={2}>ثانياً: جرّب النموذج</CardTitle>
          <p><b>التحدي: </b>{lab.challenge.prompt_ar}</p>
          {lab.controls.map((c) => (
            <div key={c.id} className="field">
              <label htmlFor={`${uid}-${c.id}`}>{c.label_ar}: <b dir="ltr">{fmt(vals[c.id]!, c.step < 1 ? 1 : 0)}</b> {c.unit_ar}</label>
              <input id={`${uid}-${c.id}`} type="range" min={c.min} max={c.max} step={c.step} value={vals[c.id]} disabled={done} onChange={(e) => setVals({ ...vals, [c.id]: Number(e.target.value) })} />
            </div>
          ))}
          <div className="lab-out" role="group" aria-label="النتائج الحية">
            {outs.map(({ o, v, read }) => (
              <p key={o.id}><span>{o.label_ar}: </span><output htmlFor={lab.controls.map((c) => `${uid}-${c.id}`).join(" ")}><b>{fmt(v, o.decimals)}</b> {o.unit_ar}</output>{read && <span className="small dim" style={{ display: "block" }}>{read}</span>}</p>
            ))}
          </div>
          <p className="small" aria-live="polite">{met ? "بلغتَ هدف التحدي." : `لم تبلغ الهدف بعد. تلميح: ${lab.challenge.hint_ar}`}</p>
          {!done && <Button variant="primary" size="lg" block onClick={() => setDone(true)}>اكشف الصيغة المخفية</Button>}
        </section>
      )}

      {done && (
        <section className="card" aria-label="الصيغة المخفية" role="status">
          <CardTitle level={2}>ما كان مخفياً</CardTitle>
          <p><b>{guessOk ? "توقعك صحيح. " : "توقعك لم يصب. "}</b>{lab.predict.why_ar}</p>
          <p><b>التحدي: </b>{met ? "نجحتَ فيه." : "لم تبلغه، وهذا مفيد: لاحظ أي منزلق كان الأثر الأكبر."}</p>
          <p className="lab-formula" dir="auto">{lab.reveal.formula_ar}</p>
          <ul className="stack-sm">{lab.reveal.points_ar.map((p) => <li key={p}>{p}</li>)}</ul>
        </section>
      )}
      {done && <LabEnd lab={lab} onRetry={() => { setGuess(null); setLocked(false); setVals(start()); setDone(false); }} summary={<>{guessOk ? "توقعك أصاب" : "توقعك لم يصب"}، و{met ? "بلغتَ هدف التحدي" : "لم تبلغ هدف التحدي"}.</>} />}
    </div>
  );
}
