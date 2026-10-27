"use client";
import Link from "next/link";
import { useMemo, useState } from "react";
import { CONF_LABEL, STATUS_LABEL, TYPE_LABEL } from "@/engine/knowledge-labels";
import type { Ko } from "@/engine/knowledge";

type Item = Pick<Ko, "ko_id" | "type" | "name_ar" | "summary_ar" | "confidence" | "status" | "tags">;
const TYPES: Ko["type"][] = ["forensic_concept", "reasoning_skill", "narrative_pattern"];
export function KnowledgeBrowser({ items }: { items: Item[] }) {
  const [t, setT] = useState<"all" | Ko["type"]>("all");
  const [s, setS] = useState("");
  const list = useMemo(() => {
    const needle = s.trim();
    return items.filter((i) => (t === "all" || i.type === t) && (!needle || i.name_ar.includes(needle) || i.summary_ar.includes(needle) || i.tags.some((x) => x.toLowerCase().includes(needle.toLowerCase()))));
  }, [items, t, s]);
  return (
    <div className="stack">
      <label className="stack" style={{ gap: 4 }}><span className="small dim">ابحث في الموسوعة</span>
        <input type="search" value={s} onChange={(e) => setS(e.target.value)} placeholder="مثلاً: بصمة، شاهد، ترتيب زمني" /></label>
      <div className="seg" role="group" aria-label="نوع المادة">
        <button aria-pressed={t === "all"} onClick={() => setT("all")}>الكل ({items.length})</button>
        {TYPES.map((x) => <button key={x} aria-pressed={t === x} onClick={() => setT(x)}>{TYPE_LABEL[x]} ({items.filter((i) => i.type === x).length})</button>)}
      </div>
      <p className="small dim" role="status">{list.length} مادة</p>
      <ul className="stack" style={{ listStyle: "none", padding: 0 }}>
        {list.slice(0, 120).map((i) => (
          <li key={i.ko_id} className="card stack" style={{ gap: 6 }}>
            <Link href={`/knowledge/${i.ko_id}`}><b>{i.name_ar}</b></Link>
            <p className="small" style={{ margin: 0 }}>{i.summary_ar.length > 190 ? i.summary_ar.slice(0, 190) + "…" : i.summary_ar}</p>
            <div className="row small dim"><span className="chip">{TYPE_LABEL[i.type]}</span><span className="chip">{CONF_LABEL[i.confidence]}</span><span className="chip">{STATUS_LABEL[i.status]}</span></div>
          </li>
        ))}
      </ul>
      {list.length > 120 && <p className="small dim">يُعرض أول ١٢٠ نتيجة؛ ضيّق البحث لرؤية الباقي.</p>}
    </div>
  );
}
