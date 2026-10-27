import Link from "next/link";
import { loadTracks } from "@/engine/tracks";

export const metadata = { title: "الأكاديمية" };
export const dynamic = "force-dynamic";

export default function Academy() {
  const { tracks } = loadTracks();
  return (
    <div className="wrap stack">
      <h1>أكاديمية المحققين</h1>
      <p className="dim">ست مسارات قصيرة. كل درس بين ٣ و٧ دقائق، ينتهي بسؤال تطبيقي، وبعضها يمهّد لقضية بعينها.</p>
      {tracks.map((t) => (
        <section key={t.id} className="card stack" aria-labelledby={`t-${t.id}`}>
          <div className="row"><span className="avatar" aria-hidden>{t.glyph}</span><div><p className="kicker" style={{ margin: 0 }}>المسار {t.id}</p><h2 id={`t-${t.id}`} style={{ margin: 0 }}>{t.title_ar}</h2></div></div>
          <p className="dim">{t.summary_ar}</p>
          <ul className="stack" style={{ listStyle: "none", padding: 0 }}>
            {t.lessons.map((l) => <li key={l.id}><Link className="btn" style={{ inlineSize: "100%", justifyContent: "space-between" }} href={`/academy/${l.id}`}><span>{l.title_ar}</span><span className="small dim">{l.minutes} د</span></Link></li>)}
          </ul>
        </section>
      ))}
    </div>
  );
}
