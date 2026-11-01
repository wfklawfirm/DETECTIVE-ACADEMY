import { getActorFromCookies } from "@/server/auth";
import { drillsFor, loadBooks } from "@/engine/books";

import { DrillRunner } from "@/components/books/DrillRunner";

import type { Metadata } from "next";
export const metadata: Metadata = {
  title: "تمارين استدلال المشهد",
  description: "تمارين قصيرة على استدلال المشهد — مشاهد خيالية بجواب واحد دقيق تتمرّن فيه على قراءة الأدلة قبل الحكم.",
  robots: { index: false, follow: false },
  openGraph: { title: "تمارين استدلال المشهد · Detective Academy", description: "مشاهد خيالية قصيرة لتمرين الاستدلال.", type: "website", siteName: "Detective Academy" },
  twitter: { card: "summary", title: "تمارين استدلال المشهد · Detective Academy" },
};
export const dynamic = "force-dynamic";

export default async function Drills() {
  const a = await getActorFromCookies();
  const { drills } = loadBooks();
  const items = drillsFor(drills, a.ageBand).map(({ id, skill, scenario_ar, question_ar, options, answer_id, explanation_ar }) => ({ id, skill, scenario_ar, question_ar, options, answer_id, explanation_ar }));
  return (
    <>
      <div className="ref-hero">
        <p className="ref-hero-kicker">تمرين</p>
        <h1 className="ref-hero-title">تمارين استدلال المشهد</h1>
        <p className="ref-hero-hook">مشاهد خيالية قصيرة، وجواب واحد هو الأدق: افحص ما تراه قبل أن تحكم.</p>
      </div>
      <DrillRunner drills={items} />
    </>
  );
}
