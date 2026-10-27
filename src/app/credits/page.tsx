import { loadAssets } from "@/engine/assets";
import { Badge } from "@/components/ui/badge";
import { Card, PageHead } from "@/components/ui/card";

export const metadata = { title: "الاعتمادات" };
export const dynamic = "force-dynamic";

export default function Credits() {
  const all = loadAssets();
  return (
    <>
      <PageHead title="الاعتمادات والتراخيص" lead="لا ندرج في أثر صورة ولا صوتاً إلا إذا سجّلت مكتبتنا أنه ملكية عامة أو بترخيص مفتوح يسمح بالاستخدام. وهذه قائمتها كاملة؛ الذكر هنا واجب في بعضها (CC BY) وتطوّع في الباقي." />
      <ul className="list grid-2" style={{ display: "grid" }}>
        {all.map((a) => (
          <li key={a.id}><Card flat className="small" lang="en" dir="ltr"><span><b>{a.id}</b> · {a.attribution}</span><span className="row"><a href={a.source} target="_blank" rel="noopener noreferrer">source</a><Badge latin>{a.license.split(" — ")[0]}</Badge></span></Card></li>
        ))}
      </ul>
      <p className="small dim">الخطوط: Amiri وIBM Plex Sans Arabic وIBM Plex Mono وReem Kufi بترخيص SIL OFL عبر Fontsource.</p>
    </>
  );
}
