import { loadAssets } from "@/engine/assets";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";

export const metadata = { title: "مكتبة الأصوات" };
export const dynamic = "force-dynamic";

export default function Sounds() {
  const snd = loadAssets().filter((a) => a.kind === "audio");
  const groups = new Map<string, typeof snd>();
  for (const a of snd) groups.set(a.collection ?? "other", [...(groups.get(a.collection ?? "other") ?? []), a]);
  return (
    <>
      <div className="ref-hero">
        <p className="ref-hero-kicker">المؤثرات الصوتية</p>
        <h1 className="ref-hero-title">مكتبة الأصوات</h1>
        <p className="ref-hero-hook">لا يبدأ أي مقطع من تلقاء نفسه — كلها بترخيص مفتوح أو ملكية عامة.</p>
        <div className="ref-hero-stats">
          <div><span className="ref-hero-stat-value">{snd.length}</span><span className="ref-hero-stat-label">مقطعاً</span></div>
          <div><span className="ref-hero-stat-value">{groups.size}</span><span className="ref-hero-stat-label">مجموعة</span></div>
        </div>
      </div>
      {[...groups.entries()].map(([g, list]) => (
        <section key={g} className="stack" aria-label={g}>
          <h2 className="text-label section-title" lang="en" dir="ltr">{g.replace(/_/g, " ")} ({list.length})</h2>
          <ul className="list">
            {list.map((a) => (
              <li key={a.id}><Card flat className="stack-sm">
                <span lang="en" dir="ltr"><b>{a.id}</b> · {a.title}{a.duration_s ? ` · ${a.duration_s}s` : ""}</span>
                <audio controls preload="none" src={a.file} aria-label={a.title} style={{ inlineSize: "100%" }} />
                <span className="row small dim" lang="en" dir="ltr"><Badge latin>{a.license.split(/[ (—]/).slice(0, 3).join(" ")}</Badge> {a.creator}</span>
              </Card></li>
            ))}
          </ul>
        </section>
      ))}
    </>
  );
}
