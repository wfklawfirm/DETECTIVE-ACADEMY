"use client";
import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { type Card, type Prog } from "@/components/CaseCard";
import { LinkButton } from "@/components/ui/button";
import { ErrorState, LoadingRegion } from "@/components/ui/feedback";
import { FolderIcon } from "@/components/ui/icons";
import { ProgressBar } from "@/components/ui/progress";
import { allTokens, api } from "@/lib/client";

/* ── types ──────────────────────────────────────────────────── */
type Filter = "all" | "new" | "inprogress" | "done";

/* ── Difficulty dots ─────────────────────────────────────────── */
function DifficultyDots({ level, max = 5 }: { level: number; max?: number }) {
  return (
    <div className="difficulty-bar" aria-label={`مستوى الصعوبة: ${level} من ${max}`}>
      {Array.from({ length: max }, (_, i) => (
        <span
          key={i}
          className={`difficulty-segment${i < level ? " difficulty-segment--active" : ""}`}
        />
      ))}
    </div>
  );
}

/* ── Status chip ─────────────────────────────────────────────── */
function StatusChip({ prog }: { prog?: Prog }) {
  if (!prog) return <span className="cases-chip cases-chip--new">جديدة</span>;
  if (prog.done) return <span className="cases-chip cases-chip--done">مكتملة ✓</span>;
  return (
    <span className="cases-chip cases-chip--open">
      قيد التحقيق · {prog.evidence_count} دليل
    </span>
  );
}

/* ── Featured case card ──────────────────────────────────────── */
function FeaturedCase({ c, prog }: { c: Card; prog?: Prog }) {
  const href = prog && !prog.done ? `/play/${c.case_id}` : `/case/${c.case_id}`;
  const cta = prog?.done ? "مراجعة القضية" : prog ? "تابع التحقيق" : c.tutorial ? "ابدأ التدريب" : "افتح الملف";
  const idNum = c.case_id.replace(/\D/g, "").padStart(3, "0");
  const stamp = prog?.done ? "مغلقة" : prog ? "قيد التحقيق" : "سرّي";

  return (
    <Link href={href} className="cases-featured" aria-label={`القضية المميزة: ${c.title_ar}`}>
      <div className="cases-featured-visual">
        <span className="cases-featured-glyph" aria-hidden>{c.glyph ?? "🔍"}</span>
        <span className="cases-featured-stamp">{stamp}</span>
      </div>
      <div className="cases-featured-body">
        <div className="cases-featured-toprow">
          <span className="cases-featured-id">CASE #{idNum}</span>
          {c.tutorial && <span className="cases-tag cases-tag--amber">تمهيدية</span>}
          {c.preview && <span className="cases-tag cases-tag--warn">تجريبية</span>}
        </div>
        <p className="cases-featured-kicker">{c.kicker_ar}</p>
        <h2 className="cases-featured-title">{c.title_ar}</h2>
        <p className="cases-featured-tagline">{c.tagline_ar}</p>
        <div className="cases-featured-meta">
          <span className="cases-tag">{c.minutes} دقيقة</span>
          <DifficultyDots level={c.difficulty} />
          <StatusChip prog={prog} />
        </div>
        <span className="btn btn-primary btn-sm cases-featured-cta">{cta}</span>
      </div>
    </Link>
  );
}

/* ── Dossier card ────────────────────────────────────────────── */
function DossierCard({ c, prog }: { c: Card; prog?: Prog }) {
  const href = prog && !prog.done ? `/play/${c.case_id}` : `/case/${c.case_id}`;
  const cta = prog?.done ? "مراجعة" : prog ? "تابع" : c.tutorial ? "ابدأ" : "افتح الملف";
  const idNum = c.case_id.replace(/\D/g, "").padStart(3, "0");

  return (
    <Link href={href} className="dossier-card" aria-label={c.title_ar}>
      <div className="dossier-card-toprow">
        <span className="dossier-card-id">#{idNum}</span>
        <span className="dossier-card-glyph" aria-hidden>{c.glyph ?? "📁"}</span>
      </div>
      <p className="dossier-card-kicker">{c.kicker_ar}</p>
      <h3 className="dossier-card-title">{c.title_ar}</h3>
      <p className="dossier-card-tagline">{c.tagline_ar}</p>
      <div className="dossier-card-meta">
        <span className="cases-tag">{c.minutes} د</span>
        <DifficultyDots level={c.difficulty} />
        {c.tutorial && <span className="cases-tag cases-tag--amber">تمهيدية</span>}
        {c.preview && <span className="cases-tag cases-tag--warn">تجريبية</span>}
      </div>
      <div className="dossier-card-footer">
        <StatusChip prog={prog} />
        <span className="dossier-card-cta">{cta} ←</span>
      </div>
    </Link>
  );
}

/* ── Filter bar ──────────────────────────────────────────────── */
const FILTERS: { id: Filter; label: string }[] = [
  { id: "all",        label: "الكل" },
  { id: "new",        label: "جديدة" },
  { id: "inprogress", label: "مفتوحة" },
  { id: "done",       label: "مكتملة" },
];

