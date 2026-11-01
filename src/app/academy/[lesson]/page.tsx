import Link from "next/link";
import { notFound } from "next/navigation";
import { loadTracks, lessonById } from "@/engine/tracks";
import { loadLabs } from "@/engine/labs";
import { Practice } from "@/components/Practice";
import { LinkButton } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardTitle } from "@/components/ui/card";
import { LessonProgressTracker } from "@/components/academy/LessonProgressTracker";


import type { Metadata } from "next";

export async function generateMetadata({ params }: { params: Promise<{ lesson: string }> }): Promise<Metadata> {
  const { lesson } = await params;
  const file = loadTracks();
  const l = lessonById(file, lesson);
  if (!l) return {};
  return {
    title: l.title_ar,
    description: l.intro_ar?.slice(0, 160) ?? undefined,
    openGraph: { title: l.title_ar, description: l.intro_ar?.slice(0, 160) ?? undefined, type: "article", siteName: "Detective Academy" },
    twitter: { card: "summary", title: l.title_ar },
    alternates: { canonical: `/academy/${l.id}` },
  };
}

export const dynamic = "force-dynamic";

export default async function Lesson({ params }: { params: Promise<{ lesson: string }> }) {
  const { lesson } = await params;
  const file = loadTracks();
  const l = lessonById(file, lesson);
  if (!l) notFound();
  const track = file.tracks.find((t) => t.lessons.some((x) => x.id === l.id))!;
  const idx = track.lessons.findIndex((x) => x.id === l.id);
  const next = track.lessons[idx + 1];

  // Find labs that share any ko_ref with this lesson
  const labsFile = loadLabs();
  const koSet = new Set(l.ko_refs);
  const relatedLabs = labsFile.playable.filter((lab) => lab.ko_ids.some((k) => koSet.has(k)));

  return (
    <article className="stack-lg">
      {/* Auto-mark lesson done for logged-in users */}
      <LessonProgressTracker lessonId={l.id} />

      <header className="ref-hero academy-hero">
        <p className="kicker">المسار {track.id} · {track.title_ar} · {l.minutes} دقائق</p>
        <h1 className="text-page-title">{l.title_ar}</h1>
      </header>
      <p className="narrative dim-2">{l.intro_ar}</p>
      <div className="stack">{l.body_ar.map((p, i) => <p key={i}>{p}</p>)}</div>
      <section className="paper" aria-label="مثال محلول"><h3>مثال محلول</h3>{l.worked_example_ar}</section>
      <Card as="section"><CardTitle level={3}>خطأ شائع</CardTitle><p>{l.common_mistake_ar}</p></Card>
      <Practice practice={l.practice} />

      {/* ── Related labs ─────────────────────────────────────── */}
      {relatedLabs.length > 0 && (
        <Card as="section" aria-labelledby="lesson-labs-h">
          <h2 id="lesson-labs-h" className="text-section-title">مختبرات تدريب مرتبطة</h2>
          <p className="small dim-2">طبّق هذه المهارة في بيئة محاكاة آمنة.</p>
          <ul className="case-linked-lessons-list" style={{ marginBlockStart: "0.6rem" }}>
            {relatedLabs.map((lab) => (
              <li key={lab.id}>
                <Link href={`/labs/${lab.id}`} className="case-linked-lesson-row">
                  <Badge className="case-linked-lesson-id">{lab.kind}</Badge>
                  <span className="case-linked-lesson-title">{lab.title_ar}</span>
                  <span className="case-linked-lesson-meta small dim">{lab.skill_ar} · {lab.minutes} د</span>
                  <span className="case-linked-lesson-chev" aria-hidden>←</span>
                </Link>
              </li>
            ))}
          </ul>
        </Card>
      )}

      <div className="stack-sm">
        {l.case_link ? <LinkButton variant="primary" size="lg" block href={`/case/${l.case_link}`}>طبّق ذلك في قضية</LinkButton> : null}
        {next ? <LinkButton variant={l.case_link ? "secondary" : "primary"} size={l.case_link ? "md" : "lg"} block href={`/academy/${next.id}`}>الدرس التالي</LinkButton> : <LinkButton variant={l.case_link ? "secondary" : "primary"} block href="/academy">كل المسارات</LinkButton>}
      </div>
    </article>
  );
}
