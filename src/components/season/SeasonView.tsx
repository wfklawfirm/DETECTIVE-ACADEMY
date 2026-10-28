"use client";
import { useEffect, useMemo, useState } from "react";
import { LinkButton } from "@/components/ui/button";
import { ErrorState, LoadingRegion } from "@/components/ui/feedback";
import { ProgressBar } from "@/components/ui/progress";
import { SearchIcon } from "@/components/ui/icons";
import {
  episodeState,
  recommendedEpisode,
  type EpState,
  type ResolvedEpisode,
  type Season,
} from "@/engine/seasons";
import { allTokens, api } from "@/lib/client";

interface Cd { case_id: string; title_ar: string; minutes: number; difficulty: number; age_band: string }
interface Pg { case_id: string; done: boolean }

type EpStateLabel = { t: string; tone: "neutral"|"positive"|"brand"|"warning"|"info" };
const LABEL: Record<EpState, EpStateLabel> = {
  done:        { t: "أُنجزت",                   tone: "positive" },
  in_progress: { t: "قيد التحقيق",              tone: "brand"    },
  recommended: { t: "التالية المقترحة",          tone: "brand"    },
  open:        { t: "متاحة",                     tone: "neutral"  },
  coming:      { t: "قريباً",                    tone: "info"     },
  other_band:  { t: "غير متاحة لك الآن",         tone: "warning"  },
  practice:    { t: "تدريب",                     tone: "info"     },
};

const EP_KIND_GLYPH: Record<string, string> = {
  tutorial: "🎓",
  episode:  "🔍",
  finale:   "🏆",
  transfer: "🔄",
  break:    "💡",
};

/* ── Episode card ────────────────────────────────────────────── */
function EpisodeCard({
  e, s, state, cardOf, isRec,
}: {
  e: ResolvedEpisode;
  s: ReturnType<typeof episodeState>;
  state: EpState;
  cardOf: (id: string) => Cd | undefined;
  isRec: boolean;
}) {
  const L = LABEL[state];
  const glyph = EP_KIND_GLYPH[e.kind] ?? "📁";
  const isLocked = state === "coming" || state === "other_band";
  const targets = e.kind === "break" ? [] : s.case_ids.length ? s.case_ids : [];

  return (
    <li className={`season-ep${isRec ? " season-ep--rec" : ""}${isLocked ? " season-ep--locked" : ""}${state === "done" ? " season-ep--done" : ""}`}>
      <div className="season-ep-header">
        <span className="season-ep-glyph" aria-hidden>{glyph}</span>
        <div className="season-ep-meta">
          <div className="season-ep-toprow">
            <h3 className="season-ep-title">{e.title_ar}</h3>
            <span className={`season-ep-chip season-ep-chip--${L.tone}`}>{L.t}</span>
          </div>
          <p className="season-ep-hook">{e.hook_ar}</p>
          <p className="season-ep-principle">
            <span className="season-ep-principle-label">الفكرة: </span>
            {e.principle_ar}
          </p>
        </div>
      </div>

      {e.kind === "break" && e.link && (
        <LinkButton variant="outline" size="sm" href={e.link.href}>
          {e.link.label_ar}
        </LinkButton>
      )}

      {targets.length > 0 && (
        <div className="season-ep-actions">
          {targets.map((id) => {
            const c = cardOf(id);
            if (!c) return null;
            const isActive = state === "recommended" || state === "in_progress";
            const ctaLabel =
              state === "done"        ? `راجع: ${c.title_ar}` :
              state === "in_progress" ? `تابع: ${c.title_ar}` :
                                        `افتح: ${c.title_ar}`;
            const href = state === "in_progress" ? `/play/${id}` : `/case/${id}`;
            return (
              <LinkButton key={id} variant={isActive ? "primary" : "outline"} block href={href}>
                {ctaLabel}
              </LinkButton>
            );
          })}
        </div>
      )}

      {e.pending.length > 0 && (
        <p className="season-ep-pending">{e.pending.length} ملفات إضافية قيد الإعداد.</p>
      )}
    </li>
  );
}

