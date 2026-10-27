import { readFileSync } from "node:fs";
import { join } from "node:path";
import { Card, PageHead } from "@/components/ui/card";

export const metadata = { title: "المهارات وأنماط الألغاز" };
export const dynamic = "force-dynamic";
interface F { skills: { id: string; title_ar: string; definition_ar: string; scenario_ar: string; achievement_ar: string; common_error_ar: string }[]; patterns: { id: string; title_ar: string; hook_ar: string; fair_play_ar: string; constraint_ar: string }[] }

export default function Skills() {
  const f = JSON.parse(readFileSync(join(process.cwd(), "content/knowledge/skills_patterns.json"), "utf8")) as F;
  return (
    <>
      <PageHead title="المهارات وأنماط الألغاز" lead={`هذا هو الإطار الذي نبني عليه القضايا: ${f.skills.length} مهارة تحقيق، و${f.patterns.length} نمطاً من الألغاز العادلة. مسودة تحريرية أصلية من فريق أثر، لم تُراجع من خبراء بعد.`} />
      <section className="stack"><h2 className="text-section-title">المهارات ({f.skills.length})</h2>
      <ul className="list grid-2" style={{ display: "grid" }}>
        {f.skills.map((s) => (
          <li key={s.id}><Card flat>
            <b>{s.title_ar}</b><span>{s.definition_ar}</span>
            <span className="small dim">مثال: {s.scenario_ar}</span>
            <span className="small">علامة الإتقان: {s.achievement_ar}</span>
            <span className="small dim">الخطأ الشائع: {s.common_error_ar}</span>
          </Card></li>
        ))}
      </ul></section>
      <section className="stack"><h2 className="text-section-title">أنماط الألغاز ({f.patterns.length})</h2>
      <p className="dim-2">كل نمط يلتزم بشرطين: أن تكون القرائن في متناول اللاعب، وألّا نُكافئ القفز إلى الاستنتاج.</p>
      <ul className="list grid-2" style={{ display: "grid" }}>
        {f.patterns.map((p) => (
          <li key={p.id}><Card flat>
            <b>{p.title_ar}</b><span>{p.hook_ar}</span>
            <span className="small dim">العدالة: {p.fair_play_ar}</span><span className="small dim">القيد: {p.constraint_ar}</span>
          </Card></li>
        ))}
      </ul></section>
    </>
  );
}
