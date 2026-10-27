import { readFileSync } from "node:fs";
import { join } from "node:path";

export const metadata = { title: "المهارات وأنماط الألغاز" };
export const dynamic = "force-dynamic";
interface F { skills: { id: string; title_ar: string; definition_ar: string; scenario_ar: string; achievement_ar: string; common_error_ar: string }[]; patterns: { id: string; title_ar: string; hook_ar: string; fair_play_ar: string; constraint_ar: string }[] }

export default function Skills() {
  const f = JSON.parse(readFileSync(join(process.cwd(), "content/knowledge/skills_patterns.json"), "utf8")) as F;
  return (
    <div className="wrap stack">
      <h1>المهارات وأنماط الألغاز</h1>
      <p className="dim">هذا هو الإطار الذي نبني عليه القضايا: أربع وعشرون مهارة تحقيق، وعشرون نمطاً من الألغاز العادلة. مسودة تحريرية أصلية من فريق أثر، لم تُراجع من خبراء بعد.</p>
      <h2>المهارات ({f.skills.length})</h2>
      <ul className="stack" style={{ listStyle: "none", padding: 0 }}>
        {f.skills.map((s) => (
          <li key={s.id} className="card stack" style={{ gap: 4 }}>
            <b>{s.title_ar}</b><span>{s.definition_ar}</span>
            <span className="small dim">مثال: {s.scenario_ar}</span>
            <span className="small">علامة الإتقان: {s.achievement_ar}</span>
            <span className="small dim">الخطأ الشائع: {s.common_error_ar}</span>
          </li>
        ))}
      </ul>
      <h2>أنماط الألغاز ({f.patterns.length})</h2>
      <p className="dim">كل نمط يلتزم بشرطين: أن تكون القرائن في متناول اللاعب، وألّا نُكافئ القفز إلى الاستنتاج.</p>
      <ul className="stack" style={{ listStyle: "none", padding: 0 }}>
        {f.patterns.map((p) => (
          <li key={p.id} className="card stack" style={{ gap: 4 }}>
            <b>{p.title_ar}</b><span>{p.hook_ar}</span>
            <span className="small dim">العدالة: {p.fair_play_ar}</span><span className="small dim">القيد: {p.constraint_ar}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
