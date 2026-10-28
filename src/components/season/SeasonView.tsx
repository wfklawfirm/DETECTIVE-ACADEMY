"use client";
import { useEffect, useMemo, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { LinkButton } from "@/components/ui/button";
import { Card, CardTitle, PageHead } from "@/components/ui/card";
import { Callout, ErrorState, LoadingRegion } from "@/components/ui/feedback";
import { ProgressBar } from "@/components/ui/progress";
import { SearchIcon } from "@/components/ui/icons";
import { episodeState, recommendedEpisode, type EpState, type ResolvedEpisode, type Season } from "@/engine/seasons";
import { allTokens, api } from "@/lib/client";

interface Cd { case_id: string; title_ar: string; minutes: number; difficulty: number; age_band: string }
interface Pg { case_id: string; done: boolean }
const LABEL: Record<EpState, { t: string; tone: "neutral" | "positive" | "brand" | "warning" | "info" }> = {
  done: { t: "أُنجزت", tone: "positive" },
  in_progress: { t: "قيد التحقيق", tone: "brand" },
  recommended: { t: "التالية المقترحة", tone: "brand" },
  open: { t: "متاحة", tone: "neutral" },
  coming: { t: "قريباً", tone: "info" },
  other_band: { t: "غير متاحة لك الآن", tone: "warning" },
  practice: { t: "تدريب", tone: "info" },
};

export function SeasonView({ season, episodes }: { season: Omit<Season, "episodes">; episodes: ResolvedEpisode[] }) {
  const [d, setD] = useState<{ cards: Cd[]; cases: Pg[] } | null>(null);
  const [failed, setFailed] = useState(false);
  useEffect(() => { api<{ cards: Cd[]; cases: Pg[] }>("/api/progress", { tokens: allTokens() }).then(setD).catch(() => setFailed(true)); }, []);

  const view = useMemo(() => {
    if (!d) return null;
    const facts = { playable: new Set(d.cards.map((c) => c.case_id)), done: new Set(d.cases.filter((c) => c.done).map((c) => c.case_id)), started: new Set(d.cases.map((c) => c.case_id)) };
    const rec = recommendedEpisode(episodes, facts);
    const rows = episodes.map((e) => ({ e, s: episodeState(e, facts) }));
    const path = rows.filter((r) => ["tutorial", "episode", "finale", "transfer"].includes(r.e.kind) && r.s.state !== "other_band");
    return { rec, rows, doneN: path.filter((r) => r.s.state === "done").length, totalN: path.length };
  }, [d, episodes]);

  const cardOf = (id: string) => d?.cards.find((c) => c.case_id === id);
  const recEp = view?.rec ? episodes.find((e) => e.id === view.rec) : undefined;

  return (
    <>
      <PageHead kicker="موسم" title={season.title_ar} lead={season.lead_ar} />
      <aside className="lead-card" aria-label="تلميح الموسم">
        <span className="mark"><SearchIcon size={18} />خيط الموسم</span>
        <p>{recEp ? recEp.hook_ar : "ست خيوط تبدو متفقة، وواحد منها فقط يحمل الحقيقة. من أين تبدأ؟"}</p>
      </aside>
      <Callout tone="info" title="ترتيب مقترح، لا قفل">{season.note_ar}</Callout>
      {failed ? <ErrorState title="تعذّر تحميل تقدّمك في الموسم" action={<button className="btn btn-outline btn-sm" onClick={() => location.reload()}>أعد المحاولة</button>} /> : !view ? <LoadingRegion cards={4} /> : (
        <>
          <Card as="section" aria-labelledby="se-sum">
            <h2 id="se-sum" className="card-title">مسيرتك في الموسم</h2>
            <p className="small dim-2">{view.doneN === 0 ? "لم تُنهِ حلقة بعد." : `أنهيت ${view.doneN} من ${view.totalN} على المسار المقترح.`}</p>
            <ProgressBar value={view.doneN} max={Math.max(1, view.totalN)} label="تقدّم الموسم" />
          </Card>
          <ol className="list" style={{ listStyle: "none", padding: 0 }}>
            {view.rows.map(({ e, s }) => {
              const state: EpState = e.id === view.rec ? "recommended" : s.state;
              const L = LABEL[state];
              const targets = e.kind === "break" ? [] : s.case_ids.length ? s.case_ids : [];
              return (
                <li key={e.id}>
                  <Card as="article" aria-labelledby={`ep-${e.id}`} flat={state === "coming" || state === "other_band"}>
                    <div className="row row-between">
                      <CardTitle level={3} id={`ep-${e.id}`}>{e.title_ar}</CardTitle>
                      <Badge tone={L.tone}>{L.t}</Badge>
                    </div>
                    <p className="small dim-2">{e.hook_ar}</p>
                    <p className="small"><b>فكرة الحلقة: </b>{e.principle_ar}</p>
                    {e.kind === "break" && e.link && <LinkButton variant="outline" size="sm" href={e.link.href} style={{ alignSelf: "flex-start" }}>{e.link.label_ar}</LinkButton>}
                    {targets.map((id) => {
                      const c = cardOf(id);
                      if (!c) return null;
                      return (
                        <LinkButton key={id} variant={state === "recommended" || state === "in_progress" ? "primary" : "outline"} block href={state === "in_progress" ? `/play/${id}` : `/case/${id}`}>
                          {state === "done" ? "راجع: " : state === "in_progress" ? "تابع: " : "افتح: "}{c.title_ar}
                        </LinkButton>
                      );
                    })}
                    {e.pending.length > 0 && <p className="small dim">{e.pending.length} ملفات إضافية قيد الإعداد ولم تُنشر بعد.</p>}
                  </Card>
                </li>
              );
            })}
          </ol>
        </>
      )}
    </>
  );
}
