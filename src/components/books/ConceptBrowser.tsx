"use client";
import { useId, useMemo, useState } from "react";
import { AGE_LABEL, SAFETY_LABEL, SKILLS, SKILL_LABEL, type BookConceptView, type Skill } from "@/engine/books-labels";
import { Badge } from "../ui/badge";
import { CardLink } from "../ui/card";
import { EmptyState } from "../ui/feedback";
import { Field, SegmentedControl } from "../ui/form";
import { SearchIcon } from "../ui/icons";

export function ConceptBrowser({ items }: { items: BookConceptView[] }) {
  const [skill, setSkill] = useState<"all" | Skill>("all");
  const [age, setAge] = useState<"all" | "teen" | "adult">("all");
  const [q, setQ] = useState("");
  const n1 = useId(), n2 = useId();
  const list = useMemo(() => {
    const needle = q.trim();
    return items.filter((i) =>
      (skill === "all" || i.skill === skill) &&
      (age === "all" || (age === "teen" ? i.age_band !== "18+" : i.age_band === "18+")) &&
      (!needle || i.title_ar.includes(needle) || i.summary_ar.includes(needle)));
  }, [items, skill, age, q]);
  return (
    <div className="stack">
      <Field label="ابحث في المفاهيم">{(p) => <input {...p} className="input" type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder="مثلاً: سلسلة الحيازة، شاهد، توقيت" />}</Field>
      <SegmentedControl label="المهارة" name={n1} value={skill} onChange={(v) => setSkill(v as typeof skill)}
        options={[{ value: "all", label: `الكل (${items.length})` }, ...SKILLS.map((s) => ({ value: s, label: `${SKILL_LABEL[s]} (${items.filter((i) => i.skill === s).length})` }))]} />
      {items.some((i) => i.age_band === "18+") && (
        <SegmentedControl label="الفئة العمرية" name={n2} value={age} onChange={(v) => setAge(v as typeof age)}
          options={[{ value: "all", label: "كل الأعمار" }, { value: "teen", label: "دون ١٨" }, { value: "adult", label: "١٨ فأكثر" }]} />
      )}
      <p className="small dim" role="status"><SearchIcon size={16} style={{ verticalAlign: "-3px" }} /> {list.length} مفهوم</p>
      {list.length === 0 && <EmptyState title="لا نتائج" body="جرّب كلمة أخرى أو مهارة أخرى." />}
      <ul className="list">
        {list.slice(0, 100).map((i) => (
          <li key={i.id}>
            <CardLink href={`/books/concept/${i.id}`} className="kb-result">
              <b>{i.title_ar}</b>
              <p className="small dim-2">{i.summary_ar.length > 170 ? i.summary_ar.slice(0, 170) + "…" : i.summary_ar}</p>
              <span className="row small"><Badge>{SKILL_LABEL[i.skill]}</Badge><Badge outline>{AGE_LABEL[i.age_band]}</Badge>{i.safety_level !== "safe" && <Badge outline>{SAFETY_LABEL[i.safety_level]}</Badge>}</span>
            </CardLink>
          </li>
        ))}
      </ul>
      {list.length > 100 && <p className="small dim">يُعرض أول ١٠٠ نتيجة؛ ضيّق البحث لرؤية الباقي.</p>}
    </div>
  );
}
