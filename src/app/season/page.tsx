import { loadResolvedSeason } from "@/engine/seasons-load";
import { SeasonView } from "@/components/season/SeasonView";

import type { Metadata } from "next";
export const metadata: Metadata = {
  title: "الموسم الأول",
  description: "ثماني قضايا بترتيب مقترح — كل حلقة تضيف عادة تفكير. تجربة متكاملة لبناء عقل تحقيقي.",
  openGraph: { title: "الموسم الأول · Detective Academy", description: "ثماني قضايا بترتيب مقترح — كل حلقة تضيف عادة تفكير.", type: "website", siteName: "Detective Academy" },
  twitter: { card: "summary", title: "الموسم الأول · Detective Academy" },
  alternates: { canonical: "/season" },
};
export const revalidate = 86400;

export default function SeasonPage() {
  const { season, episodes } = loadResolvedSeason();
  return <SeasonView season={season} episodes={episodes} />;
}
