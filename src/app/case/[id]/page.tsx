"use client";
import Link from "next/link";
import { use, useEffect, useState } from "react";
import { EntryHook } from "@/components/EntryHook";
import { allTokens, api } from "@/lib/client";
import type { Card, Prog } from "@/components/CaseCard";

export default function CaseIntro({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const [card, setCard] = useState<Card | null | undefined>(undefined);
  const [prog, setProg] = useState<Prog | undefined>();
  useEffect(() => {
    void api<{ cards: Card[]; cases: Prog[] }>("/api/progress", { tokens: allTokens() }).then((r) => { setCard(r.cards.find((c) => c.case_id === id) ?? null); setProg(r.cases.find((c) => c.case_id === id)); });
  }, [id]);
  if (card === undefined) return <div className="wrap"><p className="dim">جارٍ التحميل…</p></div>;
  if (card === null) return <div className="wrap stack"><h1>القضية غير متاحة</h1><p>قد لا تناسب فئتك العمرية أو لم تُنشر بعد.</p><Link className="btn" href="/cases">عودة إلى القضايا</Link></div>;
  return (
    <div className="wrap-narrow stack" data-accent={card.accent}>
      <EntryHook surface={prog && !prog.done ? "case_return" : "case_open"} caseId={id} />
      <p className="kicker">{card.kicker_ar}</p>
      <h1>{card.title_ar}</h1>
      <p className="lead dim" style={{ fontFamily: "var(--f-display)", fontSize: "1.4rem" }}>{card.tagline_ar}</p>
      <div className="row"><span className="chip">{card.minutes} دقيقة</span><span className="chip">الفئة: {card.age_band === "all" ? "الجميع" : card.age_band}</span>{card.preview && <span className="chip amber">نسخة تجريبية: لم تكتمل المراجعة الخبيرة</span>}</div>
      <div className="card"><p className="small dim" style={{ margin: 0 }}>القصة والأشخاص خياليون. الأدلة مصمَّمة لتدريب مهارات التحقق، وليست توثيقاً لوقائع حقيقية. ما تقرّره هنا لا يُقاس عليه في الواقع دون مختصين.</p></div>
      <div className="row">
        <Link className="btn primary" href={`/play/${id}`}>{prog && !prog.done ? "تابع التحقيق" : prog?.done ? "راجع الملخص" : "افتح الملف"}</Link>
        <Link className="btn ghost" href="/cases">رجوع</Link>
      </div>
    </div>
  );
}