/* ── Main page ───────────────────────────────────────────────── */
export default function Cases() {
  const [cards,  setCards]  = useState<Card[] | null>(null);
  const [prog,   setProg]   = useState<Prog[]>([]);
  const [failed, setFailed] = useState(false);
  const [filter, setFilter] = useState<Filter>("all");

  useEffect(() => {
    api<{ cards: Card[]; cases: Prog[] }>("/api/progress", { tokens: allTokens() })
      .then((r) => { setCards(r.cards); setProg(r.cases); })
      .catch(() => setFailed(true));
  }, []);

  /* Featured: first in-progress, else tutorial, else first */
  const featured = useMemo<Card | null>(() => {
    if (!cards || cards.length === 0) return null;
    const ipId = prog.find((p: Prog) => !p.done)?.case_id;
    if (ipId) return cards.find((c: Card) => c.case_id === ipId) ?? null;
    return cards.find((c: Card) => c.tutorial) ?? cards[0] ?? null;
  }, [cards, prog]);

  const progOf = (id: string) => prog.find((p: Prog) => p.case_id === id);

  /* Grid (exclude featured) */
  const gridCards = useMemo<Card[]>(() => {
    if (!cards) return [];
    let list = cards.filter((c: Card) => c.case_id !== featured?.case_id);
    if (filter === "new")        list = list.filter((c: Card) => !progOf(c.case_id));
    if (filter === "inprogress") list = list.filter((c: Card) => { const p = progOf(c.case_id); return p && !p.done; });
    if (filter === "done")       list = list.filter((c: Card) => progOf(c.case_id)?.done);
    return list;
  }, [cards, prog, filter, featured]);

  const counts = useMemo(() => {
    const rest = (cards ?? []).filter((c: Card) => c.case_id !== featured?.case_id);
    return {
      all:        rest.length,
      new:        rest.filter((c: Card) => !progOf(c.case_id)).length,
      inprogress: rest.filter((c: Card) => { const p = progOf(c.case_id); return p && !p.done; }).length,
      done:       rest.filter((c: Card) => progOf(c.case_id)?.done).length,
    };
  }, [cards, prog, featured]);

  const doneCount = prog.filter((p: Prog) => p.done).length;
  const openCount = prog.filter((p: Prog) => !p.done).length;
  const total     = cards?.length ?? 0;

  /* ── render ── */
  return (
    <>
      {/* ── Cinematic hero ──────────────────────────────────────── */}
      <header className="cases-hero">
        <div className="cases-hero-inner">
          <div className="cases-hero-text">
            <p className="cases-hero-kicker">أرشيف التحقيقات</p>
            <h1 className="cases-hero-title">القضايا</h1>
            <p className="cases-hero-sub">
              كل ملف يخفي حقيقة. افحص الأدلة، وشكّل حكمك بنفسك.
            </p>
          </div>
          <div className="cases-hero-badge" aria-hidden>
            <span className="cases-hero-glyph">🗂️</span>
          </div>
        </div>

        {/* Stats strip */}
        {cards && total > 0 && (
          <div className="cases-hero-stats">
            <div className="cases-stat">
              <span className="cases-stat-value">{total}</span>
              <span className="cases-stat-label">قضية</span>
            </div>
            {doneCount > 0 && (
              <div className="cases-stat">
                <span className="cases-stat-value cases-stat-value--done">{doneCount}</span>
                <span className="cases-stat-label">مكتملة</span>
              </div>
            )}
            {openCount > 0 && (
              <div className="cases-stat">
                <span className="cases-stat-value cases-stat-value--open">{openCount}</span>
                <span className="cases-stat-label">مفتوحة</span>
              </div>
            )}
            {total > 0 && (
              <div className="cases-stat cases-stat--bar">
                <ProgressBar value={doneCount} max={total} label="نسبة القضايا المكتملة" />
                <p className="cases-stat-pct">{Math.round((doneCount / total) * 100)}٪</p>
              </div>
            )}
          </div>
        )}
      </header>

      {/* ── States ─────────────────────────────────────────────── */}
      {failed && (
        <ErrorState
          title="تعذّر تحميل القضايا"
          body="تحقق من الاتصال ثم أعد المحاولة."
          action={
            <button className="btn btn-outline btn-sm" onClick={() => location.reload()}>
              أعد المحاولة
            </button>
          }
        />
      )}

      {!failed && !cards && <LoadingRegion cards={4} />}

      {!failed && cards && cards.length === 0 && (
        <div className="empty-state">
          <FolderIcon size={32} />
          <p>لا قضايا متاحة لفئتك حالياً.</p>
        </div>
      )}

      {/* ── Content ─────────────────────────────────────────────── */}
      {!failed && cards && cards.length > 0 && (
        <>
          {/* Featured */}
          {featured && (
            <section aria-labelledby="featured-h">
              <p className="cases-section-kicker" id="featured-h">
                {progOf(featured.case_id) && !progOf(featured.case_id)?.done
                  ? "تابع تحقيقك"
                  : "القضية المميزة"}
              </p>
              <FeaturedCase c={featured} prog={progOf(featured.case_id)} />
            </section>
          )}

          {/* Archive grid */}
          {total > 1 && (
            <section aria-labelledby="archive-h">
              <p className="cases-section-kicker" id="archive-h">أرشيف القضايا</p>

              {/* Filter bar */}
              <div className="cases-filter-bar" role="group" aria-label="تصفية القضايا">
                {FILTERS.map(({ id, label }) => (
                  <button
                    key={id}
                    className={`cases-filter-btn${filter === id ? " cases-filter-btn--active" : ""}`}
                    aria-pressed={filter === id}
                    onClick={() => setFilter(id)}
                  >
                    {label}
                    {counts[id] > 0 && (
                      <span className="cases-filter-count">{counts[id]}</span>
                    )}
                  </button>
                ))}
              </div>

              {/* Grid */}
              {gridCards.length === 0 ? (
                <div className="empty-state" style={{ minBlockSize: "8rem" }}>
                  <p>لا قضايا في هذه الفئة.</p>
                </div>
              ) : (
                <div className="cases-grid">
                  {gridCards.map((c: Card) => (
                    <DossierCard key={c.case_id} c={c} prog={progOf(c.case_id)} />
                  ))}
                </div>
              )}
            </section>
          )}
        </>
      )}
    </>
  );
}
