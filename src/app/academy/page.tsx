import Link from "next/link";
import { AcademyProgressOverlay } from "@/components/academy/AcademyProgressOverlay";
import { AcademyProgressStrip } from "@/components/academy/AcademyProgressStrip";
import { loadTracks } from "@/engine/tracks";
import type { Track, Lesson } from "@/engine/tracks";
import { Badge } from "@/components/ui/badge";
import { RowLink } from "@/components/ui/card";

import type { Metadata } from "next";
export const metadata: Metadata = {
  title: "الأكاديمية",
  description: "٣٦ درساً قصيراً في ٦ مسارات تحقيقية — تعلّم كيف تقرأ الأدلة، وتستجوب الشهود، وتبني استنتاجات تستحق الثقة.",
  openGraph: { title: "الأكاديمية · Detective Academy", description: "٣٦ درساً قصيراً في ٦ مسارات تحقيقية.", type: "website", siteName: "Detective Academy" },
  twitter: { card: "summary", title: "الأكاديمية · Detective Academy" },
  alternates: { canonical: "/academy" },
};
export const revalidate = 86400;

export default function Academy() {
  const { tracks } = loadTracks();
  const totalLessons = tracks.reduce((n: number, t: Track) => n + t.lessons.length, 0);

  return (
    <>
      {/* Progress overlay — marks completed lessons client-side */}
      <AcademyProgressOverlay
        lessonIds={tracks.flatMap((t: Track) => t.lessons.map((l: Lesson) => l.id))}
        trackMap={Object.fromEntries(tracks.map((t: Track) => [t.id, t.lessons.map((l: Lesson) => l.id)]))}
      />

      {/* ── Cinematic hero ──────────────────────────────────────── */}
      <header className="academy-hero">
        <div className="academy-hero-inner">
          <div className="academy-hero-text">
            <p className="academy-hero-kicker">أكاديمية المحقق · مسارات التدريب</p>
            <h1 className="academy-hero-title">مسارات الاستدلال</h1>
            <p className="academy-hero-sub">
              {tracks.length} مسارات · {totalLessons} درساً قصيراً · كل درس ينتهي بسؤال تطبيقي.
            </p>
          </div>
          <div className="academy-hero-badge" aria-hidden>
            <span className="academy-hero-glyph">🎓</span>
          </div>
        </div>
      </header>

      {/* ── Overall progress strip ────────────────────────────── */}
      <AcademyProgressStrip total={totalLessons} />

      {/* ── Educators note ─────────────────────────────────────── */}
      <div className="academy-educators-note">
        <span className="academy-educators-icon" aria-hidden>👩‍🏫</span>
        <p className="small dim-2">
          تدرّس مجموعة؟{" "}
          <Link href="/academy/educators" className="academy-educators-link">
            اطّلع على دليل المعلّم
          </Link>
          {" "}· أي لغز أولاً: «من أخذ الدفتر؟» أم «لماذا أجمعوا عليه؟»
        </p>
      </div>

      {/* ── Tracks ─────────────────────────────────────────────── */}
      <div className="academy-tracks">
        {tracks.map((t: Track) => (
          <section key={t.id} data-track-id={t.id} className="track-card" aria-labelledby={`t-${t.id}`}>
            {/* Track header */}
            <div className="track-card-header">
              <div className="track-card-glyph" aria-hidden>{t.glyph}</div>
              <div className="track-card-meta">
                <p className="track-card-kicker">المسار {t.id}</p>
                <h2 id={`t-${t.id}`} className="track-card-title">{t.title_ar}</h2>
              </div>
              <span className="track-card-count">{t.lessons.length} دروس</span>
            </div>

            <p className="track-card-summary">{t.summary_ar}</p>
            <div className="track-progress-wrap" aria-hidden>
              <div className="track-progress-bar">
                <div className="track-progress-bar-fill" />
              </div>
              <span className="track-progress-count" />
            </div>

            {/* Lessons: paths first — only the first path opens by default */}
            <details className="track-lessons-details" open={t.id === tracks[0]?.id}>
            <summary className="track-lessons-summary">دروس المسار ({t.lessons.length})</summary>
            <ul className="list track-lessons">
              {t.lessons.map((l: Lesson) => (
                <li key={l.id} data-lesson-id={l.id}>
                  <RowLink
                    href={`/academy/${l.id}`}
                    title={l.title_ar}
                    trailing={
                      <>
                        <Badge>{l.minutes} د</Badge>
                        {l.case_link && <Badge tone="info">قضية</Badge>}
                      </>
                    }
                  />
                </li>
              ))}
            </ul>
            </details>
          </section>
        ))}
      </div>
    </>
  );
}
