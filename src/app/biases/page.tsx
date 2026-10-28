import { getActorFromCookies } from "@/server/auth";
import { koLinks, loadBiases } from "@/engine/reference";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { RefBrowser, type RefItem } from "@/components/reference/RefBrowser";
import { KoLinkRow, MoreReference, Paras, Section, SourcesBox } from "@/components/reference/parts";

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
      {/* ── Hero ─────────────────────────────────────────────── */}
      <div className="ref-hero">
        <p className="ref-hero-kicker">مرجع المحقق</p>
        <h1 className="ref-hero-title">فخاخ العقل</h1>
        <p className="ref-hero-hook">{f.hook_ar}</p>
        <div className="ref-hero-stats">
          <div>
            <span className="ref-hero-stat-value">{f.items.length}</span>
            <span className="ref-hero-stat-label">فخ معرفي</span>
          </div>
        </div>
      </div>

      {/* Balance note */}
      <div className="case-detail-disclaimer">
        <span className="case-detail-disclaimer-mark" aria-hidden>⚡</span>
        <p><b>التحيز ليس دائماً خطأً — </b>{f.balance_ar}</p>
      </div>

      <p className="small dim-2">الأمثلة هنا قصيرة وخيالية كتبناها لتقريب الفكرة، وليست نتائج تجارب.</p>
      <RefBrowser items={refs} noun="بطاقة" searchLabel="ابحث في الفخاخ" placeholder="مثلاً: تأكيد، إرساء، عينة، معدل أساسي" />
      <Section title="علم يصحح نفسه" hook="بعض الأفكار الشهيرة عن العقل لم تصمد حين أُعيدت تجاربها. هذا ليس عيباً في العلم بل هو طريقته.">
        <ul className="stack-sm">{f.self_correcting_ar.map((x) => <li key={x} className="small">{x}</li>)}</ul>
      </Section>
      <MoreReference current="/biases" />
    </>
  );
}
