import { loadAssets } from "@/engine/assets";
import { Badge } from "@/components/ui/badge";
import { Card, PageHead } from "@/components/ui/card";

export const metadata = { title: "مكتبة الأصوات" };
export const dynamic = "force-dynamic";

export default function Sounds() {
  const snd = loadAssets().filter((a) => a.kind === "audio");
  const groups = new Map<string, typeof snd>();
  for (const a of snd) groups.set(a.collection ?? "other", [...(groups.get(a.collection ?? "other") ?? []), a]);
  return (
    <>
      <PageHead title="مكتبة الأصوات" lead={`${snd.length} مقطعاً من أصوات واجهة وورق وبيئات حقلية وعزف كلاسيكي، كلها بترخيص مفتوح أو ملكية عامة. لا يبدأ أي مقطع من تلقاء نفسه؛ اضغط تشغيل إن أردت. أصوات الواجهة داخل اللعبة مُطفأة افتراضياً.`} />
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
