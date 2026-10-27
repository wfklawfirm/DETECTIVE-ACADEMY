"use client";
import { useState } from "react";
import { Badge } from "../ui/badge";
import { Button } from "../ui/button";
import { Card } from "../ui/card";
import { Field } from "../ui/form";
import type { Resp, View } from "./usePlay";

export function JournalTab({ view, busy, send, last }: { view: View; busy: boolean; send: (r: Record<string, unknown>) => Promise<Resp | null>; last: Resp["extra"] | null }) {
  const [t, setT] = useState("");
  return (
    <div className="stack-lg">
      <h2 className="text-section-title">المفكرة</h2>
      <form className="stack" onSubmit={(e) => { e.preventDefault(); if (t.trim()) { void send({ op: "note", text: t.trim() }); setT(""); } }}>
        <Field label="دوّن ملاحظة">{(p) => <textarea {...p} className="textarea" value={t} maxLength={1000} onChange={(e) => setT(e.target.value)} placeholder="ما الذي لفت نظرك؟ ما الذي لا ينسجم؟" />}</Field>
        <Button type="submit" variant="secondary" disabled={busy || !t.trim()}>احفظ</Button>
      </form>
      {view.journal.length > 0 && <ul className="list">{[...view.journal].reverse().map((j) => <li key={j.seq}><Card flat>{j.text}</Card></li>)}</ul>}
      <hr className="divider" />
      <section className="stack">
        <h3 className="text-section-title">تلميحات</h3>
        <p className="small dim">التلميح يساعدك ولا يحلّ عنك. كل تلميح يخصم جزءاً صغيراً من نتيجتك المبدئية (لا يتجاوز ٢٠٪ في المجموع)، ولا حرج في استخدامه.</p>
        {view.hints_used.map((h) => <Card key={h.hint_id} flat><Badge tone="info" style={{ alignSelf: "flex-start" }}>تلميح {h.level}</Badge><p>{h.text_ar}</p></Card>)}
        {view.machine === "investigating" && <Button variant="secondary" disabled={busy} onClick={() => send({ op: "hint" })}>أعطني تلميحاً</Button>}
        {last?.hint === null && <p className="small dim">لا تلميحات إضافية.</p>}
      </section>
    </div>
  );
}
