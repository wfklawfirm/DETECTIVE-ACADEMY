import { getActorFromCookies } from "@/server/auth";
import { koLinks, loadReasoning } from "@/engine/reference";
import { Badge } from "@/components/ui/badge";
import { Card, CardTitle } from "@/components/ui/card";
import { KoLinkRow, MoreReference, Paras, RefHead, Section, SourcesBox } from "@/components/reference/parts";

export const metadata = { title: "أخطاء الاستدلال وقواعد الدليل" };
export const dynamic = "force-dynamic";

export default async function Reasoning() {
  const a = await getActorFromCookies();
  const r = loadReasoning();
  const areas = [...new Set(r.skills.map((s) => s.area_ar))];
  return (
    <>
      <RefHead title="أخطاء الاستدلال وقواعد الدليل" hook={r.hook_ar} />
      <nav aria-label="أقسام الصفحة" className="row small">
        {[["errors", "أخطاء الاستدلال"], ["evidence", "تقييم الدليل"], ["uncertainty", "سلّم الاحتمال"], ["ethics", "التحقيق الأخلاقي"], ["skills", "مهارات الاستدلال"]].map(([id, l]) => <a key={id} className="badge badge-outline" href={`#${id}`}>{l}</a>)}
      </nav>

      <Section id="errors" title="أخطاء الاستدلال الشائعة" hook="أربعة عشر خطأً يقع فيه المحققون الأذكياء أيضاً. لكل خطأ تدريب صغير.">
        <ul className="list">
          {r.errors.map((e) => (
            <li key={e.n}>
              <Card as="article" aria-labelledby={`err-${e.n}`}>
                <span className="row small"><Badge outline>{e.n}</Badge>{e.strength_ar && <Badge tone="info">قوة الدليل البحثي: {e.strength_ar}</Badge>}</span>
                <CardTitle level={3} id={`err-${e.n}`}>{e.name_ar}</CardTitle>
                {e.name_en && <p className="small dim" lang="en" dir="ltr" style={{ textAlign: "start" }}>{e.name_en}</p>}
                <p>{e.definition_ar}</p>
                {e.limits_ar && <p className="small dim-2"><b>حدود الدليل: </b>{e.limits_ar}</p>}
                <p className="paper" style={{ padding: "0.6rem 0.9rem" }}><b>جرّب: </b>{e.practice_ar}</p>
                <KoLinkRow links={koLinks(e.ko_ids, a.ageBand)} />
                <SourcesBox ids={e.src_ids} />
              </Card>
            </li>
          ))}
        </ul>
      </Section>

      <Section id="evidence" title="قائمة تقييم الدليل" hook="قبل أن تضع أي معلومة في ملف الاتهام، فرّق بين أنواعها ثم اسألها خمسة أسئلة.">
        <div className="table-wrap" tabIndex={0} role="region" aria-label="جدول قابل للتمرير"><table className="lab-table">
          <caption className="sr-only">أنواع المعلومات في القضية</caption>
          <thead><tr><th scope="col">النوع</th><th scope="col">ما هو</th><th scope="col">مثال</th></tr></thead>
          <tbody>{r.evidence_types.map((t) => <tr key={t.kind_ar}><th scope="row">{t.kind_ar}</th><td>{t.def_ar}</td><td>{t.example_ar}</td></tr>)}</tbody>
        </table></div>
        <p className="narrative">فرّق بين ما رأيته، وما قيل لك، وما استنتجته أنت.</p>
        <ol className="list">
          {r.criteria.map((c) => (
            <li key={c.n}>
              <Card as="article" aria-labelledby={`crit-${c.n}`}>
                <CardTitle level={3} id={`crit-${c.n}`}>{c.n}. {c.name_ar}{c.name_en && <span className="small dim" lang="en" dir="ltr"> ({c.name_en})</span>}</CardTitle>
                <p><b>اسأل نفسك: </b>{c.ask_ar}</p>
                {c.extra_ar.map((x) => <p key={x} className="small dim-2">{x}</p>)}
                {c.pro_ar && <details><summary>كيف يصوغها المحترفون</summary><Paras text={c.pro_ar} className="small" /><SourcesBox ids={c.src_ids} /></details>}
              </Card>
            </li>
          ))}
        </ol>
        <Card as="section" aria-labelledby="pocket">
          <CardTitle level={3} id="pocket">أسئلة الجيب السبعة</CardTitle>
          <ol className="stack-sm">{r.pocket_questions.map((q) => <li key={q}>{q}</li>)}</ol>
        </Card>
      </Section>

      <Section id="uncertainty" title="سلّم الاحتمال: كم أنت متأكد؟" hook="«ربما» كلمة تعني عند كل شخص رقماً مختلفاً. اختر درجة من السلّم بدل الكلمة الغامضة.">
        <div className="table-wrap" tabIndex={0} role="region" aria-label="جدول قابل للتمرير"><table className="lab-table">
          <caption className="sr-only">درجات الاحتمال ومداها التقريبي</caption>
          <thead><tr><th scope="col">الدرجة</th><th scope="col">العبارة</th><th scope="col">المدى التقريبي</th></tr></thead>
          <tbody>{r.uncertainty.ladder.map((l) => <tr key={l.level}><td className="num">{l.level}</td><th scope="row">{l.phrase_ar}</th><td className="num" dir="ltr">{l.range}</td></tr>)}</tbody>
        </table></div>
        <p>{r.uncertainty.teen_ar}</p>
        <p className="small dim">هذا سلّم مقترح مستعار من سياق التحليل الاستخباري وترجمته العربية لم تُختبر على قرّاء بعد.</p>
      </Section>

      <Section id="ethics" title="مبادئ التحقيق الأخلاقي" hook="تحقيق يربح القضية ويخسر الإنصاف تحقيق فاشل. هذه مبادئ سبعة تلتزم بها قضايا أثر.">
        <ul className="list">
          {r.ethics.map((e) => (
            <li key={e.n}>
              <Card as="article" aria-labelledby={`eth-${e.n}`}>
                <CardTitle level={3} id={`eth-${e.n}`}>{e.n}. {e.name_ar}{e.name_en && <span className="small dim" lang="en" dir="ltr"> ({e.name_en})</span>}</CardTitle>
                <p><b>ما تتعلمه: </b>{e.learn_ar}</p>
                {e.commitments_ar.length > 0 && (
                  <details><summary>ما تلتزم به أثر في قضاياها</summary><ul className="stack-sm">{e.commitments_ar.map((c) => <li key={c} className="small">{c}</li>)}</ul><SourcesBox ids={e.src_ids} /></details>
                )}
              </Card>
            </li>
          ))}
        </ul>
      </Section>

      <Section id="skills" title="خريطة مهارات الاستدلال" hook="أربع وعشرون مهارة صغيرة، تُقاس كل واحدة على حدة. النجاح في اللغز لا يعني أنك أتقنتها كلها.">
        {areas.map((area) => (
          <div key={area} className="stack-sm">
            <h3 className="text-label">{area}</h3>
            <ul className="list">
              {r.skills.filter((s) => s.area_ar === area).map((s) => (
                <li key={s.id}>
                  <Card flat as="article">
                    <b>{s.name_ar}</b> <span className="small dim" lang="en" dir="ltr">{s.name_en}</span>
                    <p className="small">{s.def_ar}</p>
                    {s.mistakes_ar && <p className="small dim-2"><b>أخطاء شائعة: </b>{s.mistakes_ar}</p>}
                  </Card>
                </li>
              ))}
            </ul>
          </div>
        ))}
        <details className="card card-flat">
          <summary>لماذا لا نعطيك «درجة ذكاء محقق»؟</summary>
          <ul className="stack-sm">{r.assessment_notes_ar.map((n) => <li key={n} className="small">{n}</li>)}</ul>
          <p className="small dim">هذه عناوين الدروس التي استخلصناها عند تصميم التقييم، وتفصيلها داخلي وما زال قيد المراجعة.</p>
        </details>
      </Section>
      <MoreReference current="/reasoning" />
    </>
  );
}