/* ── Main view ───────────────────────────────────────────────── */
export function SeasonView({
  season,
  episodes,
}: {
  season: Omit<Season, "episodes">;
  episodes: ResolvedEpisode[];
}) {
  const [d, setD] = useState<{ cards: Cd[]; cases: Pg[] } | null>(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    api<{ cards: Cd[]; cases: Pg[] }>("/api/progress", { tokens: allTokens() })
      .then(setD)
      .catch(() => setFailed(true));
  }, []);

  const view = useMemo(() => {
    if (!d) return null;
    const facts = {
      playable: new Set(d.cards.map((c) => c.case_id)),
      done:     new Set(d.cases.filter((c) => c.done).map((c) => c.case_id)),
      started:  new Set(d.cases.map((c) => c.case_id)),
    };
    const rec  = recommendedEpisode(episodes, facts);
    const rows = episodes.map((e) => ({ e, s: episodeState(e, facts) }));
    const path = rows.filter(
      (r) =>
        ["tutorial", "episode", "finale", "transfer"].includes(r.e.kind) &&
        r.s.state !== "other_band",
    );
    return {
      rec,
      rows,
      doneN:  path.filter((r) => r.s.state === "done").length,
      totalN: path.length,
    };
  }, [d, episodes]);

  const cardOf = (id: string) => d?.cards.find((c) => c.case_id === id);
  const recEp  = view?.rec ? episodes.find((e) => e.id === view.rec) : undefined;

  return (
    <>
      {/* ── Cinematic hero ─────────────────────────────────────── */}
      <header className="season-hero">
        <div className="season-hero-inner">
          <div className="season-hero-text">
            <p className="season-hero-kicker">موسم · سلسلة القضايا</p>
            <h1 className="season-hero-title">{season.title_ar}</h1>
            <p className="season-hero-sub">{season.lead_ar}</p>
          </div>
          <div className="season-hero-badge" aria-hidden>
            <span className="season-hero-glyph">📺</span>
          </div>
        </div>

        {/* Progress strip */}
        {view && view.totalN > 0 && (
          <div className="season-hero-progress">
            <div className="season-progress-stats">
              <span className="season-progress-done">{view.doneN}</span>
              <span className="season-progress-sep">/</span>
              <span className="season-progress-total">{view.totalN}</span>
              <span className="season-progress-label">حلقة منجزة</span>
            </div>
            <ProgressBar value={view.doneN} max={Math.max(1, view.totalN)} label="تقدّم الموسم" />
          </div>
        )}
      </header>

      {/* ── Season hook ────────────────────────────────────────── */}
      <aside className="season-hook-card" aria-label="خيط الموسم">
        <span className="season-hook-mark">
          <SearchIcon size={14} />
          خيط الموسم
        </span>
        <p className="season-hook-text">
          {recEp
            ? recEp.hook_ar
            : "ست خيوط تبدو متفقة، وواحد منها فقط يحمل الحقيقة. من أين تبدأ؟"}
        </p>
      </aside>

      {/* ── Note strip ─────────────────────────────────────────── */}
      <div className="season-note-strip">
        <span className="season-note-icon" aria-hidden>💡</span>
        <p>{season.note_ar}</p>
      </div>

      {/* ── States ─────────────────────────────────────────────── */}
      {failed ? (
        <ErrorState
          title="تعذّر تحميل تقدّمك في الموسم"
          action={
            <button className="btn btn-outline btn-sm" onClick={() => location.reload()}>
              أعد المحاولة
            </button>
          }
        />
      ) : !view ? (
        <LoadingRegion cards={4} />
      ) : (
        <ol className="season-ep-list list" style={{ listStyle: "none", padding: 0 }}>
          {view.rows.map(({ e, s }) => {
            const state: EpState = e.id === view.rec ? "recommended" : s.state;
            return (
              <EpisodeCard
                key={e.id}
                e={e}
                s={s}
                state={state}
                cardOf={cardOf}
                isRec={e.id === view.rec}
              />
            );
          })}
        </ol>
      )}
    </>
  );
}
