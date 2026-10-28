"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { CaseCard, type Card, type Prog } from "@/components/CaseCard";
import { EntryHook } from "@/components/EntryHook";
import { Badge } from "@/components/ui/badge";
import { LinkButton } from "@/components/ui/button";
import { ErrorState, LoadingRegion } from "@/components/ui/feedback";
import { ProgressBar, ProgressRing } from "@/components/ui/progress";
import { allTokens, api, deviceSeed } from "@/lib/client";

interface Riddle { id: string; title_ar: string; prompt_ar: string }

/* ── Skeleton for loading ─────────────────────────────────────── */
function HomeSkeleton() {
  return (
    <div className="home-skeleton" aria-hidden>
      <div className="skeleton" style={{ height: "14rem", borderRadius: "1rem" }} />
      <div className="skeleton" style={{ height: "7rem", borderRadius: "0.75rem", marginTop: "1.25rem" }} />
      <div className="skeleton" style={{ height: "7rem", borderRadius: "0.75rem", marginTop: "1rem" }} />
    </div>
  );
}

/* ── Rank badge ───────────────────────────────────────────────── */
function InvestigatorRank({ done, total }: { done: number; total: number }) {
  const pct = total > 0 ? done / total : 0;
  let rank = "مجنّد جديد";
  let rankEn = "Recruit";
  if (pct >= 0.9) { rank = "محقق أول"; rankEn = "Lead Detective"; }
  else if (pct >= 0.6) { rank = "محقق متقدم"; rankEn = "Senior Investigator"; }
  else if (pct >= 0.3) { rank = "محقق"; rankEn = "Investigator"; }
  else if (pct >= 0.1) { rank = "متدرب"; rankEn = "Trainee"; }
  return (
    <div className="rank-badge">
      <span className="rank-label">رتبة</span>
      <span className="rank-title">{rank}</span>
      <span className="rank-en">{rankEn}</span>
    </div>
  );
}

/* ── Featured / primary action card ───────────────────────────── */
function PrimaryAction({
  lead, leadCard, next,
}: {
  lead: Prog | undefined;
  leadCard: Card | undefined;
  next: Card[];
}) {
  if (lead && leadCard) {
    return (
      <div className="home-primary-card">
        <div className="home-primary-glyph" aria-hidden>{leadCard.glyph ?? "🔍"}</div>
        <div className="home-primary-body">
          <span className="home-primary-kicker">{leadCard.kicker_ar} · قيد التحقيق</span>
          <h2 className="home-primary-title">{leadCard.title_ar}</h2>
          <p className="home-primary-meta">
            {lead.evidence_count} دليلاً في خزانتك
            {lead.locked_count > 0 ? ` · ${lead.locked_count} لم يُكشف بعد` : ""}
          </p>
          <LinkButton variant="primary" size="lg" block href={`/play/${lead.case_id}`}>
            تابع التحقيق
          </LinkButton>
        </div>
      </div>
    );
  }
  if (next[0]) {
    return (
      <div className="home-primary-card">
        <div className="home-primary-glyph" aria-hidden>{next[0].glyph ?? "📁"}</div>
        <div className="home-primary-body">
          <span className="home-primary-kicker">{next[0].kicker_ar} · ملف جديد</span>
          <h2 className="home-primary-title">{next[0].title_ar}</h2>
          <p className="home-primary-meta">{next[0].tagline_ar}</p>
          <div className="home-primary-badges">
            <Badge>{next[0].minutes} دقيقة</Badge>
            {next[0].preview && <Badge tone="warning">نسخة تجريبية</Badge>}
          </div>
          <LinkButton variant="primary" size="lg" block href={`/case/${next[0].case_id}`}>
            افتح الملف
          </LinkButton>
        </div>
      </div>
    );
  }
  return (
    <div className="home-primary-card home-primary-card--done">
      <div className="home-primary-glyph" aria-hidden>🏆</div>
      <div className="home-primary-body">
        <span className="home-primary-kicker">إنجاز · مميز</span>
        <h2 className="home-primary-title">أنجزت كل القضايا المتاحة</h2>
        <p className="home-primary-meta">تدرّب على مهارة واحدة بسجلات خيالية، أو راجع درساً في الأكاديمية.</p>
        <div className="row-sm">
          <LinkButton variant="primary" size="lg" href="/labs">المختبرات</LinkButton>
          <LinkButton variant="outline" size="lg" href="/academy">الأكاديمية</LinkButton>
        </div>
      </div>
    </div>
  );
}

