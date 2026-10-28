"use client";
import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { type Card, type Prog } from "@/components/CaseCard";
import { FolderIcon } from "@/components/ui/icons";
import { allTokens, api } from "@/lib/client";

/* ─── types ─── */
type Filter = "all" | "new" | "inprogress" | "done";

/* ─── helpers ─── */
function DifficultyDots({ level, max = 5 }: { level: number; max?: number }) {
  return (
    <div className="difficulty-bar" aria-label={`الصعوبة ${level} من ${max}`}>
      {Array.from({ length: max }, (_, i) => (
        <div
          key={i}
          className={`difficulty-segment${i < level ? " filled" : ""}`}
        />
      ))}
    </div>
  );
}

function CaseStatusBadge({ prog }: { prog?: Prog }) {
  if (!prog) return <span className="badge">جديدة</span>;
  if (prog.done) return <span className="badge badge-positive">مكتملة ✓</span>;
  return <span className="badge badge-brand">قيد التحقيق · {prog.evidence_count} دليل</span>;
}

/* ─── loading skeleton ─── */
function CasesSkeleton() {
  return (
    <div className="cases-grid">
      {Array.from({ length: 6 }, (_, i) => (
        <div key={i} className="dossier">
          <span className="dossier-tab skeleton" style={{ inlineSize: "6rem", blockSize: "1.4rem" }} />
          <div className="card" style={{ gap: "0.75rem", minBlockSize: "14rem" }}>
            <div className="skeleton" style={{ blockSize: "2.5rem", inlineSize: "3rem", borderRadius: "4px" }} />
            <div className="skeleton skel-line" style={{ inlineSize: "70%" }} />
            <div className="skeleton skel-line" style={{ inlineSize: "90%" }} />
            <div className="skeleton skel-line" style={{ inlineSize: "50%" }} />
          </div>
        </div>
      ))}
    </div>
  );
}

/* ─── featured case card ─── */
function FeaturedCase({ c, prog }: { c: Card; prog?: Prog }) {
  const href = prog && !prog.done ? `/play/${c.case_id}` : `/case/${c.case_id}`;
  const ctaLabel = prog?.done
    ? "مراجعة القضية"
    : prog
    ? "تابع التحقيق"
    : c.tutorial
    ? "ابدأ التدريب"
    : "ابدأ التحقيق";

  const idNum = c.case_id.replace(/\D/g, "").padStart(3, "0");

  return (
    <Link href={href} className="featured-case" aria-label={`القضية المميزة: ${c.title_ar}`}>
      <div className="featured-case-visual">
        <span className="featured-case-glyph" aria-hidden>{c.glyph || "🔍"}</span>
      </div>
      <div className="featured-case-body">
        <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
          <span className="featured-case-id">CASE #{idNum}</span>
          {c.tutorial && <span className="badge badge-amber">تمهيدية</span>}
          {c.preview && <span className="badge badge-warning">قيد المراجعة</span>}
        </div>
        <h2 className="featured-case-title">{c.title_ar}</h2>
        <p className="featured-case-desc">{c.tagline_ar}</p>
        <div className="featured-case-meta">
          <span className="badge">⏱ {c.minutes} دقيقة</span>
          <DifficultyDots level={c.difficulty} />
          <CaseStatusBadge prog={prog} />
        </div>
        <div className="featured-case-cta" style={{ marginBlockStart: "0.75rem" }}>
          <span className="btn btn-primary btn-sm">{ctaLabel}</span>
        </div>
      </div>
    </Link>
  );
}

/* ─── dossier case card ─── */
function DossierCard({ c, prog }: { c: Card; prog?: Prog }) {
  const href = prog && !prog.done ? `/play/${c.case_id}` : `/case/${c.case_id}`;
  const ctaLabel = prog?.done ? "مراجعة" : prog ? "تابع" : c.tutorial ? "ابدأ التدريب" : "افتح الملف";
  const idNum = c.case_id.replace(/\D/g, "").padStart(3, "0");

  return (
    <div className="dossier">
      <span className="dossier-tab">{c.kicker_ar}</span>
      <Link href={href} className="card card-link dossier-cover">
        {/* case ID and glyph */}
        <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between" }}>
          <span className="case-id-label">#{idNum}</span>
          <span
            aria-hidden
            style={{
              fontSize: "2rem",
              lineHeight: 1,
              opacity: 0.75,
              transition: "opacity 200ms ease, transform 220ms ease",
            }}
          >
            {c.glyph || "📁"}
          </span>
        </div>

        {/* title + description */}
        <div className="stack-sm" style={{ flex: 1 }}>
          <h3 className="card-title">{c.title_ar}</h3>
          <p className="small dim-2" style={{ lineHeight: 1.65 }}>{c.tagline_ar}</p>
        </div>

        {/* metadata row */}
        <div className="row small" style={{ gap: "0.4rem", flexWrap: "wrap" }}>
          <span className="badge">⏱ {c.minutes} د</span>
          <DifficultyDots level={c.difficulty} />
          {c.tutorial && <span className="badge badge-amber">تمهيدية</span>}
          {c.preview && <span className="badge badge-warning">تجريبية</span>}
        </div>

        {/* status + CTA */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            gap: "0.5rem",
            marginBlockStart: "0.25rem",
          }}
        >
          <CaseStatusBadge prog={prog} />
          <span
            style={{
              fontSize: "0.8125rem",
              fontWeight: 600,
              color: "var(--accent)",
              textDecoration: "none",
              whiteSpace: "nowrap",
            }}
          >
            {ctaLabel} ←
          </span>
        </div>
      </Link>
    </div>
  );
}

