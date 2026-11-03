import { getActorFromCookies } from "@/server/auth";
import { progressFor } from "@/server/progress";
import HomeClient, { type HomeData } from "./HomeClient";

export const dynamic = "force-dynamic";

export default async function HomePage() {
  let initial: HomeData | null = null;
  try {
    const actor = await getActorFromCookies();
    // No age band yet → the age gate is showing; let the client path handle it.
    if (actor.ageBand) initial = (await progressFor(actor, undefined)) as unknown as HomeData;
  } catch { initial = null; }
  return <HomeClient initial={initial} />;
}
