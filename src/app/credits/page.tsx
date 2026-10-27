import { loadAssets } from "@/engine/assets";

export const metadata = { title: "الاعتمادات" };
export const dynamic = "force-dynamic";

export default function Credits() {
  const all = loadAssets();
  return (
    <div className="wrap stack">
      <h1>الاعتمادات والتراخيص</h1>
      <p className="dim">لا ندرج في أثر صورة ولا صوتاً إلا إذا سجّلت مكتبتنا أنه ملكية عامة أو بترخيص مفتوح يسمح بالاستخدام. وهذه قائمتها كاملة؛ الذكر هنا واجب في بعضها (CC BY) وتطوّع في الباقي.</p>
      <ul className="stack" style={{ listStyle: "none", padding: 0 }}>
        {all.map((a) => (
          <li key={a.id} className="card small" lang="en" dir="ltr"><b>{a.id}</b> · {a.attribution} <a href={a.source} target="_blank" rel="noopener noreferrer">source</a> · <span className="chip">{a.license.split(" — ")[0]}</span></li>
        ))}
      </ul>
      <p className="small dim">الخطوط: Amiri وIBM Plex Sans Arabic وIBM Plex Mono وReem Kufi بترخيص SIL OFL عبر Fontsource.</p>
    </div>
  );
}
