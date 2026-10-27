"use client";
import { useMemo, useState } from "react";
import { RIGHTS_LABEL } from "@/engine/knowledge-labels";

interface S { id: string; title: string; title_ar: string | null; authors: string[]; year: number | null; url: string | null; rights: string | null; grade: string | null }
export function SourceList({ items }: { items: S[] }) {
  const [q, setQ] = useState("");
  const [r, setR] = useState("all");
  const list = useMemo(() => items.filter((i) => (r === "all" || i.rights === r) && (!q.trim() || `${i.title} ${i.title_ar ?? ""} ${i.authors.join(" ")}`.toLowerCase().includes(q.trim().toLowerCase()))), [items, q, r]);
  return (
    <section className="stack">
      <div className="row">
        <label className="stack" style={{ gap: 4, flex: 1 }}><span className="small dim">بحث</span><input type="search" value={q} onChange={(e) => setQ(e.target.value)} /></label>
        <label className="stack" style={{ gap: 4 }}><span className="small dim">الحقوق</span>
          <select value={r} onChange={(e) => setR(e.target.value)}><option value="all">الكل</option>{Object.entries(RIGHTS_LABEL).map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select></label>
      </div>
      <p className="small dim" role="status">{list.length} مصدر</p>
      <ul className="stack" style={{ listStyle: "none", padding: 0 }}>
        {list.slice(0, 150).map((s) => (
          <li key={s.id} className="card small"><span lang="en" dir="ltr">{s.url ? <a href={s.url} target="_blank" rel="noopener noreferrer">{s.title}</a> : s.title}</span>
            {s.title_ar ? <> — {s.title_ar}</> : null}{s.year ? ` (${s.year})` : ""} · <span className="chip">{RIGHTS_LABEL[s.rights ?? "UNKNOWN"] ?? s.rights}</span> {s.grade ? <span className="chip">درجة الدليل {s.grade}</span> : null}</li>
        ))}
      </ul>
      {list.length > 150 && <p className="small dim">يُعرض أول ١٥٠؛ ضيّق البحث.</p>}
    </section>
  );
}
