"use client";
import { useEffect, useState } from "react";
import { CaseCard, type Card, type Prog } from "@/components/CaseCard";
import { EntryHook } from "@/components/EntryHook";
import { Badge } from "@/components/ui/badge";
import { LinkButton } from "@/components/ui/button";
import { Card as UiCard, CardTitle, Dossier, PageHead, SectionTitle } from "@/components/ui/card";
import { ErrorState, LoadingRegion } from "@/components/ui/feedback";
import { ProgressBar, ProgressRing } from "@/components/ui/progress";
import { allTokens, api, deviceSeed } from "@/lib/client";

interface Riddle { id: string; title_ar: string; prompt_ar: string }

export default function Home() {
  const [d, setD] = useState<{ cards: Card[]; cases: Prog[] } | null>(null);
  const [failed, setFailed] = useState(false);
  const [riddle, setRiddle] = useState<Riddle | null | undefined>(undefined);
  useEffect(() => {
    api<{ cards: Card[]; cases: Prog[] }>("/api/progress", { tokens: allTokens() }).then(setD).catch(() => setFailed(true));
    api<{ riddle: Riddle }>(`/api/riddle?seed=${encodeURIComponent(deviceSeed())}`).then((x) => setRiddle(x.riddle)).catch(() => setRiddle(null));
  }, []);
  const open = d?.cases.filter((c) => !c.done).sort((a, b) => b.updated_at.localeCompare(a.updated_at)) ?? [];
  const doneIds = new Set(d?.cases.filter((c) => c.done).map((c) => c.case_id));
  const next = d?.cards.filter((c) => !doneIds.has(c.case_id) && !open.some((o) => o.case_id === c.case_id)) ?? [];
  const cardOf = (id: string) => d?.cards.find((x) => x.case_id === id);
  const lead = open[0];
  const leadCard = lead ? cardOf(lead.case_id) : undefined;
  const total = d?.cards.length ?? 0;
  const done = d?.cards.filter((c) => doneIds.has(c.case_id)).length ?? 0;
  return (
    <>
      <EntryHook surface="home" />
      <PageHead title="ملفاتي" />
      {failed ? <ErrorState title="تعذّر تحميل ملفاتك" body="تحقق من الاتصال ثم أعد المحاولة." action={<button className="btn btn-outline btn-sm" onClick={() => location.reload()}>أعد المحاولة</button>} /> : !d ? <LoadingRegion cards={3} /> : (
        <>
          {/* one primary action, driven by real state */}
          <section aria-labelledby="pa-h" className="stack">
            <SectionTitle>{lead ? "أكمل من حيث توقفت" : next.length ? "ابدأ من هنا" : "ما التالي"}</SectionTitle>
            {lead && leadCard ? (
              <Dossier tab={leadCard.kicker_ar}>
                <UiCard className="lantern" raised>
                  <span className="stamp">قيد التحقيق</span>
                  <CardTitle id="pa-h" level={3}>{leadCard.title_ar}</CardTitle>
                  <p className="small dim-2">{lead.evidence_count} دليلاً في خزانتك{lead.locked_count > 0 ? ` · ${lead.locked_count} لم يُكشف بعد` : ""}</p>
                  <LinkButton variant="primary" size="lg" block href={`/play/${lead.case_id}`}>تابع التحقيق</LinkButton>
                </UiCard>
              </Dossier>
            ) : next[0] ? (
              <Dossier tab={next[0].kicker_ar}>
                <UiCard className="lantern" raised>
                  <CardTitle id="pa-h" level={3}>{next[0].title_ar}</CardTitle>
                  <p className="small dim-2">{next[0].tagline_ar}</p>
                  <div className="row small"><Badge>{next[0].minutes} دقيقة</Badge>{next[0].preview && <Badge tone="warning">نسخة تجريبية قيد المراجعة</Badge>}</div>
                  <LinkButton variant="primary" size="lg" block href={`/case/${next[0].case_id}`}>افتح الملف</LinkButton>
                </UiCard>
              </Dossier>
            ) : (
              <UiCard raised>
                <CardTitle id="pa-h" level={3}>جرّب مختبراً أو درساً</CardTitle>
                <p className="small dim-2">أنجزت كل القضايا المتاحة لفئتك. تدرّب على مهارة واحدة بسجلات خيالية، أو راجع درساً في الأكاديمية.</p>
                <LinkButton variant="primary" size="lg" block href="/labs">افتح المختبرات</LinkButton>
                <LinkButton variant="ghost" block href="/academy">الأكاديمية</LinkButton>
              </UiCard>
            )}
          </section>

          {total > 0 && (
            <UiCard as="section" aria-labelledby="sum-h">
              <div className="row" style={{ flexWrap: "nowrap" }}>
                <ProgressRing value={done} max={total} text={`${done}/${total}`} size={64} label={`أنجزت ${done} من ${total} قضايا`} />
                <div className="stack-sm grow">
                  <h2 id="sum-h" className="card-title">تقدّمك</h2>
                  <p className="small dim-2">{done === 0 ? "لم تُنهِ قضية بعد." : `أنهيت ${done} من ${total} قضايا.`}</p>
                </div>
              </div>
              <ProgressBar value={done} max={total} label="نسبة القضايا المنجزة" />
              {done > 0 && <LinkButton variant="outline" size="sm" href="/profile">شاهد مهاراتك المبدئية</LinkButton>}
            </UiCard>
          )}

          {/* self-contained "today" card */}
          <UiCard as="section" aria-labelledby="today-h">
            <p className="text-label">اليوم</p>
            <h2 id="today-h" className="card-title">تحدي اليوم</h2>
            {riddle === undefined ? <span className="skeleton skeleton-line" aria-hidden /> : riddle ? <p className="small dim-2">{riddle.title_ar}. لغز قصير من تأليفنا، بلا نقاط ولا سلاسل.</p> : <p className="small dim-2">لغز قصير من تأليفنا، جديد كل يوم.</p>}
            <LinkButton variant="outline" size="sm" href="/challenges" style={{ alignSelf: "flex-start" }}>جرّب اللغز</LinkButton>
          </UiCard>

          {open.length > 1 && (
            <section className="stack"><SectionTitle>تحقيقات مفتوحة أخرى</SectionTitle>
              {open.slice(1).map((p) => { const c = cardOf(p.case_id); return c ? <CaseCard key={p.case_id} c={c} p={p} /> : null; })}
            </section>
          )}
          {next.length > (lead ? 0 : 1) && (
            <section className="stack"><SectionTitle>ملفات أخرى</SectionTitle>
              {next.slice(lead ? 0 : 1).map((c) => <CaseCard key={c.case_id} c={c} />)}
            </section>
          )}
        </>
      )}
    </>
  );
}
