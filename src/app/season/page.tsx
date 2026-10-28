import { loadResolvedSeason } from "@/engine/seasons-load";
import { SeasonView } from "@/components/season/SeasonView";

export const metadata = { title: "الموسم الأول" };
export const dynamic = "force-dynamic";

export default function SeasonPage() {
  const { season, episodes } = loadResolvedSeason();
  return <SeasonView season={season} episodes={episodes} />;
}
