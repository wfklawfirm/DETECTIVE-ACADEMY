import { route } from "@/server/api";
import { getActor } from "@/server/auth";
import { listPlayable } from "@/server/content";
import { HttpError, json } from "@/server/http";

export const GET = route(async (req) => {
  const a = await getActor(req);
  if (!a.ageBand) throw new HttpError(403, "age_required", "حدّد فئتك العمرية أولاً");
  return json({ cases: await listPlayable(a.ageBand) });
});
