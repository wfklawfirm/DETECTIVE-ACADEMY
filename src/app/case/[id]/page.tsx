"use client";
import { use, useEffect, useState } from "react";
import { EntryHook } from "@/components/EntryHook";
import { LinkButton } from "@/components/ui/button";
import { EmptyState, LoadingRegion } from "@/components/ui/feedback";
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
        <div className="case-detail-hero case-detail-hero--empty">
          <div className="case-detail-topbar">
            <span className="case-id-label">ملف مجهول</span>
            <span className="case-detail-stamp">سرّي</span>
          </div>
          <div className="case-detail-glyph" aria-hidden>🔒</div>
          <h1 className="case-detail-title">القضية غير متاحة</h1>
        </div>
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

  const stampLabel = isDone ? "مغلقة" : isOpen ? "قيد التحقيق" : "سرّي";
  const stampMod   = isDone ? "stamp--closed" : isOpen ? "stamp--active" : "stamp--secret";

  return (
    <>
      <EntryHook surface={isOpen ? "case_return" : "case_open"} caseId={id} />

      {/* ── Cinematic hero ──────────────────────────────────────── */}
      <div className="case-detail-hero">
        {/* Top bar */}
        <div className="case-detail-topbar">
          <span className="case-id-label">#{caseNum}</span>
          <span className={`case-detail-stamp ${stampMod}`}>{stampLabel}</span>
        </div>

        {/* Glyph */}
        <div className="case-detail-glyph" aria-hidden>{card.glyph ?? "📁"}</div>

        {/* Kicker + title + tagline */}
        <p className="case-detail-kicker">{card.kicker_ar}</p>
        <h1 className="case-detail-title">{card.title_ar}</h1>
        <p className="case-detail-tagline">{card.tagline_ar}</p>

        {/* Meta chips */}
        <div className="case-detail-meta">
          <span className="case-detail-chip">{card.minutes} دقيقة</span>
          <span className="case-detail-chip">
            {card.age_band === "all" ? "للجميع" : `الفئة: ${card.age_band}`}
          </span>
          {card.tutorial && <span className="case-detail-chip case-detail-chip--amber">نقطة البداية</span>}
          {card.preview  && <span className="case-detail-chip case-detail-chip--red">تجريبية</span>}
        </div>

        {/* Difficulty */}
        {card.difficulty != null && (
          <div className="case-detail-difficulty">
            <span className="case-detail-difficulty-label">الصعوبة</span>
            <DifficultyDots level={card.difficulty} />
          </div>
        )}
      </div>

      {/* ── Progress panel (open investigation) ────────────────── */}
      {isOpen && (
        <div className="case-detail-progress">
          <p className="case-detail-progress-eyebrow">تقدّم التحقيق</p>
          <div className="case-detail-progress-row">
            <div className="case-detail-progress-stat">
              <span className="case-detail-progress-value">{prog.evidence_count}</span>
              <span className="case-detail-progress-key">دليل محفوظ</span>
            </div>
            {prog.locked_count > 0 && (
              <div className="case-detail-progress-stat">
                <span className="case-detail-progress-value">{prog.locked_count}</span>
                <span className="case-detail-progress-key">لم يُكشف بعد</span>
              </div>
            )}
          </div>
          <p className="case-detail-progress-note">تحقيقك مستمر — تابع من حيث توقفت</p>
        </div>
      )}

      {/* ── Disclaimer strip ────────────────────────────────────── */}
      <div className="case-detail-disclaimer">
        <span className="case-detail-disclaimer-mark" aria-hidden>ℹ</span>
        <p>القصة والأشخاص خياليون. الأدلة مصمَّمة لتدريب مهارات التحقق، وليست توثيقاً لوقائع حقيقية. ما تقرّره هنا لا يُقاس عليه في الواقع دون مختصين.</p>
      </div>

      {/* ── CTA ─────────────────────────────────────────────────── */}
      <div className="case-detail-actions">
        <LinkButton variant="primary" size="lg" block href={`/play/${id}`}>
          {isDone ? "راجع الملخص" : isOpen ? "تابع التحقيق" : "افتح الملف"}
        </LinkButton>
        <LinkButton variant="ghost" block href="/cases">رجوع إلى القضايا</LinkButton>
      </div>
    </>
  );
}
