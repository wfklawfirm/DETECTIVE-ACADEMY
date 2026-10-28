import Link from "next/link";
import { getActorFromCookies } from "@/server/auth";
import { AGE_BAND_LABEL, VIOLENCE_LABEL, archetypeCaseUse, gated, isAdult, loadArchetypes } from "@/engine/reference";
import { Badge } from "@/components/ui/badge";
import { Card, CardTitle } from "@/components/ui/card";
import { RefBrowser, type RefItem } from "@/components/reference/RefBrowser";
import { MoreReference, RefHead } from "@/components/reference/parts";

export const metadata = { title: "أنماط الألغاز" };
export const dynamic = "force-dynamic";

export default async function Archetypes() {
  const a = await getActorFromCookies();
  const f = loadArchetypes();
  const items = gated(f.items, a.ageBand);
  const hidden = f.items.length - items.length;
  const uses = archetypeCaseUse(f.items);
  const built = (id: string) => (uses.get(id) ?? []).filter((c) => c.age_band !== "18+" || isAdult(a.ageBand));
  const nBuilt = items.filter((x) => built(x.id).length > 0).length;
  const refs: RefItem[] = items.map((x) => {
    const cases = built(x.id);
    return {
      id: x.id,
      text: [x.name_ar, x.name_en, x.core_ar, ...x.teaches_ar, ...x.concepts_ar, ...x.pattern_ar].join(" "),
      facets: { age: x.age_band, built: cases.length ? "yes" : "no" },
      node: (
        <Card as="article" aria-labelledby={`${x.id}-t`}>
          <span className="row small">
            <Badge outline latin dir="ltr" lang="en">{x.id}</Badge>
            <Badge>{AGE_BAND_LABEL[x.age_band]}</Badge>
            {cases.length ? <Badge tone="positive">بُني: {cases.length} {cases.length === 1 ? "قضية" : "قضايا"}</Badge> : <Badge tone="neutral">لم يُبنَ بعد</Badge>}
            {x.no_culprit && <Badge tone="info">بلا جانٍ</Badge>}
          </span>
          <CardTitle level={2} id={`${x.id}-t`}>{x.name_ar}</CardTitle>
          <p className="small dim" lang="en" dir="ltr" style={{ textAlign: "start" }}>{x.name_en}</p>
          <p>{x.core_ar}</p>
          {x.teaches_ar.length > 0 && (
            <div className="stack-sm"><span className="text-label dim">ماذا يعلّمك هذا النمط؟</span><ul className="row" style={{ listStyle: "none", padding: 0, margin: 0 }}>{x.teaches_ar.map((t) => <li key={t}><Badge outline>{t}</Badge></li>)}</ul></div>
          )}
          {x.warnings_ar.length > 0 && (
            <div className="stack-sm"><span className="text-label" style={{ color: "var(--warning)" }}>تحذيرات اللعب العادل</span><ul className="stack-sm">{x.warnings_ar.map((w) => <li key={w} className="small">{w}</li>)}</ul></div>
          )}
          <details>
            <summary>الأعمار والأماكن والقضايا</summary>
            <div className="stack-sm">
              <p className="small"><b>مستوى العنف: </b>{VIOLENCE_LABEL[x.violence]}. {x.violence_ar}</p>
              {x.age_variant_ar && <p className="small"><b>نسخة الأعمار: </b>{x.age_variant_ar}</p>}
              {x.observables_ar && <p className="small"><b>ما نلاحظه في أدائك: </b>{x.observables_ar}</p>}
              {x.concepts_ar.length > 0 && <p className="small"><b>مفاهيم علمية مرتبطة: </b>{x.concepts_ar.join("، ")}</p>}
              {x.pattern_ar.length > 0 && <p className="small"><b>أنماط حبكة مرتبطة: </b>{x.pattern_ar.join("، ")}</p>}
              {x.lab_ar && <p className="small"><b>مختبر مرتبط: </b>{x.lab_ar}</p>}
              {x.settings_ar.length > 0 && <><span className="text-label dim">أفكار لأماكن القصة</span><ul className="stack-sm">{x.settings_ar.map((s) => <li key={s} className="small">{s}</li>)}</ul></>}
              {cases.length > 0 && <><span className="text-label dim">قضايا موجودة تشارك هذا النمط</span><ul className="stack-sm">{cases.map((c) => <li key={c.case_id} className="small"><Link href={`/case/${c.case_id}`}>{c.title_ar}</Link></li>)}</ul></>}
              <p className="small dim">حالة النمط: فرضية تصميم لم تُختبر مع لاعبين.</p>
            </div>
          </details>
        </Card>
      ),
    };
  });
  return (
    <>
      <RefHead title="أنماط الألغاز" hook={f.hook_ar} />
      <p className="small dim-2">{items.length} نمطاً، منها {nBuilt} له قضية واحدة على الأقل. النمط قالب قابل للتكرار وليس قضية جاهزة. {hidden > 0 && `أُخفي ${hidden} نمط مؤجل للبالغين. `}ننسب القضية إلى النمط حين تشترك معه في وحدة نمط حبكة من الموسوعة، فهذا استدلال تقريبي قد يخطئ.</p>
      <RefBrowser items={refs} noun="نمطاً" searchLabel="ابحث في الأنماط" placeholder="مثلاً: شهود، ساعة، وثيقة، تراث"
        facets={[
          { key: "age", label: "الفئة العمرية", display: "chips", allLabel: "الكل", options: [...new Set(items.map((x) => x.age_band))].map((v) => ({ value: v, label: AGE_BAND_LABEL[v] ?? v })) },
          { key: "built", label: "هل بُني؟", display: "chips", allLabel: "الكل", options: [{ value: "yes", label: "بُني" }, { value: "no", label: "لم يُبنَ بعد" }] },
        ]} />
      <MoreReference current="/archetypes" />
    </>
  );
}
