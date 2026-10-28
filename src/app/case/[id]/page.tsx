"use client";
import { use, useEffect, useState } from "react";
import { EntryHook } from "@/components/EntryHook";
import { Badge } from "@/components/ui/badge";
import { LinkButton } from "@/components/ui/button";
import { Callout, EmptyState, LoadingRegion } from "@/components/ui/feedback";
import { FolderIcon } from "@/components/ui/icons";
import { allTokens, api } from "@/lib/client";
import type { Card, Prog } from "@/components/CaseCard";

/* ── Difficulty dots ─────────────────────────────────────────── */
function DifficultyDots({ level, max = 5 }: { level: number; max?: number }) {
  return (
    <div className="difficulty-bar" aria-label={`مستوى الصعوبة: ${level} من ${max}`}>
      {Array.from({ length: max }, (_, i) => (
        <span key={i} className={`difficulty-segment${i < level ? " difficulty-segment--active" : ""}`} />
      ))}
    </div>
  );
}

/* ── Case detail page ────────────────────────────────────────── */
export default function CaseIntro({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const [card, setCard] = useState<Card | null | undefined>(undefined);
  const [prog, setProg] = useState<Prog | undefined>();

  useEffect(() => {
    api<{ cards: Card[]; cases: Prog[] }>("/api/progress", { tokens: allTokens() })
      .then((r) => {
        setCard(r.cards.find((c: Card) => c.case_id === id) ?? null);
        setProg(r.cases.find((c: Prog) => c.case_id === id));
      })
      .catch(() => setCard(null));
  }, [id]);

  if (card === undefined) return <LoadingRegion cards={2} />;

  if (card === null) {
    return (
      <>
        <h1 className="text-page-title">القضية غير متاحة</h1>
        <EmptyState
          icon={<FolderIcon size={28} />}
          title="لم نجد هذه القضية"
          body="قد لا تناسب فئتك العمرية أو لم تُنشر بعد."
          action={<LinkButton variant="secondary" href="/cases">عودة إلى القضايا</LinkButton>}
        />
      </>
    );
  }

  const isDone = prog?.done;
  const isOpen = prog && !prog.done;
  const caseNum = card.case_id.replace(/[^0-9]/g, "").padStart(3, "0");

  return (
    <>
      <EntryHook surface={isOpen ? "case_return" : "case_open"} caseId={id} />

      {/* ── Cinematic hero ──────────────────────────────────────── */}
      <div className="case-detail-hero">
        {/* Top bar */}
        <div className="case-detail-topbar">
          <span className="case-id-label">#{caseNum}</span>
          <span className="case-detail-stamp">
            {isDone ? "مغلقة" : isOpen ? "قيد التحقيق" : "سرّي"}
          </span>
        </div>

        {/* Glyph + title */}
        <div className="case-detail-glyph" aria-hidden>{card.glyph ?? "📁"}</div>
        <p className="case-detail-kicker">{card.kicker_ar}</p>
        <h1 className="case-detail-title">{card.title_ar}</h1>
        <p className="case-detail-tagline">{card.tagline_ar}</p>

        {/* Meta row */}
        <div className="case-detail-meta">
          <Badge>{card.minutes} دقيقة</Badge>
          <Badge>الفئة: {card.age_band === "all" ? "الجميع" : card.age_band}</Badge>
          {card.tutorial && <Badge tone="warning">نقطة البداية</Badge>}
          {card.preview && <Badge tone="warning">نسخة تجريبية: لم تكتمل المراجعة الخبيرة</Badge>}
        </div>

        {/* Difficulty */}
        {card.difficulty != null && (
          <div className="case-detail-difficulty">
            <span className="case-detail-difficulty-label">مستوى الصعوبة</span>
            <DifficultyDots level={card.difficulty} />
          </div>
        )}
      </div>

      {/* ── Progress panel (if open investigation) ─────────────── */}
      {isOpen && (
        <div className="case-detail-progress-panel">
          <div className="case-detail-progress-row">
            <div className="case-detail-progress-stat">
              <span className="case-detail-progress-value">{prog.evidence_count}</span>
              <span className="case-detail-progress-label">دليل محفوظ</span>
            </div>
            {prog.locked_count > 0 && (
              <div className="case-detail-progress-stat">
                <span className="case-detail-progress-value">{prog.locked_count}</span>
                <span className="case-detail-progress-label">لم يُكشف بعد</span>
              </div>
            )}
          </div>
          <p className="small dim-2">تحقيقك مستمر — تابع من حيث توقفت.</p>
        </div>
      )}

      {/* ── Disclaimer ────────────────────────────────────────── */}
      <Callout tone="info">
        القصة والأشخاص خياليون. الأدلة مصمَّمة لتدريب مهارات التحقق، وليست توثيقاً لوقائع حقيقية. ما تقرّره هنا لا يُقاس عليه في الواقع دون مختصين.
      </Callout>

      {/* ── CTA ───────────────────────────────────────────────── */}
      <div className="case-detail-actions">
        <LinkButton variant="primary" size="lg" block href={`/play/${id}`}>
          {isDone ? "راجع الملخص" : isOpen ? "تابع التحقيق" : "افتح الملف"}
        </LinkButton>
        <LinkButton variant="ghost" block href="/cases">رجوع إلى القضايا</LinkButton>
      </div>
    </>
  );
}
