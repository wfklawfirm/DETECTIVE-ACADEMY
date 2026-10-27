"use client";
import type { View } from "./usePlay";

const KIND_AR: Record<string, string> = { physical: "مادي", documentary: "وثيقة", testimonial: "إفادة", digital: "رقمي", lab_result: "نتيجة مختبر", observation: "ملاحظة" };
const REL_AR: Record<string, string> = { strong: "موثوقية عالية", moderate: "موثوقية متوسطة", weak: "موثوقية ضعيفة" };
const DIGITAL = new Set(["digital", "lab_result"]);

export function EvidenceCard({ e, tag, onTag, disabled }: { e: View["evidence"][number]; tag?: string; onTag?: (cls: string) => void; disabled?: boolean }) {
  return (
    <article className={`paper ${DIGITAL.has(e.kind) ? "digital" : ""}`} aria-labelledby={`ev-${e.id}`}>
      <span className="stamp">{KIND_AR[e.kind] ?? e.kind}</span>
      <h3 id={`ev-${e.id}`}>{e.title_ar}</h3>
      <div style={{ whiteSpace: "pre-wrap" }}>{e.content_ar}</div>
      {e.media?.map((m) => <p key={m.uri} className="meta">[{m.alt_ar}]</p>)}
      <p className="meta" style={{ marginBlockStart: 12 }}><b>{REL_AR[e.reliability] ?? e.reliability}.</b> {e.limits_ar}</p>
      {onTag && (
        <div className="meta" style={{ marginBlockStart: 8 }}>
          <label htmlFor={`tag-${e.id}`} style={{ display: "inline", marginInlineEnd: 8, fontWeight: 600 }}>نوع المصدر:</label>
          <TagSelect id={`tag-${e.id}`} value={tag} onChange={onTag} disabled={disabled} />
        </div>
      )}
    </article>
  );
}

import { createContext, useContext } from "react";
export const ClassesCtx = createContext<View["source_classes"]>([]);

function TagSelect({ id, value, onChange, disabled }: { id: string; value?: string; onChange: (c: string) => void; disabled?: boolean }) {
  const classes = useContext(ClassesCtx);
  return (
    <select id={id} value={value ?? ""} disabled={disabled} onChange={(ev) => ev.target.value && onChange(ev.target.value)} style={{ minBlockSize: 40, inlineSize: "auto", background: "#fffaf0", color: "#222", borderColor: "#b5a67f" }}>
      <option value="">— صنّف —</option>
      {classes.map((c) => <option key={c.id} value={c.id}>{c.label_ar}</option>)}
    </select>
  );
}

export function EvidenceTab({ view, onTag, busy }: { view: View; onTag: (id: string, cls: string) => void; busy: boolean }) {
  const classes = view.source_classes;
  return (
    <ClassesCtx.Provider value={classes}>
      <div className="stack">
        <h2>خزانة الأدلة</h2>
        <p className="dim small">{view.evidence.length} دليلاً بين يديك{view.locked_evidence_count > 0 ? ` · ${view.locked_evidence_count} لم يُكشف بعد` : ""}. صنّف كل مصدر: التصنيف الدقيق يحمي استنتاجك.</p>
        <details className="card small"><summary>ما أنواع المصادر؟</summary>
          <ul>{classes.map((c) => <li key={c.id}><b>{c.label_ar}:</b> {c.help_ar}</li>)}</ul>
        </details>
        {view.evidence.length === 0 && <p>لا أدلة بعد. ارجع إلى «الملف» وابدأ بإجراء.</p>}
        <div className="grid cols-2">
          {view.evidence.map((e) => <EvidenceCard key={e.id} e={e} tag={view.source_tags[e.id]} onTag={(c) => onTag(e.id, c)} disabled={busy} />)}
        </div>
      </div>
    </ClassesCtx.Provider>
  );
}
