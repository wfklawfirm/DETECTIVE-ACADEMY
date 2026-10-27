import { notFound } from "next/navigation";
import { loadTracks, lessonById } from "@/engine/tracks";
import { Practice } from "@/components/Practice";
import { LinkButton } from "@/components/ui/button";
import { Card, CardTitle } from "@/components/ui/card";

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
    <article className="stack-lg">
      <header className="page-head">
        <p className="kicker">المسار {track.id} · {track.title_ar} · {l.minutes} دقائق</p>
        <h1 className="text-page-title">{l.title_ar}</h1>
      </header>
      <p className="narrative dim-2">{l.intro_ar}</p>
      <div className="stack">{l.body_ar.map((p, i) => <p key={i}>{p}</p>)}</div>
      <section className="paper" aria-label="مثال محلول"><h3>مثال محلول</h3>{l.worked_example_ar}</section>
      <Card as="section"><CardTitle level={3}>خطأ شائع</CardTitle><p>{l.common_mistake_ar}</p></Card>
      <Practice practice={l.practice} />
      <div className="stack-sm">
        {l.case_link ? <LinkButton variant="primary" size="lg" block href={`/case/${l.case_link}`}>طبّق ذلك في قضية</LinkButton> : null}
        {next ? <LinkButton variant={l.case_link ? "secondary" : "primary"} size={l.case_link ? "md" : "lg"} block href={`/academy/${next.id}`}>الدرس التالي</LinkButton> : <LinkButton variant={l.case_link ? "secondary" : "primary"} block href="/academy">كل المسارات</LinkButton>}
      </div>
    </article>
  );
}
