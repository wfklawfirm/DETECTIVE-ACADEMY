"use client";
import { useState } from "react";
import type { LabOf } from "@/engine/labs";
import { Button } from "../ui/button";
import { LabEnd, shuffled } from "./common";

export function Order({ lab }: { lab: LabOf<"order"> }) {
  const init = () => shuffled(lab.steps.map((s) => s.id), lab.id).map((x) => x);
  const [seq, setSeq] = useState<string[]>(init);
  const [done, setDone] = useState(false);
  const [note, setNote] = useState("");
  const by = Object.fromEntries(lab.steps.map((s, i) => [s.id, { ...s, pos: i }]));
  const move = (i: number, d: -1 | 1) => {
    const j = i + d; if (j < 0 || j >= seq.length) return;
    const n = [...seq]; [n[i], n[j]] = [n[j]!, n[i]!]; setSeq(n);
    setNote(`نُقلت «${by[n[j]!]!.text_ar}» إلى المرتبة ${j + 1} من ${n.length}`);
  };
  const right = seq.filter((id, i) => by[id]!.pos === i).length;
  return (
    <div className="stack">
      <p className="small dim">{lab.goal_ar} استعمل زرّي «أعلى» و«أسفل» لتحريك كل خطوة.</p>
      <ol className="lab-order" aria-label="الخطوات">
        {seq.map((id, i) => {
          const s = by[id]!; const ok = s.pos === i;
          return (
            <li key={id} className="lab-step" data-state={done ? (ok ? "correct" : "wrong") : undefined}>
              <span className="lab-step-n" aria-hidden>{i + 1}</span>
              <span className="lab-step-t">{s.text_ar}
                {done && <span className="small" style={{ display: "block" }}><b>{ok ? "في مكانها. " : `مكانها الصحيح: ${s.pos + 1}. `}</b>{s.why_ar}</span>}
              </span>
              {!done && (
                <span className="lab-step-b">
                  <Button size="sm" variant="outline" disabled={i === 0} aria-label={`حرّك «${s.text_ar}» إلى أعلى`} onClick={() => move(i, -1)}>أعلى</Button>
                  <Button size="sm" variant="outline" disabled={i === seq.length - 1} aria-label={`حرّك «${s.text_ar}» إلى أسفل`} onClick={() => move(i, 1)}>أسفل</Button>
                </span>
              )}
            </li>
          );
        })}
      </ol>
      <p className="sr-only" role="status">{note}</p>
      {!done ? <Button variant="primary" size="lg" block onClick={() => setDone(true)}>تحقق من الترتيب</Button>
        : <LabEnd lab={lab} onRetry={() => { setSeq(init()); setDone(false); setNote(""); }} summary={<><b>{right} من {seq.length}</b> في موضعها الصحيح.</>} />}
    </div>
  );
}
