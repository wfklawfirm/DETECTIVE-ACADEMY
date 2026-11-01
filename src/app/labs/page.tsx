import { KIND_LABEL, loadLabs, type LabKind } from "@/engine/labs";
import { Card } from "@/components/ui/card";
import { DIFFICULTY_LABEL } from "./labels";
import { LabsClient } from "./LabsClient";

import type { Metadata } from "next";
export const metadata: Metadata = {
  title: "مختبرات آمنة",
  description: "تمارين تفاعلية قصيرة في علم الأدلة والاستدلال — صُمّمت لتبني مهارات تحقيقية حقيقية بسياقات خيالية آمنة.",
  openGraph: { title: "مختبرات آمنة · Detective Academy", description: "تمارين تفاعلية قصيرة في علم الأدلة والاستدلال.", type: "website", siteName: "Detective Academy" },
  twitter: { card: "summary", title: "مختبرات آمنة · Detective Academy" },
  alternates: { canonical: "/labs" },
};
export const dynamic = "force-dynamic";

export default function Labs() {
  const f = loadLabs();
  const playable = new Map(f.playable.map((l) => [l.id, l]));
  const kinds = Object.keys(KIND_LABEL) as LabKind[];

  // Build grouped items for the client component
  const groups: { kind: LabKind; label: string; items: { id: string; title_ar: string; skill_ar: string; interaction_ar: string; difficulty: number; minutes: number }[] }[] = [];
  for (const k of kinds) {
    const group = f.catalogue.filter((c) => playable.get(c.id)?.kind === k);
    if (!group.length) continue;
    groups.push({
      kind: k,
      label: KIND_LABEL[k],
      items: group.map((c) => {
        const l = playable.get(c.id)!;
        return { id: l.id, title_ar: l.title_ar, skill_ar: l.skill_ar, interaction_ar: c.interaction_ar, difficulty: l.difficulty, minutes: l.minutes };
      }),
    });
  }

  const allIds = f.playable.map((l) => l.id);

  return (
    <>
      <div className="ref-hero">
        <p className="ref-hero-kicker">تدريب بلا خطر</p>
        <h1 className="ref-hero-title">مختبرات آمنة</h1>
        <p className="ref-hero-hook">هل تستطيع أن تحكم على دليل دون أن تتجاوز ما يقوله؟ تمارين قصيرة بسجلات خيالية، كل واحد يدرّب مهارة واحدة.</p>
        <div className="ref-hero-stats">
          <div><span className="ref-hero-stat-value">{f.playable.length}</span><span className="ref-hero-stat-label">تمريناً متاحاً</span></div>
          <div><span className="ref-hero-stat-value">{f.catalogue.length}</span><span className="ref-hero-stat-label">في الكتالوج</span></div>
        </div>
      </div>

      <LabsClient groups={groups} allIds={allIds} difficultyLabel={DIFFICULTY_LABEL} />

      {f.declined.length > 0 && (
        <Card as="section" aria-labelledby="declined">
          <h2 id="declined" className="text-section-title">مختبرات لم نبنِها، ولماذا</h2>
          <ul className="stack-sm">{f.declined.map((d) => <li key={d.title_ar}><b>{d.title_ar}.</b> <span className="small dim">{d.reason_ar}</span></li>)}</ul>
        </Card>
      )}
    </>
  );
}
