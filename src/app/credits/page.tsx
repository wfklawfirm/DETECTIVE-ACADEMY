import { loadAssets } from "@/engine/assets";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";

export const metadata = { title: "الاعتمادات" };
export const dynamic = "force-dynamic";

export default function Credits() {
  const all = loadAssets();
  const imgs = all.filter((a) => a.kind === "image").length, snd = all.filter((a) => a.kind === "audio").length;
  return (
    <>
      <div className="ref-hero">
        <p className="ref-hero-kicker">الاعتمادات والتراخيص</p>
        <h1 className="ref-hero-title">كل ما نستخدمه وأصحابه</h1>
        <p className="ref-hero-hook">لا ندرج صورة ولا صوتاً إلا بترخيص مفتوح أو ملك عام مُسجَّل. الذكر هنا واجب في بعضها وتطوّع في الباقي.</p>
        <div className="ref-hero-stats">
          <div><span className="ref-hero-stat-value">{imgs}</span><span className="ref-hero-stat-label">صورة</span></div>
          <div><span className="ref-hero-stat-value">{snd}</span><span className="ref-hero-stat-label">مقطع صوتي</span></div>
        </div>
      </div>
      {[...new Set(all.map((a) => `${a.kind}:${a.collection ?? "core"}`))].sort().map((g) => (
        <details key={g} className="card">
          <summary lang="en" dir="ltr">{g.replace(":", " · ").replace(/_/g, " ")} ({all.filter((a) => `${a.kind}:${a.collection ?? "core"}` === g).length})</summary>
          <ul className="stack-sm small" lang="en" dir="ltr">
            {all.filter((a) => `${a.kind}:${a.collection ?? "core"}` === g).map((a) => (
              <li key={a.id}><b>{a.id}</b> · {a.attribution} <a href={a.source} target="_blank" rel="noopener noreferrer">source</a> <Badge latin>{(a.license.split(" — ")[0] ?? "").slice(0, 40)}</Badge></li>
            ))}
          </ul>
        </details>
      ))}
      <p className="small dim">الأيقونات في <a href="/icons">مكتبة الأيقونات</a> بتراخيص MIT وISC وApache-2.0 مع نص كل ترخيص. الخطوط: Amiri وIBM Plex Sans Arabic وIBM Plex Mono وReem Kufi بترخيص SIL OFL عبر Fontsource.</p>
    </>
  );
}
