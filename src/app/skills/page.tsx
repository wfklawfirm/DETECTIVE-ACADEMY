import { readFileSync } from "node:fs";
import { join } from "node:path";

export const metadata = { title: "المهارات وأنماط الألغاز" };
export const dynamic = "force-dynamic";

interface Skill    { id: string; title_ar: string; definition_ar: string; scenario_ar: string; achievement_ar: string; common_error_ar: string }
interface Pattern  { id: string; title_ar: string; hook_ar: string; fair_play_ar: string; constraint_ar: string }
interface F        { skills: Skill[]; patterns: Pattern[] }

export default function Skills() {
  const f = JSON.parse(readFileSync(join(process.cwd(), "content/knowledge/skills_patterns.json"), "utf8")) as F;
  return (
    <>
      {/* ── Hero ─────────────────────────────────────────────── */}
      <div className="skills-hero">
        <p className="skills-hero-kicker">إطار التحقيق</p>
        <h1 className="skills-hero-title">المهارات وأنماط الألغاز</h1>
        <p className="skills-hero-lead">
          {f.skills.length} مهارة تحقيقية و{f.patterns.length} نمطاً من الألغاز العادلة —
          الإطار الذي تُبنى عليه كل قضية في Detective Academy.
        </p>
        <div className="skills-hero-note">
          <span className="skills-hero-note-mark" aria-hidden>✦</span>
          مسودة تحريرية أصلية من فريق التطوير، لم تُراجع من خبراء بعد.
        </div>
      </div>

      {/* ── Skills grid ──────────────────────────────────────── */}
      <section className="skills-section">
        <div className="skills-section-header">
          <h2 className="skills-section-title">مهارات التحقيق</h2>
          <span className="skills-count">{f.skills.length}</span>
        </div>
        <ul className="skills-grid">
          {f.skills.map((s) => (
            <li key={s.id} className="skill-card">
              <span className="skill-card-id">{s.id}</span>
              <strong className="skill-card-name">{s.title_ar}</strong>
              <p className="skill-card-def">{s.definition_ar}</p>
              <div className="skill-card-footer">
                <span className="skill-card-row">
                  <span className="skill-card-row-label">مثال</span>
                  {s.scenario_ar}
                </span>
                <span className="skill-card-row skill-card-row--teal">
                  <span className="skill-card-row-label">علامة الإتقان</span>
                  {s.achievement_ar}
                </span>
                <span className="skill-card-row skill-card-row--dim">
                  <span className="skill-card-row-label">الخطأ الشائع</span>
                  {s.common_error_ar}
                </span>
              </div>
            </li>
          ))}
        </ul>
      </section>

      {/* ── Patterns grid ────────────────────────────────────── */}
      <section className="skills-section">
        <div className="skills-section-header">
          <h2 className="skills-section-title">أنماط الألغاز</h2>
          <span className="skills-count">{f.patterns.length}</span>
        </div>
        <p className="skills-section-note">
          كل نمط يلتزم بشرطين: أن تكون القرائن في متناول اللاعب، وألّا نُكافئ القفز إلى الاستنتاج.
        </p>
        <ul className="skills-grid">
          {f.patterns.map((p) => (
            <li key={p.id} className="skill-card skill-card--pattern">
              <span className="skill-card-id">{p.id}</span>
              <strong className="skill-card-name">{p.title_ar}</strong>
              <p className="skill-card-def">{p.hook_ar}</p>
              <div className="skill-card-footer">
                <span className="skill-card-row skill-card-row--teal">
                  <span className="skill-card-row-label">العدالة</span>
                  {p.fair_play_ar}
                </span>
                <span className="skill-card-row skill-card-row--dim">
                  <span className="skill-card-row-label">القيد</span>
                  {p.constraint_ar}
                </span>
              </div>
            </li>
          ))}
        </ul>
      </section>
    </>
  );
}
