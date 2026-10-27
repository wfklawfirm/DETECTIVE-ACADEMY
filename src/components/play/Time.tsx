"use client";
import { useState } from "react";
import { Button } from "../ui/button";
import { Card, CardTitle } from "../ui/card";
import { Callout } from "../ui/feedback";
import { Field } from "../ui/form";
import { FlaskIcon } from "../ui/icons";
import type { Resp, View } from "./usePlay";

type Send = (r: Record<string, unknown>) => Promise<Resp | null>;
const hm = (min: number, epochMin: number) => { const t = (((epochMin + min) % 1440) + 1440) % 1440; const d = Math.floor((epochMin + min) / 1440); return `${String(Math.floor(t / 60)).padStart(2, "0")}:${String(t % 60).padStart(2, "0")}${d > 0 ? ` (+${d})` : d < 0 ? ` (${d})` : ""}`; };

export function TimeTab({ view, busy, send, last }: { view: View; busy: boolean; send: Send; last: Resp["extra"] | null }) {
  const [ev, setEv] = useState("");
  const [time, setTime] = useState("");
  const [day, setDay] = useState(0);
  const [note, setNote] = useState("");
  const [err, setErr] = useState<string | null>(null);
  const [m0, m1] = view.clock.epoch_hhmm.split(":").map(Number) as [number, number];
  const epochMin = m0 * 60 + m1;
  const place = async () => {
    const mt = /^(\d{1,2}):(\d{2})$/.exec(time.trim());
    if (!ev || !mt || Number(mt[1]) > 23 || Number(mt[2]) > 59) { setErr("اختر دليلاً واكتب الوقت بصيغة ساعة:دقيقة، مثل 21:10"); return; }
    setErr(null);
    const minute = day * 1440 + Number(mt[1]) * 60 + Number(mt[2]) - epochMin;
    await send({ op: "timeline", evidence_id: ev, minute, note: note.trim() || undefined });
    setTime(""); setNote("");
  };
  const sorted = [...view.timeline].sort((a, b) => a.utc_minute - b.utc_minute);
  const title = (id: string) => view.evidence.find((e) => e.id === id)?.title_ar ?? id;
  return (
    <div className="stack-lg">
      <div className="stack-sm">
        <h2 className="text-section-title">الخط الزمني</h2>
        <p className="dim small">ضع الأدلة على محور واحد. قبل المقارنة تأكد أن كل الأوقات بمرجع واحد: <b>{view.clock.zone_label_ar}</b>. الصفر عند {view.clock.epoch_hhmm}.</p>
      </div>
      <Card>
        <Field label="الدليل">{(p) => <select {...p} value={ev} onChange={(e) => setEv(e.target.value)}><option value="">— اختر —</option>{view.evidence.map((e) => <option key={e.id} value={e.id}>{e.title_ar}</option>)}</select>}</Field>
        <div className="row" style={{ alignItems: "flex-start" }}>
          <Field className="grow" label={`الوقت (${view.clock.zone_label_ar})`}>{(p) => <input {...p} className="input input-ltr" inputMode="numeric" placeholder="21:10" value={time} onChange={(e) => setTime(e.target.value)} />}</Field>
          <Field className="grow" label="اليوم">{(p) => <select {...p} value={day} onChange={(e) => setDay(Number(e.target.value))}>{[-1, 0, 1, 2].map((d) => <option key={d} value={d}>{d === 0 ? "اليوم الأول" : d > 0 ? `بعد ${d} يوم` : "قبل يوم"}</option>)}</select>}</Field>
        </div>
        <Field label="ملاحظة (اختياري)">{(p) => <input {...p} className="input" value={note} maxLength={200} onChange={(e) => setNote(e.target.value)} />}</Field>
        {err && <p role="alert" className="field-error">{err}</p>}
        <Button variant="secondary" onClick={place} disabled={busy}>ضعه على الخط</Button>
      </Card>
      {sorted.length > 0 && (
        <ol className="list" aria-label="الأدلة مرتبة زمنياً">
          {sorted.map((t) => <li key={t.evidence_id}><Card flat><div className="row" style={{ flexWrap: "nowrap", alignItems: "flex-start" }}><span className="mono num" style={{ fontWeight: 600 }}>{hm(t.utc_minute, epochMin)}</span><span className="grow">{title(t.evidence_id)}{t.note ? ` — ${t.note}` : ""}</span></div></Card></li>)}
        </ol>
      )}
      {view.labs.map((lab) => <Lab key={lab.id} lab={lab} busy={busy} send={send} last={last} />)}
    </div>
  );
}

