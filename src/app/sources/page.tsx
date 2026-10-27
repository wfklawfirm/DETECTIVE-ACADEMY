import { RIGHTS_LABEL, loadKnowledge } from "@/engine/knowledge";
import { SourceList } from "@/components/SourceList";
import { Card, CardTitle, PageHead } from "@/components/ui/card";

export const metadata = { title: "المصادر والحقوق" };
export const dynamic = "force-dynamic";

export default function Sources() {
  const { src, kos } = loadKnowledge();
  const by: Record<string, number> = {};
  for (const s of src) by[s.rights ?? "UNKNOWN"] = (by[s.rights ?? "UNKNOWN"] ?? 0) + 1;
  const cited = src.filter((s) => s.cited);
  return (
    <>
      <PageHead title="المصادر والحقوق" lead={`سجل مصادر مكتبة أثر البحثية: ${src.length} مصدراً، منها ${cited.length} يستند إليه محتوى الموسوعة (${kos.length} كائن معرفي). نعرض حالة الحقوق كما سُجّلت، ولا نقتبس من محمي بحقوق النشر؛ نحيل إليه فقط.`} />
      <Card as="section"><CardTitle level={2}>حالة الحقوق</CardTitle>
        <table className="simple"><tbody>{Object.entries(by).sort((a, b) => b[1] - a[1]).map(([k, n]) => <tr key={k}><th scope="row">{RIGHTS_LABEL[k] ?? k}</th><td className="num">{n}</td></tr>)}</tbody></table>
        <p className="small dim">«غير محسوم» تعني أن الحالة لم تُحسم بعد ونعاملها معاملة المحمي حتى يثبت غير ذلك. هذا سجل عملي وليس رأياً قانونياً.</p></Card>
      <SourceList items={cited.map(({ id, title, title_ar, authors, year, url, rights, grade }) => ({ id, title, title_ar, authors, year, url, rights, grade }))} />
    </>
  );
}
