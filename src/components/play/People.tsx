"use client";
import { useState } from "react";
import { Badge } from "../ui/badge";
import { Button } from "../ui/button";
import { Callout } from "../ui/feedback";
import { Field } from "../ui/form";
import { BackIcon, ChevronIcon, CheckIcon } from "../ui/icons";
import type { View } from "./usePlay";

export function PeopleTab({ view, busy, send, initial }: { initial?: string | null; view: View; busy: boolean; send: (r: Record<string, unknown>) => Promise<unknown> }) {
  const [sel, setSel] = useState<string | null>(initial ?? null);
  const [free, setFree] = useState("");
  const [ev, setEv] = useState("");
  const ch = view.characters.find((c) => c.id === sel);
  const started = (id: string) => view.transcript.some((t) => t.char_id === id);
  if (!ch) {
    return (
      <div className="stack">
        <h2 className="text-section-title">الشخصيات</h2>
        <p className="dim small">لكل شخص ما يعرفه وما يخفيه. الارتباك أو الصمت ليسا دليلاً بذاتهما.</p>
        <ul className="list">
          {view.characters.map((c) => (
            <li key={c.id}>
              <button className="card card-link person" onClick={() => setSel(c.id)}>
                <span className="row" style={{ flexWrap: "nowrap" }}>
                  <span className="avatar" aria-hidden>{c.glyph ?? c.name_ar.slice(0, 1)}</span>
                  <span className="grow"><b>{c.name_ar}</b><br /><span className="small dim">{c.role_label}{c.age_descriptor_ar ? ` · ${c.age_descriptor_ar}` : ""}</span></span>
                  <ChevronIcon className="chev" size={20} />
                </span>
                <span className="small dim-2">{c.persona_ar}</span>
                <span className="small">{c.interview_open ? <Badge tone={started(c.id) ? "brand" : "neutral"}>{started(c.id) ? "المقابلة مفتوحة" : "يمكنك بدء المقابلة"}</Badge> : <span className="dim">لم تُفتح المقابلة بعد (ابحث عن طريق إليه في الملف)</span>}</span>
              </button>
            </li>
          ))}
        </ul>
      </div>
    );
  }
  const lines = view.transcript.filter((t) => t.char_id === ch.id);
  const hasEv = view.evidence;
  return (
    <div className="stack">
      <Button variant="ghost" size="sm" onClick={() => setSel(null)} style={{ alignSelf: "flex-start" }}><BackIcon size={20} />كل الشخصيات</Button>
      <div className="row" style={{ flexWrap: "nowrap" }}><span className="avatar" aria-hidden>{ch.glyph ?? ch.name_ar.slice(0, 1)}</span><div><h2 className="text-section-title">{ch.name_ar}</h2><span className="small dim">{ch.role_label} · بقي {ch.turns_left} أسئلة</span></div></div>
      <div className="chat" role="log" aria-live="polite" aria-label={`حوار مع ${ch.name_ar}`}>
        {lines.length === 0 && <p className="dim">لم تسأل بعد.</p>}
        {lines.map((t) => (
          <div key={t.seq} className="stack-sm">
            <div className="bubble you"><span className="who">أنت</span>{t.topic_label ?? "سؤال حر"}</div>
            {t.lines.map((l, i) => <div key={i} className="bubble"><span className="who">{ch.name_ar}</span>{l.text_ar}</div>)}
            {t.lines.length === 0 && <div className="bubble dim"><span className="who">{ch.name_ar}</span>(لا يجيب عن هذا)</div>}
          </div>
        ))}
      </div>
      {!ch.interview_open ? <Callout tone="info">لم تُفتح هذه المقابلة بعد.</Callout> : ch.turns_left <= 0 ? <Callout tone="info">انتهت أسئلة هذه المقابلة.</Callout> : (
        <>
          <h3 className="text-section-title">اسأل عن…</h3>
          <div className="stack-sm">
            {ch.topics.map((t) => (
              <Button key={t.id} variant="secondary" block className="topic-btn" disabled={busy} onClick={() => send({ op: "ask", character_id: ch.id, topic_id: t.id })}>
                <span>{t.label_ar}{t.examples_ar[0] && <small>مثال: {t.examples_ar[0]}</small>}</span>{t.asked && <CheckIcon size={20} aria-label="سُئل" />}
              </Button>
            ))}
          </div>
          <form className="stack-sm" onSubmit={(e) => { e.preventDefault(); if (free.trim()) { void send({ op: "ask", character_id: ch.id, text: free.trim() }); setFree(""); } }}>
            <Field label="أو اكتب سؤالك" hint="الشخصيات تجيب بما كُتب لها فقط؛ لا يخترع النظام معلومات جديدة.">{(p) => (
              <div className="row" style={{ flexWrap: "nowrap" }}><input {...p} className="input" value={free} maxLength={300} onChange={(e) => setFree(e.target.value)} placeholder="مثال: متى غادرت؟" /><Button type="submit" variant="secondary" className="btn-nowrap" disabled={busy || !free.trim()}>اسأل</Button></div>
            )}</Field>
          </form>
        </>
      )}
      {hasEv.length > 0 && ch.interview_open && (
        <div className="card">
          <h3 className="card-title">اعرض دليلاً</h3>
          <Field label={`اختر دليلاً لتعرضه على ${ch.name_ar}`}>{(p) => (
            <div className="row" style={{ flexWrap: "nowrap" }}><select {...p} value={ev} onChange={(e) => setEv(e.target.value)}><option value="">— اختر —</option>{hasEv.map((e) => <option key={e.id} value={e.id}>{e.title_ar}</option>)}</select>
              <Button variant="secondary" className="btn-nowrap" disabled={busy || !ev} onClick={() => send({ op: "present", evidence_id: ev, character_id: ch.id })}>اعرض</Button></div>
          )}</Field>
        </div>
      )}
    </div>
  );
}
