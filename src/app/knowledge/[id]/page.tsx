import Link from "next/link";
import { notFound } from "next/navigation";
import { getActorFromCookies } from "@/server/auth";
import { CONF_LABEL, RIGHTS_LABEL, STATUS_LABEL, TYPE_LABEL, loadKnowledge, visibleKos } from "@/engine/knowledge";
import { loadTracks } from "@/engine/tracks";

export const dynamic = "force-dynamic";
const EN_KEYS = ["what_it_can_show", "what_it_cannot_show", "error_sources", "tv_myth", "safe_simulation", "reliability_note", "discipline", "operational_definition", "common_errors", "evidence_strength", "transfer_notes", "plot_type", "mystery_principle", "fairness_criterion", "athar_use", "strengths", "weaknesses"];
const EN_LABEL: Record<string, string> = {
  what_it_can_show: "ما يمكن أن يدلّ عليه", what_it_cannot_show: "ما لا يستطيع إثباته", error_sources: "مصادر الخطأ", tv_myth: "الخرافة التلفزيونية",
  safe_simulation: "محاكاة آمنة مقترحة", reliability_note: "ملاحظة عن الموثوقية", discipline: "التخصص", operational_definition: "التعريف التشغيلي",
  common_errors: "أخطاء شائعة", evidence_strength: "قوة الدليل", transfer_notes: "الانتقال إلى الحياة", plot_type: "نوع الحبكة", mystery_principle: "مبدأ التشويق",
  fairness_criterion: "معيار العدالة", athar_use: "استخدامه في أثر", strengths: "نقاط القوة", weaknesses: "نقاط الضعف",
};

export default async function Ko({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const a = await getActorFromCookies();
  const { kos, src } = loadKnowledge();
  const k = visibleKos(kos, a.ageBand).find((x) => x.ko_id === id);
  if (!k) notFound();
  const srcs = k.source_ids.map((s) => src.find((x) => x.id === s)).filter((x): x is NonNullable<typeof x> => !!x);
  const lessons = loadTracks().tracks.flatMap((t) => t.lessons.filter((l) => l.ko_refs.includes(k.ko_id)).map((l) => ({ id: l.id, title: l.title_ar })));
  const extras = EN_KEYS.filter((key) => k.extra[key] !== undefined);
  return (
    <article className="wrap-narrow stack">
      <p className="kicker"><Link href="/knowledge">الموسوعة</Link> · {TYPE_LABEL[k.type]}</p>
      <h1>{k.name_ar}</h1>
      <p className="small dim" lang="en" dir="ltr">{k.name}</p>
      <p style={{ fontFamily: "var(--f-display)", fontSize: "1.2rem" }}>{k.summary_ar}</p>
      <div className="row small"><span className="chip">{CONF_LABEL[k.confidence]}</span><span className="chip">{STATUS_LABEL[k.status]}</span>{k.tags.map((t) => <span key={t} className="chip" lang="en" dir="ltr">{t}</span>)}</div>
      {lessons.length > 0 && <section className="card"><h3>دروس مرتبطة</h3><ul>{lessons.map((l) => <li key={l.id}><Link href={`/academy/${l.id}`}>{l.title}</Link></li>)}</ul></section>}
      {extras.length > 0 && (
        <details className="card"><summary>تفاصيل من المكتبة البحثية (بالإنجليزية)</summary>
          <dl className="stack" lang="en" dir="ltr">
            {extras.map((key) => { const v = k.extra[key]; return <div key={key}><dt className="small dim">{EN_LABEL[key]}</dt><dd style={{ margin: 0 }}>{Array.isArray(v) ? v.join(" · ") : String(v)}</dd></div>; })}
          </dl>
        </details>
      )}
      <section className="card stack"><h3>المصادر ({srcs.length})</h3>
        <p className="small dim">المصدر المحمي بحقوق نشر يُذكر هنا للإحالة فقط؛ لا ننسخ نصه.</p>
        <ul className="stack">{srcs.map((s) => (
          <li key={s.id} className="small">{s.url ? <a href={s.url} rel="noopener noreferrer" target="_blank" lang="en" dir="ltr">{s.title}</a> : <span lang="en" dir="ltr">{s.title}</span>}
            {s.year ? ` (${s.year})` : ""} — {RIGHTS_LABEL[s.rights ?? "UNKNOWN"] ?? s.rights}</li>))}</ul></section>
    </article>
  );
}
