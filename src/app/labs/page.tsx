import { KIND_LABEL, loadLabs, type LabKind } from "@/engine/labs";
import { Badge } from "@/components/ui/badge";
import { Card, CardLink, PageHead } from "@/components/ui/card";
import { ChevronIcon } from "@/components/ui/icons";
import { DIFFICULTY_LABEL } from "./labels";

export const metadata = { title: "مختبرات آمنة" };
export const dynamic = "force-dynamic";

export default function Labs() {
  const f = loadLabs();
  const playable = new Map(f.playable.map((l) => [l.id, l]));
  const kinds = Object.keys(KIND_LABEL) as LabKind[];
  return (
    <>
      <PageHead title="مختبرات آمنة" kicker="تدريب بلا خطر" lead={`هل تستطيع أن تحكم على دليل دون أن تتجاوز ما يقوله؟ ${f.playable.length} تمريناً قصيراً بسجلات خيالية، كل واحد يدرّب مهارة واحدة. ليست إجراءات جنائية حقيقية ولا مختبرات طبية، وكلها تنتهي بسؤال: ماذا لا يثبته هذا الدليل؟ المتاح للعب الآن ${f.playable.length} من ${f.catalogue.length}.`} />
      {kinds.map((k) => {
        const group = f.catalogue.filter((c) => playable.get(c.id)?.kind === k);
        if (!group.length) return null;
        return (
          <section key={k} className="stack" aria-labelledby={`k-${k}`}>
            <h2 id={`k-${k}`} className="text-section-title">{KIND_LABEL[k]} <span className="small dim">({group.length})</span></h2>
            <ul className="list">
              {group.map((c) => {
                const l = playable.get(c.id)!;
                return (
                  <li key={c.id}>
                    <CardLink href={`/labs/${c.id}`}>
                      <div className="row" style={{ flexWrap: "nowrap" }}><b className="grow">{l.title_ar}</b><ChevronIcon className="chev" size={20} /></div>
                      <span className="small dim">المهارة: {l.skill_ar} · {c.interaction_ar}</span>
                      <span className="row small"><Badge outline>{DIFFICULTY_LABEL[l.difficulty]}</Badge><Badge outline>نحو {l.minutes} د</Badge><Badge tone="warning">يتطلب مراجعة خبراء</Badge></span>
                    </CardLink>
                  </li>
                );
              })}
            </ul>
          </section>
        );
      })}
      {f.declined.length > 0 && (
        <Card as="section" aria-labelledby="declined">
          <h2 id="declined" className="text-section-title">مختبرات لم نبنِها، ولماذا</h2>
          <ul className="stack-sm">{f.declined.map((d) => <li key={d.title_ar}><b>{d.title_ar}.</b> <span className="small dim">{d.reason_ar}</span></li>)}</ul>
        </Card>
      )}
    </>
  );
}
