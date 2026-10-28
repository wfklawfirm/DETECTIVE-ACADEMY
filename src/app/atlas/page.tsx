import { getActorFromCookies } from "@/server/auth";
import { loadAtlas } from "@/engine/reference";
import { PATTERN_AGE_TONE } from "@/engine/reference-labels";
import { Badge } from "@/components/ui/badge";
import { Card, CardTitle } from "@/components/ui/card";
import { Callout } from "@/components/ui/feedback";
import { RefBrowser, type RefItem } from "@/components/reference/RefBrowser";
import { MoreReference, RefHead, Section, SourcesBox } from "@/components/reference/parts";

export const metadata = { title: "أطلس الأدب البوليسي" };
export const dynamic = "force-dynamic";

const KIND = { principle: "مبدأ من الأدب", expansion: "مبدأ من تقاليد العالم", corpus: "عمل من التراث العربي", heritage: "درس من التراث", pattern: "نمط حبكة" } as const;

export default async function Atlas() {
  await getActorFromCookies();
  const f = loadAtlas();
  const refs: RefItem[] = [
    ...f.corpus.map((c, i): RefItem => ({
      id: `C${String(i + 1).padStart(2, "0")}`, text: [c.work_ar, c.author_ar, c.era_ar, c.kind_ar, c.idea_ar].join(" "), facets: { kind: "corpus" },
      node: (
        <Card as="article">
          <Badge tone="brand">{KIND.corpus}</Badge>
          <CardTitle level={2}>{c.work_ar}</CardTitle>
          <dl className="stack-sm" style={{ margin: 0 }}>
            <div><dt className="small dim">المؤلف</dt><dd style={{ margin: 0 }}>{c.author_ar}</dd></div>
            <div><dt className="small dim">العصر (سنة الوفاة)</dt><dd style={{ margin: 0 }}>{c.era_ar}</dd></div>
            <div><dt className="small dim">النوع</dt><dd style={{ margin: 0 }}>{c.kind_ar}</dd></div>
            <div><dt className="small dim">الفكرة التي يقدّمها</dt><dd style={{ margin: 0 }}>{c.idea_ar}</dd></div>
          </dl>
          <SourcesBox ids={c.src_ids} />
        </Card>
      ),
    })),
    ...f.heritage.map((h): RefItem => ({
      id: h.id, text: [h.title_ar, h.basis_ar].join(" "), facets: { kind: "heritage" },
      node: (<Card as="article"><Badge tone="brand">{KIND.heritage}</Badge><CardTitle level={2}>{h.title_ar}</CardTitle><p className="small">{h.basis_ar}</p><SourcesBox ids={h.src_ids} /></Card>),
    })),
    ...f.principles.map((p): RefItem => ({
      id: `P${String(p.n).padStart(2, "0")}`, text: [p.title_ar, p.principle_ar, p.basis_ar, p.why_ar].join(" "), facets: { kind: "principle" },
      node: (
        <Card as="article">
          <span className="row small"><Badge outline>المبدأ {p.n}</Badge><Badge>{KIND.principle}</Badge></span>
          <CardTitle level={2}>{p.title_ar}</CardTitle>
          <p>{p.principle_ar}</p>
          <details><summary>الأساس الأدبي ولماذا يعمل</summary>
            <p className="small">{p.basis_ar}</p>{p.why_ar && <p className="small dim-2"><b>لماذا يعمل: </b>{p.why_ar}</p>}<SourcesBox ids={p.src_ids} /></details>
        </Card>
      ),
    })),
    ...f.expansion.map((p): RefItem => ({
      id: `A${p.n}`, text: [p.title_ar, p.principle_ar, p.basis_ar, p.why_ar].join(" "), facets: { kind: "expansion" },
      node: (
        <Card as="article">
          <span className="row small"><Badge outline>مبدأ {p.n}</Badge><Badge>{KIND.expansion}</Badge></span>
          <CardTitle level={2}>{p.title_ar}</CardTitle>
          <p>{p.principle_ar}</p>
          <details><summary>الأساس ولماذا يعمل</summary>
            <p className="small">{p.basis_ar}</p>{p.why_ar && <p className="small dim-2"><b>لماذا يعمل: </b>{p.why_ar}</p>}<SourcesBox ids={p.src_ids} /></details>
        </Card>
      ),
    })),
    ...f.patterns.map((p): RefItem => ({
      id: `T${String(p.n).padStart(2, "0")}`, text: [p.name_ar, p.name_en, p.def_ar, p.pros_ar, p.cons_ar].join(" "), facets: { kind: "pattern" },
      node: (
        <Card as="article">
          <span className="row small"><Badge outline>الصعوبة {p.diff} من 5</Badge><Badge tone="brand">{KIND.pattern}</Badge></span>
          <CardTitle level={2}>{p.name_ar}</CardTitle>
          <p className="small dim" lang="en" dir="ltr" style={{ textAlign: "start" }}>{p.name_en}</p>
          <p>{p.def_ar}</p>
          <details><summary>المزايا والعيوب والأعمار</summary>
            {p.pros_ar && <p className="small"><b>المزايا: </b>{p.pros_ar}</p>}
            {p.cons_ar && <p className="small"><b>العيوب: </b>{p.cons_ar}</p>}
            <span className="row small"><Badge tone={PATTERN_AGE_TONE[p.a13]}>13–15: {p.a13}</Badge><Badge tone={PATTERN_AGE_TONE[p.a16]}>16–18: {p.a16}</Badge><Badge tone={PATTERN_AGE_TONE[p.a18]}>18+: {p.a18}</Badge></span>
          </details>
        </Card>
      ),
    })),
  ];
  return (
    <>
      <RefHead title="أطلس الأدب البوليسي" hook={f.hook_ar} />
      <Callout tone="info" title="كيف نتعامل مع الأعمال المحمية؟">{f.rights_note_ar}</Callout>
      <nav aria-label="أقسام الصفحة" className="row small">
        <a className="badge badge-outline" href="#cards">البطاقات ({refs.length})</a>
        <a className="badge badge-outline" href="#limits">حدود التراث</a>
        <a className="badge badge-outline" href="#myths">مبالغات شائعة</a>
        <a className="badge badge-outline" href="#avoid">ما لا نكتبه</a>
        <a className="badge badge-outline" href="#works">أعمال يُشار إليها</a>
      </nav>
      <Section id="cards" title="بطاقات الأطلس">
        <RefBrowser items={refs} noun="بطاقة" searchLabel="ابحث في الأطلس" placeholder="مثلاً: قرينة، إياس، الغرفة المغلقة، تحدي القارئ"
          facets={[{ key: "kind", label: "نوع البطاقة", display: "select", allLabel: "كل الأنواع", options: (Object.keys(KIND) as (keyof typeof KIND)[]).map((k) => ({ value: k, label: `${KIND[k]}` })) }]} />
      </Section>
      <Section id="limits" title="ما لا يثبته التراث" hook={f.hooks.heritage}>
        <ol className="stack-sm">{f.heritage_limits_ar.map((x) => <li key={x} className="small">{x}</li>)}</ol>
      </Section>
      <Section id="myths" title="حقائق مشهورة مبالغ فيها" hook={f.hooks.myths}>
        <ol className="stack-sm">{f.myths_ar.map((x) => <li key={x} className="small">{x}</li>)}</ol>
      </Section>
      <Section id="avoid" title="أنماط لا نكتبها أبداً" hook="اللغز العادل يعرف ما يرفضه كما يعرف ما يحبه.">
        <ul className="stack-sm">{f.avoid_ar.map((x) => <li key={x} className="small">{x}</li>)}</ul>
      </Section>
      <Section id="works" title={`أعمال يُشار إليها (${f.works.length})`} hook={f.hooks.works}>
        <details className="card card-flat">
          <summary>عرض القائمة</summary>
          <p className="small dim">للإحالة فقط: العنوان والمؤلف وسنة النشر الأولى. لا نقتبس منها ولا نستعمل شخصياتها.</p>
          <ul className="stack-sm" lang="en" dir="ltr">
            {f.works.map((w) => <li key={w.title + w.author} className="small"><b>{w.title}</b> — {w.author} ({w.year})</li>)}
          </ul>
          <p className="small dim">الحالة القانونية لكل عمل قيد مراجعة محامٍ؛ ما لم يُراجع نعامله على أنه للإحالة فقط.</p>
        </details>
      </Section>
      <MoreReference current="/atlas" />
    </>
  );
}
