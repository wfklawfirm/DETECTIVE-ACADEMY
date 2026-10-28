import Link from "next/link";
import { getActorFromCookies } from "@/server/auth";
import { GLOSSARY_STATUS_LABEL, GLOSSARY_STATUS_TONE, LEVEL_LABEL, glossaryFor, koLinks, loadGlossary, sortLetters } from "@/engine/reference";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { RefBrowser, type RefItem } from "@/components/reference/RefBrowser";
import { KoLinkRow, MoreReference, SourcesBox } from "@/components/reference/parts";

export const metadata = { title: "المسرد الجنائي" };
export const dynamic = "force-dynamic";

export default async function Glossary() {
  const a = await getActorFromCookies();
  const g = loadGlossary();
  const all = g.items;
  const items = glossaryFor(all, a.ageBand);
  const hidden = all.length - items.length;
  const catLabel = new Map(g.categories.map((c) => [c.id, c.label_ar]));
  const letters = sortLetters(items.map((i) => i.letter));
  const refs: RefItem[] = items.map((t) => ({
    id: t.id,
    text: [t.term_ar, t.term_en, ...t.alts_ar, t.def_ar].join(" "),
    facets: { letter: t.letter, cat: t.cat },
    node: (
      <Card as="article" aria-labelledby={`${t.id}-t`}>
        <div className="row-between" style={{ alignItems: "baseline" }}>
          <h2 className="card-title" id={`${t.id}-t`}>{t.term_ar}</h2>
          <a className="small dim linklike" dir="ltr" href={`#${t.id}`} aria-label={`رابط مباشر إلى «${t.term_ar}»`}>#{t.id}</a>
        </div>
        <p className="small dim" lang="en" dir="ltr" style={{ textAlign: "start" }}>{t.term_en}</p>
        <p>{t.def_ar}</p>
        <span className="row small">
          <Badge outline>{catLabel.get(t.cat) ?? t.cat}</Badge>
          <Badge outline>{LEVEL_LABEL[t.level]}</Badge>
          <Badge tone={GLOSSARY_STATUS_TONE[t.status]}>{GLOSSARY_STATUS_LABEL[t.status]}</Badge>
        </span>
        {(t.alts_ar.length > 0 || t.ko_ids.length > 0 || t.src_ids.length > 0) && (
          <details>
            <summary>تفاصيل ومرادفات ومراجع</summary>
            <div className="stack-sm">
              {t.alts_ar.length > 0 && <p className="small"><b>صيغ أخرى مستعملة: </b>{t.alts_ar.join("، ")}</p>}
              <KoLinkRow links={koLinks(t.ko_ids, a.ageBand)} />
              <SourcesBox ids={t.src_ids} compact />
            </div>
          </details>
        )}
      </Card>
    ),
  }));
  return (
    <>
            <div className="ref-hero">
        <p className="ref-hero-kicker">مرجع المحقق</p>
        <h1 className="ref-hero-title">المسرد الجنائي</h1>
        <p className="ref-hero-hook">{g.hook_ar}</p>
        <div className="ref-hero-stats">
          <div><span className="ref-hero-stat-value">{items.length}</span><span className="ref-hero-stat-label">مصطلح</span></div>
        </div>
      </div>
      <p className="small dim-2">{items.length} مصطلحاً عربياً مع مقابلها الإنجليزي. «سلسلة العهدة» و«نسبة الترجيح» هما المصطلحان المعتمدان في واجهة Detective Academy.{hidden > 0 && ` أُخفي ${hidden} مصطلحاً مخصصاً للبالغين.`}</p>
      <RefBrowser items={refs} noun="مصطلح" searchLabel="ابحث في المسرد" placeholder="مثلاً: عهدة، بصمة، ترجيح، chain of custody"
        facets={[
          { key: "letter", label: "الحرف الأول", display: "chips", options: letters.map((l) => ({ value: l, label: l })), allLabel: "الكل" },
          { key: "cat", label: "التصنيف", display: "select", allLabel: "كل التصنيفات", options: g.categories.filter((c) => items.some((i) => i.cat === c.id)).map((c) => ({ value: c.id, label: `${c.label_ar} (${items.filter((i) => i.cat === c.id).length})` })) },
        ]} />
      <p className="small dim">روابط المصادر وحقوقها الكاملة في <Link href="/sources">سجل المصادر والحقوق</Link>.</p>
      <MoreReference current="/glossary" />
    </>
  );
}
