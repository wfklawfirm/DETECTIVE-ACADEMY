import { readFileSync } from "node:fs";
import { join } from "node:path";
import { loadResolvedSeason } from "@/engine/seasons-load";
import koNames from "../../../../content/knowledge/ko_names.json";
import { Badge } from "@/components/ui/badge";
import { Callout } from "@/components/ui/feedback";
import { Card } from "@/components/ui/card";
import { SearchIcon } from "@/components/ui/icons";

export const metadata = { title: "دليل المعلّم" };
export const dynamic = "force-dynamic";

interface Meta { title: string; minutes: number; band: string; skills: string[] }
function meta(id: string): Meta | null {
  try {
    const dir = join(process.cwd(), "content", "cases");
    const core = JSON.parse(readFileSync(join(dir, `${id}.json`), "utf8")) as { meta: { title_ar: string; estimated_minutes: number; age_band: string }; learning_objectives: { skill_ko_ref: string }[] };
    const names = koNames as Record<string, string>;
    const sk = [...new Set(core.learning_objectives.map((o) => o.skill_ko_ref))].map((k) => names[k] ?? k);
    return { title: core.meta.title_ar, minutes: core.meta.estimated_minutes, band: core.meta.age_band, skills: sk };
  } catch { return null; }
}

/** Adult-facing class guide. Static curriculum information only: it reads no play data and shows no student data. */
export default function Educators() {
  const { season, episodes } = loadResolvedSeason();
  return (
    <>
      <div className="ref-hero">
        <p className="ref-hero-kicker">للمعلّمين والمشرفين</p>
        <h1 className="ref-hero-title">دليل المعلّم</h1>
        <p className="ref-hero-hook">كيف تستعمل «{season.title_ar}» مع مجموعة؟ نعرض المنهج فقط، لا بيانات أي طالب.</p>
      </div>
      <aside className="lead-card" aria-label="تلميح">
        <span className="mark"><SearchIcon size={18} />سؤال للصف</span>
        <p>اعرضوا على الصف ملفاً فيه شاهدان يتفقان بثقة، ثم اسألوهم: ما الذي سيجعلنا نصدّقهما؟</p>
      </aside>
      <Callout tone="warning" title="حالة المحتوى">هذا الترتيب مقترح من فريقنا ولم يُجرَّب مع طلاب ولم يراجعه خبير تربوي بعد. استعمله اقتراحاً وعدّله بخبرتك.</Callout>
      <Card as="section" aria-labelledby="ed-how">
        <h2 id="ed-how" className="card-title">طريقة مقترحة للحصة</h2>
        <ol className="small stack-sm" style={{ paddingInlineStart: "1.2rem" }}>
          <li>قبل الحصة: اقرأ فكرة الحلقة أدناه، وجرّب القضية بنفسك مرة.</li>
          <li>افتتاحية قصيرة: اقرأوا السطر التشويقي واطلبوا من كل طالب تخمينه الأول مكتوباً دون مناقشة.</li>
          <li>الطلاب يلعبون القضية فردياً أو بثنائيات. لا نعرض لك نتائجهم، ولا نقارن بينهم.</li>
          <li>الختام: كل طالب يشرح ما غيّر رأيه، ثم تناقشون فكرة الحلقة.</li>
        </ol>
        <p className="small dim">المنصة لا تُظهر للمعلّم أسماء أو درجات أو تقدّماً فردياً. هذا قرار مقصود لحماية الطلاب، وليس نقصاً.</p>
      </Card>
      <ol className="list" style={{ listStyle: "none", padding: 0 }}>
        {episodes.filter((e) => e.kind !== "bonus").map((e) => (
          <li key={e.id}>
            <Card as="article" aria-labelledby={`ed-${e.id}`}>
              <h2 id={`ed-${e.id}`} className="card-title">{e.title_ar}</h2>
              <p className="small"><b>فكرة الحلقة: </b>{e.principle_ar}</p>
              <p className="small dim-2"><b>سؤال تشويقي: </b>{e.hook_ar}</p>
              {e.case_ids.map((id) => { const m = meta(id); return m ? (
                <div key={id} className="stack-sm">
                  <div className="row"><b>{m.title}</b><Badge>{m.minutes} دقيقة</Badge><Badge tone="info">{m.band === "all" ? "كل الأعمار" : m.band}</Badge></div>
                  <p className="small dim">المهارات: {m.skills.join("، ")}</p>
                </div>
              ) : null; })}
              {e.link && <p className="small dim">نشاط قصير: {e.link.label_ar}.</p>}
            </Card>
          </li>
        ))}
      </ol>
    </>
  );
}
