"use client";
import { useState } from "react";
import type { Resp, View } from "./usePlay";

export function JournalTab({ view, busy, send, last }: { view: View; busy: boolean; send: (r: Record<string, unknown>) => Promise<Resp | null>; last: Resp["extra"] | null }) {
  const [t, setT] = useState("");
  return (
    <div className="stack">
      <h2>المفكرة</h2>
      <form onSubmit={(e) => { e.preventDefault(); if (t.trim()) { void send({ op: "note", text: t.trim() }); setT(""); } }}>
        <label htmlFor="jn">دوّن ملاحظة</label>
        <textarea id="jn" value={t} maxLength={1000} onChange={(e) => setT(e.target.value)} placeholder="ما الذي لفت نظرك؟ ما الذي لا ينسجم؟" />
        <button className="btn" disabled={busy || !t.trim()} style={{ marginBlockStart: 8 }}>احفظ</button>
      </form>
      {view.journal.length > 0 && <ul className="stack" style={{ listStyle: "none", padding: 0 }}>{[...view.journal].reverse().map((j) => <li key={j.seq} className="card">{j.text}</li>)}</ul>}
      <hr className="hr" />
      <h3>تلميحات</h3>
      <p className="small dim">التلميح يساعدك ولا يحلّ عنك. كل تلميح يخصم جزءاً صغيراً من نتيجتك المبدئية (لا يتجاوز ٢٠٪ في المجموع)، ولا حرج في استخدامه.</p>
      {view.hints_used.map((h) => <div key={h.hint_id} className="card"><span className="chip cyan">تلميح {h.level}</span><p style={{ margin: "8px 0 0" }}>{h.text_ar}</p></div>)}
      {view.machine === "investigating" && <button className="btn" disabled={busy} onClick={() => send({ op: "hint" })}>أعطني تلميحاً</button>}
      {last?.hint === null && <p className="small dim">لا تلميحات إضافية.</p>}
    </div>
  );
}
