import { route } from "@/server/api";
import { getActor, requireRole } from "@/server/auth";
import { q1 } from "@/server/db";
import { json } from "@/server/http";

export const GET = route(async (req) => {
  requireRole(await getActor(req), ["admin"]);

  const [users, cases, plays, lessons, casesByStatus] = await Promise.all([
    q1<{ total: number; today: number }>(
      "SELECT COUNT(*) AS total, SUM(CASE WHEN DATE(created_at) = DATE('now') THEN 1 ELSE 0 END) AS today FROM users"
    ),
    q1<{ total: number; published: number; in_review: number; draft: number }>(
      "SELECT COUNT(*) AS total, SUM(CASE WHEN status='published' THEN 1 ELSE 0 END) AS published, SUM(CASE WHEN status='in_review' THEN 1 ELSE 0 END) AS in_review, SUM(CASE WHEN status='draft' THEN 1 ELSE 0 END) AS draft FROM case_versions"
    ),
    q1<{ total: number; completed: number }>(
      "SELECT COUNT(*) AS total, SUM(CASE WHEN state='resolved' THEN 1 ELSE 0 END) AS completed FROM plays"
    ),
    q1<{ total: number }>(
      "SELECT COUNT(*) AS total FROM lesson_progress"
    ),
    null,
  ]);

  return json({
    users: { total: users?.total ?? 0, today: users?.today ?? 0 },
    cases: { total: cases?.total ?? 0, published: cases?.published ?? 0, in_review: cases?.in_review ?? 0, draft: cases?.draft ?? 0 },
    plays: { total: plays?.total ?? 0, completed: plays?.completed ?? 0 },
    lessons_done: lessons?.total ?? 0,
  });
}, { limit: 30, key: "studio-stats" });
