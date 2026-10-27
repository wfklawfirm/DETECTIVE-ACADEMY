import Link from "next/link";
import { notFound } from "next/navigation";
import { loadTracks, lessonById } from "@/engine/tracks";
import { Practice } from "@/components/Practice";

export const dynamic = "force-dynamic";

export default async function Lesson({ params }: { params: Promise<{ lesson: string }> }) {
  const { lesson } = await params;
  const file = loadTracks();
  const l = lessonById(file, lesson);
  if (!l) notFound();
  const track = file.tracks.find((t) => t.lessons.some((x) => x.id === l.id))!;
  const idx = track.lessons.findIndex((x) => x.id === l.id);
  const next = track.lessons[idx + 1];
  return (
    <article className="wrap-narrow stack">
      <p className="kicker">المسار {track.id} · {track.title_ar} · {l.minutes} دقائق</p>
      <h1>{l.title_ar}</h1>
      <p className="dim" style={{ fontFamily: "var(--f-display)", fontSize: "1.3rem" }}>{l.intro_ar}</p>
      {l.body_ar.map((p, i) => <p key={i}>{p}</p>)}
      <section className="paper"><h3>مثال محلول</h3>{l.worked_example_ar}</section>
      <section className="card"><h3>خطأ شائع</h3><p style={{ margin: 0 }}>{l.common_mistake_ar}</p></section>
      <Practice practice={l.practice} />
      <div className="row">
        {l.case_link && <Link className="btn primary" href={`/case/${l.case_link}`}>طبّق ذلك في قضية</Link>}
        {next ? <Link className="btn" href={`/academy/${next.id}`}>الدرس التالي</Link> : <Link className="btn" href="/academy">كل المسارات</Link>}
      </div>
    </article>
  );
}
