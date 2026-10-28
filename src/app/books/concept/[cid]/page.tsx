import Link from "next/link";
import { notFound } from "next/navigation";
import { getActorFromCookies } from "@/server/auth";
import { loadBooks, visibleConcepts, AGE_LABEL, SAFETY_LABEL, SKILL_LABEL } from "@/engine/books";
import { loadKnowledge } from "@/engine/knowledge";

import { Badge } from "@/components/ui/badge";
import { Card, CardTitle, RowLink } from "@/components/ui/card";

export const dynamic = "force-dynamic";

export default async function ConceptPage({ params }: { params: Promise<{ cid: string }> }) {
  const { cid } = await params;
  const a = await getActorFromCookies();
  const { books, concepts } = loadBooks();
  const c = visibleConcepts(concepts, books, a.ageBand).find((x) => x.id === cid);
  if (!c) notFound();
  const book = books.find((b) => b.id === c.book_id)!;
  const { kos } = loadKnowledge();
  const linked = c.linked_ko_ids.map((k) => kos.find((x) => x.ko_id === k)).filter((k): k is NonNullable<typeof k> => !!k && k.audience === "player");
  return (
    <article className="stack-lg">
      <div className="ref-hero">
        <p className="ref-hero-kicker">{SKILL_LABEL[c.skill]}</p>
        <h1 className="ref-hero-title">{c.title_ar}</h1>
        <p className="ref-hero-hook">سطر واحد من ملف «{book.title_ar}» يستحق أن نقرأه بعين المحقق.</p>
      </div>
      <p className="narrative">{c.summary_ar}</p>
      <div className="row"><Badge>{SKILL_LABEL[c.skill]}</Badge><Badge outline>{AGE_LABEL[c.age_band]}</Badge><Badge outline>{SAFETY_LABEL[c.safety_level]}</Badge></div>
      <Card as="section"><CardTitle level={2}>كيف تستخدمه في التحقيق</CardTitle><p>{c.investigation_use_ar}</p></Card>
      <Card as="section"><CardTitle level={2}>حدوده</CardTitle><p>{c.limits_ar}</p></Card>
      {c.myth_ar && <Card as="section"><CardTitle level={2}>فكرة شائعة</CardTitle><p>{c.myth_ar}</p></Card>}
      {c.glossary.length > 0 && <div className="row small">{c.glossary.map((g) => <Badge key={g} outline>{g}</Badge>)}</div>}
      {linked.length > 0 && (
        <section className="stack-sm"><h2 className="text-label section-title">مواد مرتبطة في الموسوعة</h2>
          <ul className="list">{linked.map((k) => <li key={k.ko_id}><RowLink href={`/knowledge/${k.ko_id}`} title={k.name_ar} /></li>)}</ul></section>
      )}
      <Card as="section"><CardTitle level={2}>المرجع</CardTitle>
        <p className="small">{book.title_ar} — {c.ref_ar}. ملاحظة بصياغتنا، لا اقتباس من الكتاب.</p>
        <p className="small"><Link href={`/books/${book.id}`}>مخطط الكتاب</Link></p></Card>
    </article>
  );
}
