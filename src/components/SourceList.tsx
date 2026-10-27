"use client";
import { useMemo, useState } from "react";
import { RIGHTS_LABEL } from "@/engine/knowledge-labels";
import { Badge } from "./ui/badge";
import { Card } from "./ui/card";
import { Field } from "./ui/form";

interface S { id: string; title: string; title_ar: string | null; authors: string[]; year: number | null; url: string | null; rights: string | null; grade: string | null }
export function SourceList({ items }: { items: S[] }) {
  const [q, setQ] = useState("");
  const [r, setR] = useState("all");
  const list = useMemo(() => items.filter((i) => (r === "all" || i.rights === r) && (!q.trim() || `${i.title} ${i.title_ar ?? ""} ${i.authors.join(" ")}`.toLowerCase().includes(q.trim().toLowerCase()))), [items, q, r]);
  return (
    <section className="stack">
      <div className="grid-2">
        <Field label="بحث">{(p) => <input {...p} className="input" type="search" value={q} onChange={(e) => setQ(e.target.value)} />}</Field>
        <Field label="الحقوق">{(p) => <select {...p} value={r} onChange={(e) => setR(e.target.value)}><option value="all">الكل</option>{Object.entries(RIGHTS_LABEL).map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select>}</Field>
      </div>
      <p className="small dim" role="status">{list.length} مصدر</p>
      <ul className="list">
        {list.slice(0, 150).map((s) => (
          <li key={s.id}><Card flat className="small">
            <span lang="en" dir="ltr" style={{ textAlign: "start" }}>{s.url ? <a href={s.url} target="_blank" rel="noopener noreferrer">{s.title}</a> : s.title}</span>
            <span>{s.title_ar ? <>{s.title_ar}</> : null}{s.year ? ` (${s.year})` : ""}</span>
            <span className="row"><Badge>{RIGHTS_LABEL[s.rights ?? "UNKNOWN"] ?? s.rights}</Badge>{s.grade ? <Badge outline>درجة الدليل {s.grade}</Badge> : null}</span></Card></li>
        ))}
      </ul>
      {list.length > 150 && <p className="small dim">يُعرض أول ١٥٠؛ ضيّق البحث.</p>}
    </section>
  );
}
