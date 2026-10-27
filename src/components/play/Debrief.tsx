"use client";
import Link from "next/link";
import { useState } from "react";
import type { Resp } from "./usePlay";
import { useMe } from "../Shell";

export function Debrief({ r, busy, send }: { r: Resp; busy: boolean; send: (x: Record<string, unknown>) => Promise<unknown> }) {
  const v = r.view; const a = r.assessment; const d = v.debrief;
  const { me } = useMe();
  const [picked, setPicked] = useState<string[]>([]);
  const [ft, setFt] = useState("");
  const concl = v.hypotheses.find((h) => h.id === v.submission?.conclusion_hypothesis_id);
  if (!a || !d) return <p>جارٍ تحميل الملخص…</p>;
  const evT = (id: string) => v.evidence.find((e) => e.id === id)?.title_ar ?? id;
  const tt = v.transfer_task;
  return (
    <div className="wrap-narrow stack">
      <p className="kicker">إغلاق الملف</p>
      <h1>{v.title_ar}</h1>
      <section className="card stack" aria-labelledby="sol-h"><h2 id="sol-h">ما الذي حدث فعلاً؟</h2>
        <p style={{ fontFamily: "var(--f-display)", fontSize: "1.25rem" }}>{d.solution_summary_ar}</p>
        {concl && <p className="small dim">استنتاجك كان: «{concl.statement_ar}» بترجيح {v.submission?.confidence}٪.</p>}
      </section>
      <section className="card stack" aria-labelledby="sc-h"><h2 id="sc-h">قراءة أداءك (مبدئية)</h2>
        <p className="small dim">{a.disclaimer_ar}</p>
        <div className="row"><span className="mono" style={{ fontSize: "2.4rem" }}>{a.total_pct ?? "—"}٪</span><span className="small dim">من الجزء المحسوب آلياً ({Math.round(a.deterministic_weight * 100)}٪ من الميزان)</span></div>
        <div className="meter" role="img" aria-label={`النتيجة المبدئية ${a.total_pct ?? 0} بالمئة`}><i style={{ inlineSize: `${a.total_pct ?? 0}%` }} /></div>
        {a.caps_applied.length > 0 && <div className="card" style={{ borderColor: "var(--amber)" }}><b>سقوف طُبِّقت:</b><ul>{a.caps_applied.map((c, i) => <li key={i}>{c}</li>)}</ul></div>}
        {a.criteria.map((c) => (
          <details key={c.id} open={c.status === "scored" && (c.fraction ?? 1) < 0.6}>
            <summary><b>{c.name_ar}</b> — {c.status === "pending_human" ? "بانتظار مراجعة بشرية" : `${Math.round((c.fraction ?? 0) * 100)}٪`}</summary>
            <ul>{c.feedback_ar.map((f, i) => <li key={i}>{f}</li>)}</ul>
          </details>
        ))}
      </section>
      <section className="card stack"><h2>كيف تُحَلّ القضية خطوة بخطوة</h2>
        <ol>{d.steps.map((s) => <li key={s.order}>{s.text_ar}{s.uses_evidence_ids.length > 0 && <div className="small dim">الأدلة: {s.uses_evidence_ids.map(evT).join("، ")}</div>}</li>)}</ol>
        {d.alternative_paths_ar.length > 0 && <><h3>طرق أخرى مشروعة</h3><ul>{d.alternative_paths_ar.map((p, i) => <li key={i}>{p}</li>)}</ul></>}
        {d.what_evidence_could_not_show_ar.length > 0 && <><h3>ما لا تستطيع الأدلة قوله</h3><ul>{d.what_evidence_could_not_show_ar.map((p, i) => <li key={i}>{p}</li>)}</ul></>}
        {d.science_notes_ar.length > 0 && <><h3>ملاحظات علمية</h3><ul>{d.science_notes_ar.map((p, i) => <li key={i}>{p}</li>)}</ul></>}
      </section>
      {d.claims_resolved.length > 0 && (
        <section className="card stack"><h2>ما قيل وما ثبت</h2>
          {d.claims_resolved.map((c, i) => <div key={i}><p style={{ margin: 0 }}>«{c.statement_ar}»</p><p className="small dim">{c.truth_ar ? `الواقع: ${c.truth_ar}` : "لا تحسمه الأدلة."}</p></div>)}
        </section>
      )}
      {r.review_ticket && <section className="card"><h3>طلب المراجعة البشرية</h3><p>رمز متابعتك: <b className="mono">{r.review_ticket}</b></p><Link href={`/review/${r.review_ticket}`}>تابع حالة الطلب</Link></section>}
      {tt && (
        <section className="card stack" aria-labelledby="tr-h"><h2 id="tr-h">تحدي النقل: {tt.title_ar}</h2>
          {r.transfer ? (
            <div className="stack"><p><b>{r.transfer.score_pct}٪</b> — {r.transfer.note_ar}</p>
              {r.transfer.missed.length > 0 && <p className="small">فاتتك خطوات صحيحة: {r.transfer.missed.map((id) => tt.options.find((o) => o.id === id)?.text_ar).join("؛ ")}</p>}
              {r.transfer.wrong.length > 0 && <p className="small err">اخترت خطوات لا تفيد: {r.transfer.wrong.map((id) => tt.options.find((o) => o.id === id)?.text_ar).join("؛ ")}</p>}</div>
          ) : (
            <form className="stack" onSubmit={(e) => { e.preventDefault(); void send({ op: "transfer", picked, free_text: ft }); }}>
              <p>{tt.scenario_ar}</p>
              {tt.documents.map((dd, i) => <div key={i} className="paper"><h3>{dd.title_ar}</h3>{dd.body_ar}</div>)}
              <p><b>{tt.prompt_ar}</b></p>
              {tt.options.map((o) => <label key={o.id} style={{ display: "flex", gap: 12, fontWeight: 400 }}><input type="checkbox" checked={picked.includes(o.id)} onChange={() => setPicked((p) => p.includes(o.id) ? p.filter((x) => x !== o.id) : [...p, o.id])} /><span>{o.text_ar}</span></label>)}
              <label htmlFor="trft">{tt.free_text_prompt_ar}</label><textarea id="trft" value={ft} onChange={(e) => setFt(e.target.value)} maxLength={1500} />
              <button className="btn primary" disabled={busy || picked.length === 0}>أرسل</button>
            </form>
          )}
        </section>
      )}
      <div className="row">
        {!me?.user && <Link className="btn primary" href="/account?next=/profile">أنشئ حساباً لحفظ تقدّمك</Link>}
        <Link className="btn" href="/profile">مهاراتي</Link><Link className="btn ghost" href="/cases">القضية التالية</Link>
      </div>
    </div>
  );
}
