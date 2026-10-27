"use client";
import { useState } from "react";
import { useMe } from "../Shell";
import { Button, LinkButton } from "../ui/button";
import { Card, CardTitle } from "../ui/card";
import { Callout, LoadingRegion } from "../ui/feedback";
import { ChoiceGroup, Field } from "../ui/form";
import { ProgressBar, ProgressRing } from "../ui/progress";
import type { Resp } from "./usePlay";

export function Debrief({ r, busy, send }: { r: Resp; busy: boolean; send: (x: Record<string, unknown>) => Promise<unknown> }) {
  const v = r.view; const a = r.assessment; const d = v.debrief;
  const { me } = useMe();
  const [picked, setPicked] = useState<string[]>([]);
  const [ft, setFt] = useState("");
  const concl = v.hypotheses.find((h) => h.id === v.submission?.conclusion_hypothesis_id);
  if (!a || !d) return <LoadingRegion label="جارٍ تحميل الملخص" cards={2} />;
  const evT = (id: string) => v.evidence.find((e) => e.id === id)?.title_ar ?? id;
  const tt = v.transfer_task;
  const pct = a.total_pct ?? 0;
  return (
    <>
      <header className="page-head"><p className="kicker">إغلاق الملف</p><h1 className="text-page-title">{v.title_ar}</h1></header>
      <Card as="section" className="lantern" raised aria-labelledby="sol-h">
        <h2 id="sol-h" className="text-section-title">ما الذي حدث فعلاً؟</h2>
        <p className="narrative">{d.solution_summary_ar}</p>
        {concl && <p className="small dim">استنتاجك كان: «{concl.statement_ar}» بترجيح {v.submission?.confidence}٪.</p>}
      </Card>
      <Card as="section" aria-labelledby="sc-h">
        <h2 id="sc-h" className="text-section-title">قراءة أداءك (مبدئية)</h2>
        <p className="small dim">{a.disclaimer_ar}</p>
        <div className="row" style={{ flexWrap: "nowrap" }}>
          <ProgressRing value={pct} text={`${a.total_pct ?? "—"}٪`} size={72} label={`النتيجة المبدئية ${pct} بالمئة`} />
          <span className="small dim grow">من الجزء المحسوب آلياً ({Math.round(a.deterministic_weight * 100)}٪ من الميزان)</span>
        </div>
        <ProgressBar value={pct} label={`النتيجة المبدئية ${pct} بالمئة`} />
        {a.caps_applied.length > 0 && <Callout tone="warning" title="سقوف طُبِّقت"><ul>{a.caps_applied.map((c, i) => <li key={i}>{c}</li>)}</ul></Callout>}
        {a.criteria.map((c) => (
          <details key={c.id} className="card card-flat" open={c.status === "scored" && (c.fraction ?? 1) < 0.6}>
            <summary><b>{c.name_ar}</b> <span className="dim">— {c.status === "pending_human" ? "بانتظار مراجعة بشرية" : `${Math.round((c.fraction ?? 0) * 100)}٪`}</span></summary>
            <ul>{c.feedback_ar.map((f, i) => <li key={i}>{f}</li>)}</ul>
          </details>
        ))}
      </Card>
      <Card as="section">
        <h2 className="text-section-title">كيف تُحَلّ القضية خطوة بخطوة</h2>
        <ol>{d.steps.map((s) => <li key={s.order}>{s.text_ar}{s.uses_evidence_ids.length > 0 && <div className="small dim">الأدلة: {s.uses_evidence_ids.map(evT).join("، ")}</div>}</li>)}</ol>
        {d.alternative_paths_ar.length > 0 && <><h3 className="card-title">طرق أخرى مشروعة</h3><ul>{d.alternative_paths_ar.map((p, i) => <li key={i}>{p}</li>)}</ul></>}
        {d.what_evidence_could_not_show_ar.length > 0 && <><h3 className="card-title">ما لا تستطيع الأدلة قوله</h3><ul>{d.what_evidence_could_not_show_ar.map((p, i) => <li key={i}>{p}</li>)}</ul></>}
        {d.science_notes_ar.length > 0 && <><h3 className="card-title">ملاحظات علمية</h3><ul>{d.science_notes_ar.map((p, i) => <li key={i}>{p}</li>)}</ul></>}
      </Card>
      {d.claims_resolved.length > 0 && (
        <Card as="section"><h2 className="text-section-title">ما قيل وما ثبت</h2>
          {d.claims_resolved.map((c, i) => <div key={i}><p>«{c.statement_ar}»</p><p className="small dim">{c.truth_ar ? `الواقع: ${c.truth_ar}` : "لا تحسمه الأدلة."}</p></div>)}
        </Card>
      )}
      {r.review_ticket && <Card as="section"><CardTitle level={3}>طلب المراجعة البشرية</CardTitle><p>رمز متابعتك: <b className="mono">{r.review_ticket}</b></p><LinkButton variant="outline" size="sm" href={`/review/${r.review_ticket}`} style={{ alignSelf: "flex-start" }}>تابع حالة الطلب</LinkButton></Card>}
      {tt && (
        <Card as="section" aria-labelledby="tr-h"><h2 id="tr-h" className="text-section-title">تحدي النقل: {tt.title_ar}</h2>
          {r.transfer ? (
            <div className="stack"><p><b>{r.transfer.score_pct}٪</b> — {r.transfer.note_ar}</p>
              {r.transfer.missed.length > 0 && <p className="small">فاتتك خطوات صحيحة: {r.transfer.missed.map((id) => tt.options.find((o) => o.id === id)?.text_ar).join("؛ ")}</p>}
              {r.transfer.wrong.length > 0 && <p className="small err">اخترت خطوات لا تفيد: {r.transfer.wrong.map((id) => tt.options.find((o) => o.id === id)?.text_ar).join("؛ ")}</p>}</div>
          ) : (
            <form className="stack" onSubmit={(e) => { e.preventDefault(); void send({ op: "transfer", picked, free_text: ft }); }}>
              <p>{tt.scenario_ar}</p>
              {tt.documents.map((dd, i) => <div key={i} className="paper"><h3>{dd.title_ar}</h3>{dd.body_ar}</div>)}
              <p><b>{tt.prompt_ar}</b></p>
              <ChoiceGroup multiple label="الخطوات" name="tr" value={picked} onChange={(id) => setPicked((p) => p.includes(id) ? p.filter((x) => x !== id) : [...p, id])} options={tt.options.map((o) => ({ value: o.id, label: o.text_ar }))} />
              <Field label={tt.free_text_prompt_ar}>{(p) => <textarea {...p} className="textarea" value={ft} onChange={(e) => setFt(e.target.value)} maxLength={1500} />}</Field>
              <Button type="submit" variant="secondary" disabled={busy || picked.length === 0}>أرسل</Button>
            </form>
          )}
        </Card>
      )}
      <div className="stack-sm">
        {!me?.user ? <LinkButton variant="primary" size="lg" block href="/account?next=/profile">أنشئ حساباً لحفظ تقدّمك</LinkButton> : <LinkButton variant="primary" size="lg" block href="/cases">القضية التالية</LinkButton>}
        <LinkButton variant="secondary" block href="/profile">مهاراتي</LinkButton>
        {!me?.user && <LinkButton variant="ghost" block href="/cases">القضية التالية</LinkButton>}
      </div>
    </>
  );
}
