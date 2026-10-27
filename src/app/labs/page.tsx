import { loadLabs } from "@/engine/labs";
import { Badge } from "@/components/ui/badge";
import { Card, CardLink, PageHead } from "@/components/ui/card";
import { ChevronIcon } from "@/components/ui/icons";

export const metadata = { title: "مختبرات آمنة" };
export const dynamic = "force-dynamic";

export default function Labs() {
  const f = loadLabs();
  return (
    <>
      <PageHead title="مختبرات آمنة" lead={`تمارين قصيرة بسجلات خيالية تدرّب مهارة واحدة. ليست إجراءات جنائية حقيقية ولا مختبرات طبية. المتاح للعب الآن ${f.playable.length} من ${f.catalogue.length}؛ والباقي مواصفات تصميم تنتظر البناء ومراجعة الخبراء.`} />
      <ul className="list">
        {f.catalogue.map((c) => {
          const body = (
            <>
              <div className="row" style={{ flexWrap: "nowrap" }}><b className="grow">{c.title_ar}</b>{c.playable && <ChevronIcon className="chev" size={20} />}</div>
              <span className="small dim">المهارة: {c.skill_ar} · {c.interaction_ar}</span>
              <span className="row small"><Badge tone={c.playable ? "positive" : "neutral"}>{c.playable ? "جاهز للعب" : "قيد التصميم"}</Badge><Badge tone="warning">يتطلب مراجعة خبراء</Badge></span>
            </>
          );
          return <li key={c.id}>{c.playable ? <CardLink href={`/labs/${c.id}`}>{body}</CardLink> : <Card flat>{body}</Card>}</li>;
        })}
      </ul>
    </>
  );
}
