import { notFound } from "next/navigation";
import Link from "next/link";
import { KIND_LABEL, loadKoNames, loadLabs } from "@/engine/labs";
import { loadKnowledge, visibleKos } from "@/engine/knowledge";
import { loadTracks } from "@/engine/tracks";
import { getActorFromCookies } from "@/server/auth";
import { LabRunner } from "@/components/LabRunner";
import { Badge } from "@/components/ui/badge";
import { Card, CardTitle, RowLink } from "@/components/ui/card";
import { LinkButton } from "@/components/ui/button";
import { DIFFICULTY_LABEL } from "../labels";

export const dynamic = "force-dynamic";

export default async function LabPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const f = loadLabs();
  const labIndex = f.playable.findIndex((l) => l.id === id);
  const lab = f.playable[labIndex];
  if (!lab) notFound();
  const nextLabRaw = f.playable[labIndex + 1] ?? null;
  const nextLab = nextLabRaw ? { id: nextLabRaw.id, title_ar: nextLabRaw.title_ar, skill_ar: nextLabRaw.skill_ar } : null;
  const a = await getActorFromCookies();
  const shown = new Set(visibleKos(loadKnowledge().kos, a.ageBand).map((k) => k.ko_id));
  const names = loadKoNames();
  const related = lab.ko_ids.filter((k) => shown.has(k) && names[k]);

  // Find linked Academy lessons via ko_ids
  const tracksFile = loadTracks();
  const koMap = new Map<string, { id: string; title_ar: string; track_id: string; track_title_ar: string }>();
  for (const track of tracksFile.tracks) {
    for (const lesson of track.lessons) {
      for (const ko of lesson.ko_refs) {
        if (!koMap.has(ko)) koMap.set(ko, { id: lesson.id, title_ar: lesson.title_ar, track_id: track.id, track_title_ar: track.title_ar });
      }
    }
  }
  const seenLessons = new Set<string>();
  const linkedLessons: { id: string; title_ar: string; track_id: string; track_title_ar: string }[] = [];
  for (const ko of lab.ko_ids) {
    const l = koMap.get(ko);
    if (l && !seenLessons.has(l.id)) { seenLessons.add(l.id); linkedLessons.push(l); }
  }
  return (
    <>
      <header className="ref-hero labs-hero"><p className="kicker">{lab.skill_ar}</p><h1 className="text-page-title">{lab.title_ar}</h1></header>
      <div className="lab-meta"><Badge>{KIND_LABEL[lab.kind]}</Badge><Badge outline>{DIFFICULTY_LABEL[lab.difficulty]}</Badge><Badge outline>نحو {lab.minutes} د</Badge><Badge tone="warning">محاكاة خيالية · تتطلب مراجعة خبراء</Badge></div>
      <aside className="lead-card" aria-label="سؤال الدخول"><p>{lab.hook_ar}</p></aside>
      <p className="dim-2">{lab.intro_ar}</p>
      <LabRunner key={lab.id} lab={lab} firstLesson={linkedLessons[0] ?? null} nextLab={nextLab} />
      {linkedLessons.length > 0 && (
        <Card as="section" aria-labelledby="lab-lessons-h">
          <h2 id="lab-lessons-h" className="text-section-title">دروس الأكاديمية المرتبطة</h2>
          <p className="small dim-2">تعمّق في نظرية هذا المختبر عبر درس قصير.</p>
          <ul className="case-linked-lessons-list" style={{ marginBlockStart: "0.6rem" }}>
            {linkedLessons.map((l) => (
              <li key={l.id}>
                <Link href={`/academy/${l.id}`} className="case-linked-lesson-row">
                  <span className="case-linked-lesson-id">{l.id}</span>
                  <span className="case-linked-lesson-title">{l.title_ar}</span>
                  <span className="case-linked-lesson-meta small dim">{l.track_title_ar}</span>
                  <span className="case-linked-lesson-chev" aria-hidden>←</span>
                </Link>
              </li>
            ))}
          </ul>
        </Card>
      )}
      {related.length > 0 && (
        <Card as="section" aria-label="للتوسع">
          <CardTitle level={2}>للتوسع في الموسوعة</CardTitle>
          <ul className="list">{related.map((k) => <li key={k}><RowLink href={`/knowledge/${k}`} title={names[k]!} /></li>)}</ul>
        </Card>
      )}
      <LinkButton variant="outline" href="/labs">كل المختبرات</LinkButton>
    </>
  );
}
