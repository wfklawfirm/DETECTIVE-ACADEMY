import Link from "next/link";
import { loadLabs } from "@/engine/labs";

export const metadata = { title: "مختبرات آمنة" };
export const dynamic = "force-dynamic";

export default function Labs() {
  const f = loadLabs();
  return (
    <div className="wrap stack">
      <h1>مختبرات آمنة</h1>
      <p className="dim">تمارين قصيرة بسجلات خيالية تدرّب مهارة واحدة. ليست إجراءات جنائية حقيقية ولا مختبرات طبية. المتاح للعب الآن {f.playable.length} من {f.catalogue.length}؛ والباقي مواصفات تصميم تنتظر البناء ومراجعة الخبراء.</p>
      <ul className="stack" style={{ listStyle: "none", padding: 0 }}>
        {f.catalogue.map((c) => (
          <li key={c.id} className="card stack" style={{ gap: 4 }}>
            {c.playable ? <Link href={`/labs/${c.id}`}><b>{c.title_ar}</b></Link> : <b>{c.title_ar}</b>}
            <span className="small dim">المهارة: {c.skill_ar} · {c.interaction_ar}</span>
            <span className="small"><span className="chip">{c.playable ? "جاهز للعب" : "قيد التصميم"}</span> <span className="chip">يتطلب مراجعة خبراء</span></span>
          </li>
        ))}
      </ul>
    </div>
  );
}
