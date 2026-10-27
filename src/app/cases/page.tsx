"use client";
import { useEffect, useState } from "react";
import { CaseCard, type Card, type Prog } from "@/components/CaseCard";
import { PageHead } from "@/components/ui/card";
import { EmptyState, ErrorState, LoadingRegion } from "@/components/ui/feedback";
import { FolderIcon } from "@/components/ui/icons";
import { allTokens, api } from "@/lib/client";

export default function Cases() {
  const [cards, setCards] = useState<Card[] | null>(null);
  const [prog, setProg] = useState<Prog[]>([]);
  const [failed, setFailed] = useState(false);
  useEffect(() => {
    api<{ cards: Card[]; cases: Prog[] }>("/api/progress", { tokens: allTokens() }).then((r) => { setCards(r.cards); setProg(r.cases); }).catch(() => setFailed(true));
  }, []);
  return (
    <>
      <PageHead title="القضايا" lead="كل قضية ملف مستقل بأدلته وشخصياته. ابدأ بالتمهيدية إن كانت أول مرة." />
      {failed ? <ErrorState title="تعذّر تحميل القضايا" body="تحقق من الاتصال ثم أعد المحاولة." /> : !cards ? <LoadingRegion /> : cards.length === 0 ? <EmptyState icon={<FolderIcon size={28} />} title="لا قضايا متاحة" body="لا قضايا متاحة لفئتك العمرية حالياً." /> : (
        <div className="stack">{cards.map((c) => <CaseCard key={c.case_id} c={c} p={prog.find((x) => x.case_id === c.case_id)} />)}</div>
      )}
    </>
  );
}
