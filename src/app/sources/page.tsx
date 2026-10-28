import { RIGHTS_LABEL, loadKnowledge } from "@/engine/knowledge";
import { SourceList } from "@/components/SourceList";
import { Card, CardTitle } from "@/components/ui/card";

export const metadata = { title: "المصادر والحقوق" };
export const dynamic = "force-dynamic";

export default function Sources() {
  const { src, kos } = loadKnowledge();
  const by: Record<string, number> = {};
  for (const s of src) by[s.rights ?? "UNKNOWN"] = (by[s.rights ?? "UNKNOWN"] ?? 0) + 1;
  const cited = src.filter((s) => s.cited);
  return (
    <>
      <div className="ref-hero">
        <p className="ref-hero-kicker">المصادر والحقوق</p>
        <h1 className="ref-hero-title">سجل المصادر البحثية</h1>
        <p className="ref-hero-hook">نعرض حالة الحقوق كما سُجّلت، ولا نقتبس من محمي؛ نحيل إليه فقط.</p>
        <div className="ref-hero-stats">
          <div><span className="ref-hero-stat-value">{src.length}</span><span className="ref-hero-stat-label">مصدراً</span></div>
          <div><span className="ref-hero-stat-value">{cited.length}</span><span className="ref-hero-stat-label">مستشهداً به</span></div>
          <div><span className="ref-hero-stat-value">{kos.length}</span><span className="ref-hero-stat-label">كائن معرفي</span></div>
        </div>
      </div>
      <Card as="section"><CardTitle level={2}>حالة الحقوق</CardTitle>
        <table className="simple"><tbody>{Object.entries(by).sort((a, b) => b[1] - a[1]).map(([k, n]) => <tr key={k}><th scope="row">{RIGHTS_LABEL[k] ?? k}</th><td className="num">{n}</td></tr>)}</tbody></table>
        <p className="small dim">«غير محسوم» تعني أن الحالة لم تُحسم بعد ونعاملها معاملة المحمي حتى يثبت غير ذلك. هذا سجل عملي وليس رأياً قانونياً.</p></Card>
      <SourceList items={cited.map(({ id, title, title_ar, authors, year, url, rights, grade }) => ({ id, title, title_ar, authors, year, url, rights, grade }))} />
    </>
  );
}
