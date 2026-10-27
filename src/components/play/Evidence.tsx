"use client";
import { createContext, useContext } from "react";
import { Callout } from "../ui/feedback";
import { LockIcon } from "../ui/icons";
import type { View } from "./usePlay";

const KIND_AR: Record<string, string> = { physical: "مادي", documentary: "وثيقة", testimonial: "إفادة", digital: "رقمي", lab_result: "نتيجة مختبر", observation: "ملاحظة" };
const REL_AR: Record<string, string> = { strong: "موثوقية عالية", moderate: "موثوقية متوسطة", weak: "موثوقية ضعيفة" };
const DIGITAL = new Set(["digital", "lab_result"]);
export const ClassesCtx = createContext<View["source_classes"]>([]);

export function EvidenceCard({ e, tag, onTag, disabled }: { e: View["evidence"][number]; tag?: string; onTag?: (cls: string) => void; disabled?: boolean }) {
  return (
    <article className={`paper ${DIGITAL.has(e.kind) ? "digital" : ""}`} aria-labelledby={`ev-${e.id}`}>
      <span className="paper-stamp">{KIND_AR[e.kind] ?? e.kind}</span>
      <h3 id={`ev-${e.id}`}>{e.title_ar}</h3>
      <div className="evbody">{e.content_ar}</div>
      {e.media?.map((m) => <p key={m.uri} className="meta">[{m.alt_ar}]</p>)}
      <p className="meta" style={{ marginBlockStart: 12 }}><b>{REL_AR[e.reliability] ?? e.reliability}.</b> {e.limits_ar}</p>
      {onTag && (
        <div className="meta stack-sm" style={{ marginBlockStart: 8 }}>
          <label htmlFor={`tag-${e.id}`} style={{ fontWeight: 600 }}>نوع المصدر</label>
          <TagSelect id={`tag-${e.id}`} value={tag} onChange={onTag} disabled={disabled} />
        </div>
      )}
    </article>
  );
}

function TagSelect({ id, value, onChange, disabled }: { id: string; value?: string; onChange: (c: string) => void; disabled?: boolean }) {
  const classes = useContext(ClassesCtx);
  return (
    <select id={id} value={value ?? ""} disabled={disabled} onChange={(ev) => ev.target.value && onChange(ev.target.value)}>
      <option value="">— صنّف —</option>
      {classes.map((c) => <option key={c.id} value={c.id}>{c.label_ar}</option>)}
    </select>
  );
}

/** Locked evidence is shown as redacted rows: the count is real, the content is not revealed. */
function Redacted({ n }: { n: number }) {
  const shown = Math.min(n, 4);
  return (
    <div className="stack-sm" role="group" aria-label={`${n} لم يُكشف بعد`}>
      {Array.from({ length: shown }, (_, i) => (
        <div key={i} className="redact-row" aria-hidden>
          <LockIcon size={20} className="ico" />
          <span className="lines"><span className="redact-bar" style={{ inlineSize: `${70 - (i % 3) * 14}%` }} /><span className="redact-bar" style={{ inlineSize: `${40 + (i % 2) * 18}%` }} /></span>
        </div>
      ))}
      <p className="small dim">{n > shown ? `و${n - shown} آخر ` : ""}لم يُكشف بعد: تظهر هذه الأدلة حين تسلك الطريق الذي يؤدي إليها.</p>
    </div>
  );
}

export function EvidenceTab({ view, onTag, busy }: { view: View; onTag: (id: string, cls: string) => void; busy: boolean }) {
  const classes = view.source_classes;
  return (
    <ClassesCtx.Provider value={classes}>
      <div className="stack">
        <h2 className="text-section-title">خزانة الأدلة</h2>
        <p className="dim small">{view.evidence.length} دليلاً بين يديك{view.locked_evidence_count > 0 ? ` · ${view.locked_evidence_count} لم يُكشف بعد` : ""}. صنّف كل مصدر: التصنيف الدقيق يحمي استنتاجك.</p>
        <details className="card small"><summary>ما أنواع المصادر؟</summary>
          <ul>{classes.map((c) => <li key={c.id}><b>{c.label_ar}:</b> {c.help_ar}</li>)}</ul>
        </details>
        {view.evidence.length === 0 && <Callout tone="info">لا أدلة بعد. ارجع إلى «الملف» وابدأ بإجراء.</Callout>}
        <div className="stack-lg">
          {view.evidence.map((e) => <EvidenceCard key={e.id} e={e} tag={view.source_tags[e.id]} onTag={(c) => onTag(e.id, c)} disabled={busy} />)}
        </div>
        {view.locked_evidence_count > 0 && <Redacted n={view.locked_evidence_count} />}
      </div>
    </ClassesCtx.Provider>
  );
}
