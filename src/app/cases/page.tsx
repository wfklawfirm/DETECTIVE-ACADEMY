"use client";
import { useEffect, useState } from "react";
import { CaseCard, type Card, type Prog } from "@/components/CaseCard";
import { api, allTokens } from "@/lib/client";

export default function Cases() {
  const [cards, setCards] = useState<Card[] | null>(null);
  const [prog, setProg] = useState<Prog[]>([]);
  useEffect(() => {
    void (async () => {
      const r = await api<{ cards: Card[]; cases: Prog[] }>("/api/progress", { tokens: allTokens() });
      setCards(r.cards); setProg(r.cases);
    })();
  }, []);
  return (
    <div className="wrap stack">
      <h1>القضايا</h1>
      <p className="dim">كل قضية ملف مستقل بأدلته وشخصياته. ابدأ بالتمهيدية إن كانت أول مرة.</p>
      {!cards ? <p className="dim">جارٍ التحميل…</p> : cards.length === 0 ? <p>لا قضايا متاحة لفئتك العمرية حالياً.</p> : (
        <div className="grid cols-2">{cards.map((c) => <CaseCard key={c.case_id} c={c} p={prog.find((x) => x.case_id === c.case_id)} />)}</div>
      )}
    </div>
  );
}
