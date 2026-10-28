import { getActorFromCookies } from "@/server/auth";
import { TIER_LABEL, TIER_ORDER, TIER_TONE, gated, koLinks, loadMethods } from "@/engine/reference";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { RefBrowser, type RefItem } from "@/components/reference/RefBrowser";
import { KoLinkRow, MoreReference, RefHead, SourcesBox } from "@/components/reference/parts";

export const metadata = { title: "طرق الفحص وحدودها" };
export const dynamic = "force-dynamic";

export default async function Methods() {
  const a = await getActorFromCookies();
  const f = loadMethods();
  const items = gated(f.items, a.ageBand);
  const hidden = f.items.length - items.length;
  const refs: RefItem[] = items.map((m) => ({
    id: m.id,
    text: [m.name_ar, m.name_en, m.hook_ar, m.discipline_ar, ...m.can_ar, ...m.cannot_ar, ...m.errors_ar].join(" "),
    facets: { tier: m.tier, disc: m.discipline_ar },
    node: (
      <Card as="article" aria-labelledby={`${m.id}-t`}>
        <span className="row small"><Badge tone={TIER_TONE[m.tier]}>{TIER_LABEL[m.tier]}</Badge><Badge outline>{m.discipline_ar}</Badge></span>
        <h2 className="card-title" id={`${m.id}-t`}>{m.name_ar}</h2>
        <p className="narrative">{m.hook_ar}</p>
        <div className="stack-sm">
          <h3 className="text-label" style={{ color: "var(--positive)" }}>ما يمكن أن تدلّ عليه</h3>
          <ul className="stack-sm">{m.can_ar.map((x) => <li key={x} className="small">{x}</li>)}</ul>
          <h3 className="text-label" style={{ color: "var(--negative)" }}>ما لا تستطيع إثباته</h3>
          <ul className="stack-sm">{m.cannot_ar.map((x) => <li key={x} className="small">{x}</li>)}</ul>
          <h3 className="text-label" style={{ color: "var(--warning)" }}>مصادر الخطأ</h3>
          <ul className="stack-sm">{m.errors_ar.map((x) => <li key={x} className="small">{x}</li>)}</ul>
        </div>
        <details>
          <summary>نص المصفوفة الأصلي (بالإنجليزية) والمراجع</summary>
          <dl className="stack" lang="en" dir="ltr">
            <div><dt className="small dim">Method</dt><dd style={{ margin: 0 }}>{m.name_en}</dd></div>
            <div><dt className="small dim">Validity assessment</dt><dd style={{ margin: 0 }}>{m.original_en.validity}</dd></div>
            <div><dt className="small dim">Error-rate evidence</dt><dd style={{ margin: 0 }}>{m.original_en.error_rate}</dd></div>
            <div><dt className="small dim">Key concerns</dt><dd style={{ margin: 0 }}>{m.original_en.concerns}</dd></div>
            <div><dt className="small dim">Standards</dt><dd style={{ margin: 0 }}>{m.standards_en}</dd></div>
            <div><dt className="small dim">Teen suitability (library note)</dt><dd style={{ margin: 0 }}>{m.suitability_en}</dd></div>
          </dl>
          <KoLinkRow links={koLinks(m.ko_ids, a.ageBand)} />
          <SourcesBox ids={m.src_ids} />
        </details>
      </Card>
    ),
  }));
  const discs = [...new Set(items.map((m) => m.discipline_ar))];
  return (
    <>
      <RefHead title="طرق الفحص وحدودها" hook={f.hook_ar} />
      <Card as="section" aria-label="مفتاح التصنيف">
        <p className="small"><b>كيف نقرأ التصنيف؟</b> هو تبسيط تعليمي لما خلصت إليه مراجعات منشورة (مثل PCAST عام 2016 وتقارير NIST)، وليس حكماً نهائياً على الطريقة. الطريقة «الراسخة» تبقى قابلة للخطأ، و«غير المدعومة» قد تُستعمل في المحاكم أحياناً.</p>
        <ul className="row" style={{ listStyle: "none", padding: 0, margin: 0 }}>{TIER_ORDER.map((t) => <li key={t}><Badge tone={TIER_TONE[t]}>{TIER_LABEL[t]}</Badge></li>)}</ul>
      </Card>
      <p className="small dim-2">{items.length} طريقة.{hidden > 0 && ` أُخفيت ${hidden} طرق مخصصة للبالغين لأنها تتصل بالأسلحة أو الوفاة أو الخلائط المعقدة.`} أثر لا تعلّم تنفيذ أي إجراء؛ نتحدث عن المفهوم وحدوده فقط.</p>
      <RefBrowser items={refs} noun="طريقة" searchLabel="ابحث في الطرق" placeholder="مثلاً: بصمة، شعر، رقمي، معدل الخطأ"
        facets={[
          { key: "tier", label: "درجة الدعم العلمي", display: "select", allLabel: "كل الدرجات", options: TIER_ORDER.filter((t) => items.some((m) => m.tier === t)).map((t) => ({ value: t, label: `${TIER_LABEL[t]} (${items.filter((m) => m.tier === t).length})` })) },
          { key: "disc", label: "التخصص", display: "select", allLabel: "كل التخصصات", options: discs.map((d) => ({ value: d, label: d })) },
        ]} />
      <MoreReference current="/methods" />
    </>
  );
}
