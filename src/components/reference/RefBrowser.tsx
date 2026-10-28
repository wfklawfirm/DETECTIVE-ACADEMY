"use client";
import { useCallback, useEffect, useId, useMemo, useRef, useState, type ReactNode } from "react";
import { Button } from "../ui/button";
import { EmptyState } from "../ui/feedback";
import { Field } from "../ui/form";
import { SearchIcon } from "../ui/icons";

/** One filterable reference item. `node` is rendered on the server and handed over as-is; only the haystack text is used for search. */
export interface RefItem { id: string; text: string; facets: Record<string, string>; node: ReactNode }
export interface FacetDef { key: string; label: string; display: "chips" | "select"; options: { value: string; label: string }[]; allLabel?: string }

const AR_MARKS = /[ً-ْٰـ]/g;
/** Search-insensitive Arabic: no diacritics/tatweel, one alef, one ya, one ha. English folded to lower case. */
export function foldText(s: string): string {
  return s.replace(AR_MARKS, "").replace(/[أإآٱ]/g, "ا").replace(/ى/g, "ي").replace(/ة/g, "ه").toLowerCase();
}

export function RefBrowser({ items, facets = [], searchLabel, placeholder, noun, limit = 400 }: {
  items: RefItem[]; facets?: FacetDef[]; searchLabel: string; placeholder?: string; noun: string; limit?: number;
}) {
  const [q, setQ] = useState("");
  const [sel, setSel] = useState<Record<string, string>>({});
  const [target, setTarget] = useState<string | null>(null);
  const uid = useId();
  const refs = useRef<Map<string, HTMLLIElement>>(new Map());
  const folded = useMemo(() => items.map((i) => foldText(i.text)), [items]);

  const list = useMemo(() => {
    const needle = foldText(q.trim());
    return items.filter((it, idx) => (!needle || folded[idx]!.includes(needle)) && facets.every((f) => !sel[f.key] || it.facets[f.key] === sel[f.key]));
  }, [items, folded, q, sel, facets]);

  // Deep links (/glossary#GL-023): clear any filter that would hide the item, then scroll to it and mark it.
  const goTo = useCallback(() => {
    const id = decodeURIComponent(window.location.hash.replace(/^#/, ""));
    if (!id || !items.some((i) => i.id === id)) return;
    setQ(""); setSel({}); setTarget(id);
  }, [items]);
  useEffect(() => {
    goTo();
    window.addEventListener("hashchange", goTo);
    return () => window.removeEventListener("hashchange", goTo);
  }, [goTo]);
  useEffect(() => {
    if (!target) return;
    const t = window.setTimeout(() => { refs.current.get(target)?.scrollIntoView({ block: "start", behavior: "auto" }); }, 30);
    return () => window.clearTimeout(t);
  }, [target, list]);

  const shown = list.slice(0, limit);
  return (
    <div className="stack">
      <Field label={searchLabel}>{(p) => <input {...p} className="input" type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder={placeholder} autoComplete="off" />}</Field>
      {facets.map((f) => (
        <div key={f.key} className="stack-sm" role="group" aria-label={f.label}>
          <span className="text-label dim">{f.label}</span>
          {f.display === "select" ? (
            <select className="select" aria-label={f.label} value={sel[f.key] ?? ""} onChange={(e) => setSel((s) => ({ ...s, [f.key]: e.target.value }))}>
              <option value="">{f.allLabel ?? "الكل"}</option>
              {f.options.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
            </select>
          ) : (
            <div className="row" style={{ gap: "0.35rem" }}>
              <Button size="sm" variant={!sel[f.key] ? "primary" : "outline"} aria-pressed={!sel[f.key]} onClick={() => setSel((s) => ({ ...s, [f.key]: "" }))}>{f.allLabel ?? "الكل"}</Button>
              {f.options.map((o) => (
                <Button key={o.value} size="sm" variant={sel[f.key] === o.value ? "primary" : "outline"} aria-pressed={sel[f.key] === o.value}
                  onClick={() => setSel((s) => ({ ...s, [f.key]: s[f.key] === o.value ? "" : o.value }))}>{o.label}</Button>
              ))}
            </div>
          )}
        </div>
      ))}
      <p className="small dim" role="status" aria-live="polite" id={`${uid}-n`}><SearchIcon size={16} style={{ verticalAlign: "-3px" }} /> {list.length} {noun}</p>
      {list.length === 0 && <EmptyState title="لا نتائج" body="جرّب كلمة أخرى أو ألغِ أحد المرشِّحات." />}
      <ul className="list" aria-describedby={`${uid}-n`}>
        {shown.map((it) => (
          <li key={it.id} id={it.id} ref={(el) => { if (el) refs.current.set(it.id, el); else refs.current.delete(it.id); }}
            style={{ scrollMarginBlockStart: "calc(var(--header-height) + 0.75rem)", ...(target === it.id ? { outline: "2px solid var(--accent)", outlineOffset: "3px", borderRadius: "var(--radius-card)" } : null) }}>
            {it.node}
          </li>
        ))}
      </ul>
      {list.length > limit && <p className="small dim">يُعرض أول {limit} نتيجة؛ ضيّق البحث لرؤية الباقي.</p>}
    </div>
  );
}
