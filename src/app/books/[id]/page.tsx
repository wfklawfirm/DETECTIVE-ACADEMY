import { notFound } from "next/navigation";
import { getActorFromCookies } from "@/server/auth";
import { loadBooks, visibleBooks, visibleConcepts, INCLUSION_LABEL, REASON_LABEL } from "@/engine/books";

import { ConceptBrowser } from "@/components/books/ConceptBrowser";
import { Badge } from "@/components/ui/badge";
import { Card, CardTitle } from "@/components/ui/card";

export const dynamic = "force-dynamic";

export default async function BookPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const a = await getActorFromCookies();
  const { books, concepts } = loadBooks();
  const b = visibleBooks(books, a.ageBand).find((x) => x.id === id);
  if (!b) notFound();
  const items = visibleConcepts(concepts, books, a.ageBand).filter((c) => c.book_id === b.id)
    .map(({ id, book_id, section_id, section_title_ar, ref_ar, title_ar, summary_ar, age_band, safety_level, skill }) => ({ id, book_id, section_id, section_title_ar, ref_ar, title_ar, summary_ar, age_band, safety_level, skill }));
  return (
    <>
      <div className="ref-hero">
        <p className="ref-hero-kicker">{b.authors_ar.join("، ")}{b.year ? ` · ${b.year}` : ""}</p>
        <h1 className="ref-hero-title">{b.title_ar}</h1>
        <p className="ref-hero-hook">{b.hook_ar}</p>
      </div>
      <Card as="section"><CardTitle level={2}>الحقوق</CardTitle><p className="small">{b.rights_note_ar}</p></Card>
      <section className="stack" aria-labelledby="outline-h">
        <h2 id="outline-h" className="text-label section-title">مخطط الكتاب وما أخذنا منه</h2>
        <p className="small dim">أرقام الأسطر تشير إلى موضع الفكرة في النسخة النصية التي راجعناها، لا إلى أرقام صفحات مطبوعة.</p>
        <ul className="list">
          {b.sections.map((s) => (
            <li key={s.id} className="card">
              <b>{s.title_ar}</b>
              <p className="small dim">الأسطر {s.line_start}–{s.line_end}</p>
              <span className="row small"><Badge outline={s.inclusion === "excluded"}>{INCLUSION_LABEL[s.inclusion]}</Badge><Badge outline>{REASON_LABEL[s.reason_code] ?? s.reason_code}</Badge>{s.note_count > 0 && <Badge outline>{s.note_count} مفهوماً</Badge>}</span>
              <p className="small dim-2">{s.reason_ar}</p>
            </li>
          ))}
        </ul>
      </section>
      <section className="stack" aria-labelledby="concepts-h">
        <h2 id="concepts-h" className="text-label section-title">المفاهيم</h2>
        <ConceptBrowser items={items} />
      </section>
    </>
  );
}
