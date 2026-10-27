"use client";
import { useId, useMemo, useState } from "react";
import { CONF_LABEL, STATUS_LABEL, TYPE_LABEL } from "@/engine/knowledge-labels";
import type { Ko } from "@/engine/knowledge";
import { Badge } from "./ui/badge";
import { CardLink } from "./ui/card";
import { EmptyState } from "./ui/feedback";
import { Field, SegmentedControl } from "./ui/form";
import { SearchIcon } from "./ui/icons";

type Item = Pick<Ko, "ko_id" | "type" | "name_ar" | "summary_ar" | "confidence" | "status" | "tags">;
const TYPES: Ko["type"][] = ["forensic_concept", "reasoning_skill", "narrative_pattern"];
export function KnowledgeBrowser({ items }: { items: Item[] }) {
  const [t, setT] = useState<"all" | Ko["type"]>("all");
  const [s, setS] = useState("");
  const name = useId();
  const list = useMemo(() => {
    const needle = s.trim();
    return items.filter((i) => (t === "all" || i.type === t) && (!needle || i.name_ar.includes(needle) || i.summary_ar.includes(needle) || i.tags.some((x) => x.toLowerCase().includes(needle.toLowerCase()))));
  }, [items, t, s]);
  return (
    <div className="stack">
      <Field label="ابحث في الموسوعة">{(p) => <input {...p} className="input" type="search" value={s} onChange={(e) => setS(e.target.value)} placeholder="مثلاً: بصمة، شاهد، ترتيب زمني" />}</Field>
      <SegmentedControl label="نوع المادة" name={name} value={t} onChange={(v) => setT(v as typeof t)}
        options={[{ value: "all", label: `الكل (${items.length})` }, ...TYPES.map((x) => ({ value: x, label: `${TYPE_LABEL[x]} (${items.filter((i) => i.type === x).length})` }))]} />
      <p className="small dim" role="status"><SearchIcon size={16} style={{ verticalAlign: "-3px" }} /> {list.length} مادة</p>
      {list.length === 0 && <EmptyState title="لا نتائج" body="جرّب كلمة أخرى أو نوعاً آخر." />}
      <ul className="list">
        {list.slice(0, 120).map((i) => (
          <li key={i.ko_id}>
            <CardLink href={`/knowledge/${i.ko_id}`} className="kb-result">
              <b>{i.name_ar}</b>
              <p className="small dim-2">{i.summary_ar.length > 190 ? i.summary_ar.slice(0, 190) + "…" : i.summary_ar}</p>
              <span className="row small"><Badge>{TYPE_LABEL[i.type]}</Badge><Badge outline>{CONF_LABEL[i.confidence]}</Badge><Badge outline>{STATUS_LABEL[i.status]}</Badge></span>
            </CardLink>
          </li>
        ))}
      </ul>
      {list.length > 120 && <p className="small dim">يُعرض أول ١٢٠ نتيجة؛ ضيّق البحث لرؤية الباقي.</p>}
    </div>
  );
}