function Lab({ lab, busy, send, last }: { lab: View["labs"][number]; busy: boolean; send: Send; last: Resp["extra"] | null }) {
  const [vals, setVals] = useState<Record<string, string>>({});
  const set = (k: string, v: string) => setVals((s) => ({ ...s, [k]: v }));
  const run = () => {
    const inputs: Record<string, number> = {};
    for (const it of lab.items) { inputs[`${it.evidence_id}.offset_h`] = Number(vals[`${it.evidence_id}.offset_h`] ?? 0) || 0; inputs[`${it.evidence_id}.skew_min`] = Number(vals[`${it.evidence_id}.skew_min`] ?? 0) || 0; }
    return send({ op: "lab", lab_id: lab.id, inputs });
  };
  const lastRun = lab.runs[lab.runs.length - 1];
  const out = lastRun?.output as { rows?: { evidence_id: string; utc_min: number; label: string }[]; spread_min?: number; converged?: boolean } | undefined;
  if (lab.items.length < 2) return <Card><CardTitle level={3}>{lab.title_ar}</CardTitle><p className="dim">يحتاج هذا المختبر أدلة لم تحصل عليها بعد.</p></Card>;
  return (
    <Card as="section" aria-labelledby={`lab-${lab.id}`}>
      <h3 id={`lab-${lab.id}`} className="card-title row" style={{ flexWrap: "nowrap" }}><FlaskIcon size={22} />{lab.title_ar}</h3>
      <p className="dim small">{lab.intro_ar}</p>
      <div className="table-wrap"><table className="lab-table">
        <thead><tr><th>الدليل</th><th>الوقت الظاهر</th><th>فرق التوقيت (ساعات)</th><th>انحراف الساعة (دقائق)</th></tr></thead>
        <tbody>{lab.items.map((it) => (
          <tr key={it.evidence_id}>
            <td>{it.label_ar}{it.basis_ar && <div className="small dim">{it.basis_ar}</div>}</td>
            <td className="mono">{lab.day_labels_ar[it.day] ? `${lab.day_labels_ar[it.day]} ` : ""}{it.hhmm}</td>
            <td><input aria-label={`فرق التوقيت لـ ${it.label_ar}`} inputMode="decimal" value={vals[`${it.evidence_id}.offset_h`] ?? ""} placeholder="0" onChange={(e) => set(`${it.evidence_id}.offset_h`, e.target.value)} /></td>
            <td><input aria-label={`انحراف الساعة لـ ${it.label_ar}`} inputMode="decimal" value={vals[`${it.evidence_id}.skew_min`] ?? ""} placeholder="0" onChange={(e) => set(`${it.evidence_id}.skew_min`, e.target.value)} /></td>
          </tr>))}</tbody>
      </table></div>
      <p className="small dim">القاعدة: الوقت الموحَّد = الوقت الظاهر − فرق التوقيت + انحراف الساعة (موجب إن كانت الساعة <b>متأخرة</b>).</p>
      <Button variant="secondary" onClick={run} disabled={busy}>شغّل المقارنة</Button>
      {out?.rows && (
        <div role="status" aria-live="polite" className="stack">
          <table className="simple"><tbody>{out.rows.map((r) => <tr key={r.evidence_id}><td>{r.label}</td><td className="mono">{r.utc_min >= 0 ? "+" : ""}{r.utc_min} د</td></tr>)}</tbody></table>
          <Callout tone={out.converged ? "positive" : "warning"}>{out.converged ? "تطابقت الأوقات ضمن هامش التسامح — حصلت على نتيجة جديدة." : `ما زال الفارق ${out.spread_min} دقيقة؛ راجع المدخلات.`}</Callout>
          {last?.lab?.granted?.length ? <p className="small ok">أُضيف دليل جديد إلى الخزانة.</p> : null}
        </div>
      )}
    </Card>
  );
}
