import { notFound } from "next/navigation";
import { KIND_LABEL, loadKoNames, loadLabs } from "@/engine/labs";
import { loadKnowledge, visibleKos } from "@/engine/knowledge";
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
  const lab = f.playable.find((l) => l.id === id);
  if (!lab) notFound();
  const a = await getActorFromCookies();
  const shown = new Set(visibleKos(loadKnowledge().kos, a.ageBand).map((k) => k.ko_id));
  const names = loadKoNames();
  const related = lab.ko_ids.filter((k) => shown.has(k) && names[k]);
  return (
    <>
      <header className="ref-hero labs-hero"><p className="kicker">{lab.skill_ar}</p><h1 className="text-page-title">{lab.title_ar}</h1></header>
      <div className="lab-meta"><Badge>{KIND_LABEL[lab.kind]}</Badge><Badge outline>{DIFFICULTY_LABEL[lab.difficulty]}</Badge><Badge outline>نحو {lab.minutes} د</Badge><Badge tone="warning">محاكاة خيالية · تتطلب مراجعة خبراء</Badge></div>
      <aside className="lead-card" aria-label="سؤال الدخول"><p>{lab.hook_ar}</p></aside>
      <p className="dim-2">{lab.intro_ar}</p>
      <LabRunner key={lab.id} lab={lab} />
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
