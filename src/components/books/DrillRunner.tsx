"use client";
import { useMemo, useState } from "react";
import { SKILLS, SKILL_LABEL, type Skill } from "@/engine/books-labels";
import { Button } from "../ui/button";
import { Card, CardTitle } from "../ui/card";
import { Callout } from "../ui/feedback";
import { ChoiceGroup, SegmentedControl } from "../ui/form";

export type DrillView = { id: string; skill: Skill; scenario_ar: string; question_ar: string; options: { id: string; text_ar: string }[]; answer_id: string; explanation_ar: string };

export function DrillRunner({ drills }: { drills: DrillView[] }) {
  const [skill, setSkill] = useState<"all" | Skill>("all");
  const [round, setRound] = useState(0);
  const [i, setI] = useState(0);
  const [sel, setSel] = useState<string | null>(null);
  const [score, setScore] = useState(0);
  const list = useMemo(() => {
    const base = drills.filter((d) => skill === "all" || d.skill === skill);
    // retries start from a different question so repeating is not rote
    const o = base.length ? (round * 7) % base.length : 0;
    return [...base.slice(o), ...base.slice(0, o)];
  }, [drills, skill, round]);
  const reset = (s?: "all" | Skill) => { if (s !== undefined) setSkill(s); setI(0); setSel(null); setScore(0); setRound((r) => r + 1); };
  const finished = i >= list.length;
  const d = list[i];
  const done = sel !== null && !!d;
  const states: Record<string, "correct" | "wrong"> | undefined = done ? { [d.answer_id]: "correct", ...(sel !== d.answer_id ? { [sel!]: "wrong" as const } : {}) } : undefined;
  return (
    <div className="stack">
      <SegmentedControl label="المهارة" name="drill-skill" value={skill} onChange={(v) => reset(v as typeof skill)}
        options={[{ value: "all", label: "الكل" }, ...SKILLS.map((s) => ({ value: s, label: SKILL_LABEL[s] }))]} />
      {finished || !d ? (
        <Card as="section">
          <CardTitle level={2}>انتهت الجولة</CardTitle>
          <p role="status">نتيجتك: {score} من {list.length}</p>
          <p className="small dim">الهدف ليس الدرجة؛ راجع تفسير كل سؤال أخطأت فيه، ثم أعد المحاولة بترتيب مختلف.</p>
          <Button onClick={() => reset()}>أعد الجولة</Button>
        </Card>
      ) : (
        <Card as="section" aria-labelledby="dr-q">
          <p className="small dim">سؤال {i + 1} من {list.length} · {SKILL_LABEL[d.skill]} · النتيجة {score}</p>
          <p className="narrative">{d.scenario_ar}</p>
          <CardTitle id="dr-q" level={2}>{d.question_ar}</CardTitle>
          <ChoiceGroup labelledBy="dr-q" name={`drill-${d.id}`} value={sel} disabled={done} states={states}
            onChange={(v) => { setSel(v); if (v === d.answer_id) setScore((s) => s + 1); }}
            options={d.options.map((o) => ({ value: o.id, label: o.text_ar }))} />
          {done && (
            <div role="status" className="stack-sm">
              <Callout tone={sel === d.answer_id ? "positive" : "negative"}>{sel === d.answer_id ? "إجابة صحيحة." : "ليست الإجابة الأدق."}</Callout>
              <p>{d.explanation_ar}</p>
              <Button onClick={() => { setI(i + 1); setSel(null); }}>{i + 1 >= list.length ? "اعرض النتيجة" : "السؤال التالي"}</Button>
            </div>
          )}
        </Card>
      )}
    </div>
  );
}
