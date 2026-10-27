"use client";
import { use, useEffect, useState } from "react";
import { EntryHook } from "@/components/EntryHook";
import { Badge } from "@/components/ui/badge";
import { LinkButton } from "@/components/ui/button";
import { Callout, EmptyState, LoadingRegion } from "@/components/ui/feedback";
import { FolderIcon } from "@/components/ui/icons";
import { allTokens, api } from "@/lib/client";
import type { Card, Prog } from "@/components/CaseCard";

export default function CaseIntro({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const [card, setCard] = useState<Card | null | undefined>(undefined);
  const [prog, setProg] = useState<Prog | undefined>();
  useEffect(() => {
    api<{ cards: Card[]; cases: Prog[] }>("/api/progress", { tokens: allTokens() }).then((r) => { setCard(r.cards.find((c) => c.case_id === id) ?? null); setProg(r.cases.find((c) => c.case_id === id)); }).catch(() => setCard(null));
  }, [id]);
  if (card === undefined) return <LoadingRegion cards={2} />;
  if (card === null) return (
    <>
      <h1 className="text-page-title">القضية غير متاحة</h1>
      <EmptyState icon={<FolderIcon size={28} />} title="لم نجد هذه القضية" body="قد لا تناسب فئتك العمرية أو لم تُنشر بعد." action={<LinkButton variant="secondary" href="/cases">عودة إلى القضايا</LinkButton>} />
    </>
  );
  return (
    <>
      <EntryHook surface={prog && !prog.done ? "case_return" : "case_open"} caseId={id} />
      <section className="lantern hero">
        <div className="row row-between"><span className="stamp">سرّي</span><span className="kicker">{card.kicker_ar}</span></div>
        <h1 className="hero-title" style={{ fontSize: "2rem" }}>{card.title_ar}</h1>
        <p className="hero-lead">{card.tagline_ar}</p>
        <div className="row"><Badge>{card.minutes} دقيقة</Badge><Badge>الفئة: {card.age_band === "all" ? "الجميع" : card.age_band}</Badge>{card.preview && <Badge tone="warning">نسخة تجريبية: لم تكتمل المراجعة الخبيرة</Badge>}</div>
      </section>
      <Callout tone="info">القصة والأشخاص خياليون. الأدلة مصمَّمة لتدريب مهارات التحقق، وليست توثيقاً لوقائع حقيقية. ما تقرّره هنا لا يُقاس عليه في الواقع دون مختصين.</Callout>
      <div className="stack-sm">
        <LinkButton variant="primary" size="lg" block href={`/play/${id}`}>{prog && !prog.done ? "تابع التحقيق" : prog?.done ? "راجع الملخص" : "افتح الملف"}</LinkButton>
        <LinkButton variant="ghost" block href="/cases">رجوع</LinkButton>
      </div>
    </>
  );
}
