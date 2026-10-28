import { getActorFromCookies } from "@/server/auth";
import { loadBooks, visibleBooks, visibleConcepts } from "@/engine/books";
import { Badge } from "@/components/ui/badge";
import { CardLink, RowLink } from "@/components/ui/card";
import { SparkIcon } from "@/components/ui/icons";

export const metadata = { title: "مكتبة الكتب" };
export const dynamic = "force-dynamic";

export default async function Books() {
  const a = await getActorFromCookies();
  const { books, concepts, drills } = loadBooks();
  const vis = visibleBooks(books, a.ageBand);
  const vc = visibleConcepts(concepts, books, a.ageBand);
  return (
    <>
      <div className="ref-hero">
        <p className="ref-hero-kicker">المكتبة البحثية</p>
        <h1 className="ref-hero-title">مكتبة الكتب</h1>
        <p className="ref-hero-hook">أربعة ملفات مغلقة على رف المحقق: نفتح منها الأفكار التي تنفع، ونترك الباقي مقفلاً لسبب مكتوب.</p>
        <div className="ref-hero-stats">
          <div><span className="ref-hero-stat-value">{vis.length}</span><span className="ref-hero-stat-label">كتاب</span></div>
          <div><span className="ref-hero-stat-value">{drills.length}</span><span className="ref-hero-stat-label">تمريناً</span></div>
        </div>
      </div>
      <ul className="list" aria-label="روابط المكتبة">
        <li><RowLink href="/books/drills" icon={<SparkIcon size={22} />} title="تمارين استدلال المشهد" hint={`${drills.length} سؤالاً بتغذية راجعة فورية`} /></li>
      </ul>
      <ul className="list">
        {vis.map((b) => (
          <li key={b.id}>
            <CardLink href={`/books/${b.id}`}>
              <b>{b.title_ar}</b>
              <p className="small dim-2">{b.hook_ar}</p>
              <p className="small dim">{b.authors_ar.join("، ")}{b.year ? ` · ${b.year}` : ""}</p>
              <span className="row small">
                <Badge>{vc.filter((c) => c.book_id === b.id).length} مفهوماً</Badge>
                <Badge outline>{b.included_count} فصلاً مشمولاً</Badge>
                <Badge outline>{b.excluded_count} مستبعداً</Badge>
              </span>
              <p className="small dim">{b.rights_note_ar}</p>
            </CardLink>
          </li>
        ))}
      </ul>
      {vis.length < books.length && <p className="small dim">كتاب إضافي مستبعد من هذه الواجهة لعدم ملاءمته للفئة العمرية ولرسالة المنصة.</p>}
    </>
  );
}