/* ─── progress summary ─── */
function ProgressSummary({
  cards,
  prog,
}: {
  cards: Card[];
  prog: Prog[];
}) {
  const done      = prog.filter((p: Prog) => p.done).length;
  const inProgress = prog.filter((p: Prog) => !p.done).length;
  const total     = cards.length;

  if (total === 0) return null;
  return (
    <div
      style={{
        display: "flex",
        gap: "1.5rem",
        padding: "0.875rem 1.25rem",
        background: "var(--surface)",
        border: "1px solid var(--border)",
        borderRadius: "var(--radius-card)",
        flexWrap: "wrap",
        alignItems: "center",
      }}
    >
      <div className="hero-stat">
        <span className="hero-stat-value">{total}</span>
        <span className="hero-stat-label">قضية متاحة</span>
      </div>
      <div className="hero-stat">
        <span className="hero-stat-value" style={{ color: "var(--positive)" }}>{done}</span>
        <span className="hero-stat-label">مكتملة</span>
      </div>
      {inProgress > 0 && (
        <div className="hero-stat">
          <span className="hero-stat-value" style={{ color: "var(--accent)" }}>{inProgress}</span>
          <span className="hero-stat-label">قيد التحقيق</span>
        </div>
      )}
      {/* progress bar */}
      <div style={{ flex: 1, minInlineSize: "8rem" }}>
        <div className="mastery-track" style={{ blockSize: "6px" }}>
          <div
            className="mastery-fill"
            style={{ inlineSize: total > 0 ? `${Math.round((done / total) * 100)}%` : "0%" }}
          />
        </div>
        <p className="text-meta" style={{ marginBlockStart: "0.3rem" }}>
          {total > 0 ? Math.round((done / total) * 100) : 0}٪ مكتمل
        </p>
      </div>
    </div>
  );
}

/* ─── filter buttons ─── */
const FILTERS: { id: Filter; label: string }[] = [
  { id: "all",        label: "جميع القضايا" },
  { id: "new",        label: "جديدة" },
  { id: "inprogress", label: "قيد التحقيق" },
  { id: "done",       label: "مكتملة" },
];

