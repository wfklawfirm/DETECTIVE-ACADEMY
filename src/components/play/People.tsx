"use client";
import { useState } from "react";
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
        <h2>الشخصيات</h2>
        <p className="dim small">لكل شخص ما يعرفه وما يخفيه. الارتباك أو الصمت ليسا دليلاً بذاتهما.</p>
        <div className="grid cols-2">
          {view.characters.map((c) => (
            <button key={c.id} className="card" style={{ textAlign: "start", cursor: "pointer", font: "inherit", color: "inherit" }} onClick={() => setSel(c.id)}>
              <div className="row"><span className="avatar" aria-hidden>{c.glyph ?? c.name_ar.slice(0, 1)}</span><div><b>{c.name_ar}</b><br /><span className="small dim">{c.role_label}{c.age_descriptor_ar ? ` · ${c.age_descriptor_ar}` : ""}</span></div></div>
              <p className="small dim" style={{ marginBlockStart: 10, marginBottom: 0 }}>{c.persona_ar}</p>
              <p className="small" style={{ margin: "8px 0 0" }}>{c.interview_open ? (started(c.id) ? "المقابلة مفتوحة" : "يمكنك بدء المقابلة") : <span className="dim">لم تُفتح المقابلة بعد (ابحث عن طريق إليه في الملف)</span>}</p>
            </button>
          ))}
        </div>
      </div>
    );
  }
  const lines = view.transcript.filter((t) => t.char_id === ch.id);
  const hasEv = view.evidence;
  return (
    <div className="stack">
      <button className="btn ghost sm" onClick={() => setSel(null)}>← كل الشخصيات</button>
      <div className="row"><span className="avatar" aria-hidden>{ch.glyph ?? ch.name_ar.slice(0, 1)}</span><div><h2 style={{ margin: 0 }}>{ch.name_ar}</h2><span className="small dim">{ch.role_label} · بقي {ch.turns_left} أسئلة</span></div></div>
      <div className="chat" role="log" aria-live="polite" aria-label={`حوار مع ${ch.name_ar}`}>
        {lines.length === 0 && <p className="dim">لم تسأل بعد.</p>}
        {lines.map((t) => (
          <div key={t.seq} className="stack">
            <div className="bubble you"><span className="who">أنت</span>{t.topic_label ?? "سؤال حر"}</div>
            {t.lines.map((l, i) => <div key={i} className="bubble"><span className="who">{ch.name_ar}</span>{l.text_ar}</div>)}
            {t.lines.length === 0 && <div className="bubble dim"><span className="who">{ch.name_ar}</span>(لا يجيب عن هذا)</div>}
          </div>
        ))}
      </div>
      {!ch.interview_open ? <p className="card">لم تُفتح هذه المقابلة بعد.</p> : ch.turns_left <= 0 ? <p className="card">انتهت أسئلة هذه المقابلة.</p> : (
        <>
          <h3>اسأل عن…</h3>
          <div className="stack">
            {ch.topics.map((t) => (
              <button key={t.id} className="btn topic-btn" disabled={busy} onClick={() => send({ op: "ask", character_id: ch.id, topic_id: t.id })}>
                {t.label_ar}{t.asked ? " ✓" : ""}{t.examples_ar[0] && <small>مثال: {t.examples_ar[0]}</small>}
              </button>
            ))}
          </div>
          <form onSubmit={(e) => { e.preventDefault(); if (free.trim()) { void send({ op: "ask", character_id: ch.id, text: free.trim() }); setFree(""); } }}>
            <label htmlFor="free-q">أو اكتب سؤالك</label>
            <div className="field-row"><input id="free-q" value={free} maxLength={300} onChange={(e) => setFree(e.target.value)} placeholder="مثال: متى غادرت؟" style={{ flex: 1 }} /><button className="btn" disabled={busy || !free.trim()}>اسأل</button></div>
            <p className="small dim">الشخصيات تجيب بما كُتب لها فقط؛ لا يخترع النظام معلومات جديدة.</p>
          </form>
        </>
      )}
      {hasEv.length > 0 && ch.interview_open && (
        <div className="card stack">
          <h3>اعرض دليلاً</h3>
          <label htmlFor="pres">اختر دليلاً لتعرضه على {ch.name_ar}</label>
          <div className="field-row"><select id="pres" value={ev} onChange={(e) => setEv(e.target.value)} style={{ flex: 1 }}><option value="">— اختر —</option>{hasEv.map((e) => <option key={e.id} value={e.id}>{e.title_ar}</option>)}</select>
            <button className="btn" disabled={busy || !ev} onClick={() => send({ op: "present", evidence_id: ev, character_id: ch.id })}>اعرض</button></div>
        </div>
      )}
    </div>
  );
}