/* ── Main page ─────────────────────────────────────────────────── */
export default function Home() {
  const [d, setD] = useState<{ cards: Card[]; cases: Prog[] } | null>(null);
  const [failed, setFailed] = useState(false);
  const [riddle, setRiddle] = useState<Riddle | null | undefined>(undefined);

  useEffect(() => {
    api<{ cards: Card[]; cases: Prog[] }>("/api/progress", { tokens: allTokens() })
      .then(setD)
      .catch(() => setFailed(true));
    api<{ riddle: Riddle }>(`/api/riddle?seed=${encodeURIComponent(deviceSeed())}`)
      .then((x) => setRiddle(x.riddle))
      .catch(() => setRiddle(null));
  }, []);

  const open = d?.cases.filter((c: Prog) => !c.done).sort((a: Prog, b: Prog) => b.updated_at.localeCompare(a.updated_at)) ?? [];
  const doneIds = new Set(d?.cases.filter((c: Prog) => c.done).map((c: Prog) => c.case_id));
  const next = d?.cards.filter((c: Card) => !doneIds.has(c.case_id) && !open.some((o: Prog) => o.case_id === c.case_id)) ?? [];
  const cardOf = (id: string) => d?.cards.find((x: Card) => x.case_id === id);
  const lead = open[0];
  const leadCard = lead ? cardOf(lead.case_id) : undefined;
  const total = d?.cards.length ?? 0;
  const done = d?.cards.filter((c: Card) => doneIds.has(c.case_id)).length ?? 0;

  if (failed) {
    return (
      <>
        <EntryHook surface="home" />
        <ErrorState
          title="تعذّر تحميل ملفاتك"
          body="تحقق من الاتصال ثم أعد المحاولة."
          action={
            <button className="btn btn-outline btn-sm" onClick={() => location.reload()}>
              أعد المحاولة
            </button>
          }
        />
      </>
    );
  }

  return (
    <>
      <EntryHook surface="home" />

      {/* ── Hero ──────────────────────────────────────────────── */}
      <header className="home-hero">
        <div className="home-hero-inner">
          <div className="home-hero-text">
            <p className="home-hero-kicker">أكاديمية المحقق · مركز العمليات</p>
            <h1 className="home-hero-title">ملفاتي</h1>
            <p className="home-hero-sub">كل قضية فرصة لبناء عقل يحلل ولا يُخدع.</p>
          </div>
          {d && <InvestigatorRank done={done} total={total} />}
        </div>

        {/* Progress strip */}
        {d && total > 0 && (
          <div className="home-hero-progress">
            <div className="home-hero-stats">
              <div className="home-hero-stat">
                <span className="home-stat-value">{total}</span>
                <span className="home-stat-label">قضية</span>
              </div>
              <div className="home-hero-stat">
                <span className="home-stat-value">{done}</span>
                <span className="home-stat-label">منجزة</span>
              </div>
              <div className="home-hero-stat">
                <span className="home-stat-value">{open.length}</span>
                <span className="home-stat-label">مفتوحة</span>
              </div>
              <div className="home-hero-stat">
                <span className="home-stat-value">{next.length}</span>
                <span className="home-stat-label">جديدة</span>
              </div>
            </div>
            <ProgressBar value={done} max={total} label="نسبة القضايا المنجزة" />
          </div>
        )}
      </header>

      {/* ── Content ───────────────────────────────────────────── */}
      {!d ? (
        <HomeSkeleton />
      ) : (
        <div className="home-content">

          {/* Primary action */}
          <section aria-label="الإجراء الرئيسي">
            <p className="home-section-kicker">
              {lead ? "أكمل من حيث توقفت" : next.length ? "ابدأ من هنا" : "ما التالي"}
            </p>
            <PrimaryAction lead={lead} leadCard={leadCard} next={next} />
          </section>

          {/* Season card */}
          <section className="home-info-grid" aria-label="موارد إضافية">
            <div className="home-info-card">
              <span className="home-info-icon" aria-hidden>📺</span>
              <div>
                <p className="home-info-label">موسم</p>
                <h3 className="home-info-title">الموسم الأول: خيوط لا تتفق</h3>
                <p className="home-info-body small dim-2">ثماني حلقات بترتيب مقترح. كل حلقة تضيف عادة تفكير.</p>
                <Link href="/season" className="home-info-link">افتح الموسم ←</Link>
              </div>
            </div>

            {/* Daily riddle card */}
            <div className="home-info-card">
              <span className="home-info-icon" aria-hidden>🧩</span>
              <div>
                <p className="home-info-label">اليوم</p>
                <h3 className="home-info-title">تحدي اليوم</h3>
                {riddle === undefined ? (
                  <span className="skeleton skel-line" aria-hidden />
                ) : riddle ? (
                  <p className="home-info-body small dim-2">{riddle.title_ar}</p>
                ) : (
                  <p className="home-info-body small dim-2">لغز قصير من تأليفنا، جديد كل يوم.</p>
                )}
                <Link href="/challenges" className="home-info-link">جرّب اللغز ←</Link>
              </div>
            </div>
          </section>

          {/* Progress ring — only if has done cases */}
          {done > 0 && (
            <section className="home-mastery-card" aria-labelledby="mastery-h">
              <div className="home-mastery-ring">
                <ProgressRing
                  value={done}
                  max={total}
                  text={`${done}/${total}`}
                  size={72}
                  label={`أنجزت ${done} من ${total} قضايا`}
                />
              </div>
              <div className="home-mastery-body">
                <h2 id="mastery-h" className="home-mastery-title">تقدّمك</h2>
                <p className="small dim-2">أنهيت {done} من {total} قضايا.</p>
                <LinkButton variant="outline" size="sm" href="/profile">شاهد مهاراتك</LinkButton>
              </div>
            </section>
          )}

          {/* Open investigations */}
          {open.length > 1 && (
            <section aria-labelledby="open-h">
              <p className="home-section-kicker" id="open-h">تحقيقات مفتوحة أخرى</p>
              <div className="home-cases-list">
                {open.slice(1).map((p: Prog) => {
                  const c = cardOf(p.case_id);
                  return c ? <CaseCard key={p.case_id} c={c} p={p} /> : null;
                })}
              </div>
            </section>
          )}

          {/* New cases */}
          {next.length > (lead ? 0 : 1) && (
            <section aria-labelledby="new-h">
              <p className="home-section-kicker" id="new-h">ملفات أخرى</p>
              <div className="home-cases-list">
                {next.slice(lead ? 0 : 1).map((c: Card) => <CaseCard key={c.case_id} c={c} />)}
              </div>
            </section>
          )}
        </div>
      )}
    </>
  );
}