/* ─── main page ─── */
export default function Cases() {
  const [cards,   setCards]   = useState<Card[] | null>(null);
  const [prog,    setProg]    = useState<Prog[]>([]);
  const [failed,  setFailed]  = useState(false);
  const [filter,  setFilter]  = useState<Filter>("all");

  useEffect(() => {
    api<{ cards: Card[]; cases: Prog[] }>("/api/progress", { tokens: allTokens() })
      .then((r) => { setCards(r.cards); setProg(r.cases); })
      .catch(() => setFailed(true));
  }, []);

  /* pick a featured case: in-progress first, else tutorial, else first */
  const featured = useMemo<Card | null>(() => {
    if (!cards || cards.length === 0) return null;
    const inProgressId = prog.find((p: Prog) => !p.done)?.case_id;
    if (inProgressId) return cards.find((c: Card) => c.case_id === inProgressId) ?? null;
    const tutorial = cards.find((c: Card) => c.tutorial);
    return tutorial ?? cards[0] ?? null;
  }, [cards, prog]);

  /* filter the REST (exclude featured from grid) */
  const gridCards = useMemo<Card[]>(() => {
    if (!cards) return [];
    let list = cards.filter((c: Card) => c.case_id !== featured?.case_id);
    if (filter === "new")        list = list.filter((c: Card) => !prog.find((p: Prog) => p.case_id === c.case_id));
    if (filter === "inprogress") list = list.filter((c: Card) => prog.find((p: Prog) => p.case_id === c.case_id && !p.done));
    if (filter === "done")       list = list.filter((c: Card) => prog.find((p: Prog) => p.case_id === c.case_id && p.done));
    return list;
  }, [cards, prog, filter, featured]);

  /* counts for filter badges */
  const counts = useMemo(() => ({
    all:        (cards?.length ?? 0) - (featured ? 1 : 0),
    new:        (cards ?? []).filter((c: Card) => c.case_id !== featured?.case_id && !prog.find((p: Prog) => p.case_id === c.case_id)).length,
    inprogress: (cards ?? []).filter((c: Card) => c.case_id !== featured?.case_id && prog.find((p: Prog) => p.case_id === c.case_id && !p.done)).length,
    done:       (cards ?? []).filter((c: Card) => c.case_id !== featured?.case_id && prog.find((p: Prog) => p.case_id === c.case_id && p.done)).length,
  }), [cards, prog, featured]);

  /* ── render ── */
  return (
    <>
      {/* ── HERO ── */}
      <header className="cases-hero">
        <p className="cases-hero-kicker">أرشيف التحقيقات</p>
        <h1>القضايا</h1>
        <p className="cases-hero-tagline">
          كل ملف يخفي حقيقة. وكل دليل يقربك منها.
          <br />
          <span style={{ opacity: 0.75 }}>اختر قضيتك، افحص الأدلة، واختبر قدرتك على كشف الحقيقة.</span>
        </p>
        {cards && cards.length > 0 && (
          <div className="cases-hero-stats">
            <div className="hero-stat">
              <span className="hero-stat-value">{cards.length}</span>
              <span className="hero-stat-label">قضية</span>
            </div>
            {prog.filter((p: Prog) => p.done).length > 0 && (
              <div className="hero-stat">
                <span className="hero-stat-value" style={{ color: "var(--positive)" }}>
                  {prog.filter((p: Prog) => p.done).length}
                </span>
                <span className="hero-stat-label">مكتملة</span>
              </div>
            )}
            {prog.filter((p: Prog) => !p.done).length > 0 && (
              <div className="hero-stat">
                <span className="hero-stat-value" style={{ color: "var(--accent)" }}>
                  {prog.filter((p: Prog) => !p.done).length}
                </span>
                <span className="hero-stat-label">قيد التحقيق</span>
              </div>
            )}
          </div>
        )}
      </header>

      {/* ── ERROR / LOADING ── */}
      {failed && (
        <div className="error-state">
          <span style={{ fontSize: "2rem" }}>⚠️</span>
          <h2>تعذّر تحميل القضايا</h2>
          <p>تحقق من الاتصال ثم أعد المحاولة.</p>
          <button className="btn btn-ghost btn-sm" onClick={() => window.location.reload()}>
            إعادة المحاولة
          </button>
        </div>
      )}

      {!failed && !cards && <CasesSkeleton />}

      {!failed && cards && cards.length === 0 && (
        <div className="empty-state">
          <FolderIcon size={32} />
          <h2>لا قضايا متاحة</h2>
          <p>لا قضايا متاحة لفئتك العمرية حالياً.</p>
        </div>
      )}

      {/* ── CONTENT ── */}
      {!failed && cards && cards.length > 0 && (
        <>
          {/* progress summary */}
          {prog.length > 0 && (
            <ProgressSummary cards={cards} prog={prog} />
          )}

          {/* featured case */}
          {featured && (
            <section>
              <div className="section-header" style={{ marginBlockEnd: "0.75rem" }}>
                <h2 className="text-label section-title">
                  {prog.find((p: Prog) => p.case_id === featured.case_id && !p.done)
                    ? "تابع تحقيقك"
                    : "القضية المميزة"}
                </h2>
              </div>
              <FeaturedCase
                c={featured}
                prog={prog.find((p: Prog) => p.case_id === featured.case_id)}
              />
            </section>
          )}

          {/* filter bar + cases grid */}
          {gridCards !== null && (cards.length > 1) && (
            <section>
              <div className="section-header" style={{ marginBlockEnd: "0.75rem" }}>
                <h2 className="text-label section-title">أرشيف القضايا</h2>
              </div>

              {/* filters */}
              <div
                className="filter-bar"
                role="group"
                aria-label="تصفية القضايا"
                style={{ marginBlockEnd: "1rem" }}
              >
                {FILTERS.map(({ id, label }) => {
                  const count = counts[id];
                  return (
                    <button
                      key={id}
                      className={`filter-btn${filter === id ? " active" : ""}`}
                      aria-pressed={filter === id}
                      onClick={() => setFilter(id)}
                    >
                      {label}
                      {count > 0 && (
                        <span
                          style={{
                            background: filter === id ? "var(--accent)" : "var(--surface-muted)",
                            color: filter === id ? "var(--accent-contrast)" : "var(--foreground-muted)",
                            borderRadius: "var(--radius-pill)",
                            fontSize: "0.6875rem",
                            fontWeight: 700,
                            padding: "0 0.35rem",
                            lineHeight: "1.4",
                          }}
                        >
                          {count}
                        </span>
                      )}
                    </button>
                  );
                })}
              </div>

              {/* grid */}
              {gridCards.length === 0 ? (
                <div className="empty-state" style={{ minBlockSize: "8rem" }}>
                  <p>لا توجد قضايا في هذه الفئة.</p>
                </div>
              ) : (
                <div className="cases-grid">
                  {gridCards.map((c: Card) => (
                    <DossierCard
                      key={c.case_id}
                      c={c}
                      prog={prog.find((p: Prog) => p.case_id === c.case_id)}
                    />
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
