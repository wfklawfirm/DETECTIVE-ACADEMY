import { getActorFromCookies } from "@/server/auth";
import { koLinks, loadBiases } from "@/engine/reference";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { Callout } from "@/components/ui/feedback";
import { RefBrowser, type RefItem } from "@/components/reference/RefBrowser";
import { KoLinkRow, MoreReference, Paras, RefHead, Section, SourcesBox } from "@/components/reference/parts";

export const metadata = { title: "فخاخ العقل" };
export const dynamic = "force-dynamic";

export default async function Biases() {
  const a = await getActorFromCookies();
  const f = loadBiases();
  const refs: RefItem[] = f.items.map((b) => ({
    id: b.id,
    text: [b.name_ar, b.name_en, b.example_ar, b.research_ar].join(" "),
    facets: {},
    node: (
      <Card as="article" aria-labelledby={`${b.id}-t`}>
        <span className="row small"><Badge outline latin lang="en" dir="ltr">{b.id}</Badge></span>
        <h2 className="card-title" id={`${b.id}-t`}>{b.name_ar}</h2>
        <p className="small dim" lang="en" dir="ltr" style={{ textAlign: "start" }}>{b.name_en}</p>
        <div className="paper" style={{ padding: "0.75rem 1rem" }}>
          <p className="text-label">مثال قصير</p>
          <p>{b.example_ar}</p>
        </div>
        {b.golden_rule_ar && <p><b>القاعدة: </b>{b.golden_rule_ar}</p>}
        <details>
          <summary>ماذا يقول البحث؟ وكيف نتدرّب؟</summary>
          <div className="stack-sm">
            {b.research_ar && <><p className="text-label">ما يقوله البحث</p><Paras text={b.research_ar} className="small" /></>}
            {b.debrief_ar && <><p className="text-label">كيف نتدرّب عليه</p><Paras text={b.debrief_ar} className="small" /></>}
            <KoLinkRow links={koLinks(b.ko_ids, a.ageBand)} />
            <SourcesBox ids={b.src_ids} />
          </div>
        </details>
      </Card>
    ),
  }));
  return (
    <>
      <RefHead title="فخاخ العقل" hook={f.hook_ar} />
      <Callout tone="info" title="التحيز ليس دائماً خطأً">{f.balance_ar}</Callout>
      <p className="small dim-2">{f.items.length} فخاً معرفياً. الأمثلة هنا قصيرة وخيالية كتبناها لتقريب الفكرة، وليست نتائج تجارب.</p>
      <RefBrowser items={refs} noun="بطاقة" searchLabel="ابحث في الفخاخ" placeholder="مثلاً: تأكيد، إرساء، عينة، معدل أساسي" />
      <Section title="علم يصحح نفسه" hook="بعض الأفكار الشهيرة عن العقل لم تصمد حين أُعيدت تجاربها. هذا ليس عيباً في العلم بل هو طريقته.">
        <ul className="stack-sm">{f.self_correcting_ar.map((x) => <li key={x} className="small">{x}</li>)}</ul>
      </Section>
      <MoreReference current="/biases" />
    </>
  );
}
