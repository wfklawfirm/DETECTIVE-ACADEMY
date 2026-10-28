"use client";
import { useState } from "react";
import type { LabOf } from "@/engine/labs";
import { Button } from "../ui/button";
import { CardTitle } from "../ui/card";
import { LabEnd } from "./common";

export function Spot({ lab }: { lab: LabOf<"spot"> }) {
  const [marked, setMarked] = useState<Set<string>>(new Set());
  const [done, setDone] = useState(false);
  const flaws = lab.lines.filter((l) => l.flaw);
  const found = flaws.filter((l) => marked.has(l.id)).length;
  const false_ = lab.lines.filter((l) => !l.flaw && marked.has(l.id)).length;
  const toggle = (id: string) => { const n = new Set(marked); if (n.has(id)) n.delete(id); else n.add(id); setMarked(n); };
  return (
    <div className="stack">
      <p className="small dim">{lab.task_ar} المس السطر لتعليمه، والمسه ثانية لإلغاء العلامة.</p>
      <section className="card lab-doc" aria-label={lab.doc_title_ar}>
        <CardTitle level={2}>{lab.doc_title_ar}</CardTitle>
        <ul className="list">
          {lab.lines.map((l) => {
            const on = marked.has(l.id);
            const state = done ? (l.flaw ? (on ? "correct" : "wrong") : on ? "wrong" : undefined) : undefined;
            return (
              <li key={l.id}>
                <button type="button" className="lab-line" aria-pressed={on} disabled={done} data-state={state} onClick={() => toggle(l.id)}>
                  <span className="lab-line-mark" aria-hidden>{on ? "⚑" : ""}</span>
                  <span>{l.text_ar}</span>
                </button>
                {done && (l.flaw
                  ? <p className="small" role="status"><b>{on ? "رصدتَ الخلل: " : "فاتك هذا الخلل: "}{l.flaw.label_ar}. </b>{l.flaw.why_ar}</p>
                  : on ? <p className="small" role="status"><b>علّمتَ سطراً سليماً. </b>{l.ok_ar ?? "هذا السطر لا خلل فيه بذاته؛ الحذر من الشك في كل شيء جزء من المهارة."}</p> : null)}
              </li>
            );
          })}
        </ul>
      </section>
      <p className="small" aria-live="polite">علّمتَ {marked.size} سطراً.</p>
      {!done ? <Button variant="primary" size="lg" block onClick={() => setDone(true)}>اكشف الأخطاء</Button>
        : <LabEnd lab={lab} onRetry={() => { setMarked(new Set()); setDone(false); }} summary={<>رصدتَ <b>{found} من {flaws.length}</b> {flaws.length === 1 ? "خللاً" : "أخلال"}، وعلّمتَ {false_} {false_ === 1 ? "سطراً سليماً" : "أسطر سليمة"} بالخطأ.</>} />}
    </div>
  );
}
