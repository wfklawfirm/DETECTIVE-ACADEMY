import Link from "next/link";
import { loadTracks } from "@/engine/tracks";
import { Badge } from "@/components/ui/badge";
import { Card, PageHead, RowLink } from "@/components/ui/card";

export const metadata = { title: "الأكاديمية" };
export const dynamic = "force-dynamic";

export default function Academy() {
  const { tracks } = loadTracks();
  return (
    <>
      <PageHead title="أكاديمية المحققين" lead={`${tracks.length === 6 ? "ست" : tracks.length} مسارات قصيرة. كل درس بين ٣ و٧ دقائق، ينتهي بسؤال تطبيقي، وبعضها يمهّد لقضية بعينها.`} />
      <Card as="section" flat aria-label="للمعلّمين"><p className="small">تدرّس مجموعة؟ <Link href="/academy/educators">اطّلع على دليل المعلّم</Link>. أي لغز أولاً: «من أخذ الدفتر؟» أم «لماذا أجمعوا عليه؟»</p></Card>
      {tracks.map((t) => (
        <Card as="section" key={t.id} aria-labelledby={`t-${t.id}`}>
          <div className="row" style={{ flexWrap: "nowrap" }}>
            <span className="avatar" aria-hidden>{t.glyph}</span>
            <div className="grow"><p className="kicker">المسار {t.id}</p><h2 id={`t-${t.id}`} className="text-section-title">{t.title_ar}</h2></div>
          </div>
          <p className="small dim-2">{t.summary_ar}</p>
          <ul className="list">
            {t.lessons.map((l) => <li key={l.id}><RowLink href={`/academy/${l.id}`} title={l.title_ar} trailing={<><Badge>{l.minutes} د</Badge>{l.case_link && <Badge tone="info">قضية</Badge>}</>} /></li>)}
          </ul>
        </Card>
      ))}
    </>
  );
}
