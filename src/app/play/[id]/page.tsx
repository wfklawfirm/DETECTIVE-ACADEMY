"use client";
import { use, useEffect, useRef, useState, type ReactNode } from "react";
import { EntryHook } from "@/components/EntryHook";
import { BoardTab } from "@/components/play/Board";
import { BriefTab } from "@/components/play/Brief";
import { DeduceTab } from "@/components/play/Deduce";
import { Debrief } from "@/components/play/Debrief";
import { EvidenceTab } from "@/components/play/Evidence";
import { JournalTab } from "@/components/play/Journal";
import { PeopleTab } from "@/components/play/People";
import { TimeTab } from "@/components/play/Time";
import { usePlay } from "@/components/play/usePlay";
import { Badge } from "@/components/ui/badge";
import { Button, LinkButton } from "@/components/ui/button";
import { ErrorState, LoadingRegion } from "@/components/ui/feedback";
import { BoardIcon, ClockIcon, EvidenceIcon, FileIcon, PenIcon, ScaleIcon, UsersIcon } from "@/components/ui/icons";
import { useToast } from "@/components/ui/toast";

const TABS: readonly [string, string, (p: { size: number }) => ReactNode][] = [
  ["brief", "الملف", FileIcon], ["evidence", "الأدلة", EvidenceIcon], ["people", "الشخصيات", UsersIcon], ["board", "اللوحة", BoardIcon], ["time", "الزمن", ClockIcon], ["journal", "المفكرة", PenIcon], ["deduce", "الاستنتاج", ScaleIcon],
];
type Tab = string;

export default function Play({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const { resp, view, error, busy, last, send, clearError } = usePlay(id);
  const toast = useToast();
  const [tab, setTab] = useState<Tab>("brief");
  const [seenEv, setSeenEv] = useState(0);
  const main = useRef<HTMLDivElement>(null);
  const [focusChar, setFocusChar] = useState<string | null>(null);
  const go = (t: string, charId?: string) => { setFocusChar(charId ?? null); setTab(t); };
  useEffect(() => { main.current?.focus({ preventScroll: true }); window.scrollTo({ top: 0 }); }, [tab]);
  useEffect(() => { if (tab === "evidence" && view) setSeenEv(view.evidence.length); }, [tab, view]);
  const granted = last?.granted_evidence?.length ?? 0;
  useEffect(() => { if (granted > 0) toast(`أُضيف ${granted} دليل إلى خزانتك`); }, [last, granted, toast]);

  if (error && !view) {
    return (
      <>
        <h1 className="text-page-title">تعذّر فتح الملف</h1>
        <ErrorState title="تعذّر فتح الملف" body={error.message} action={<div className="row"><Button variant="secondary" onClick={() => location.reload()}>أعد المحاولة</Button><LinkButton variant="ghost" href="/cases">القضايا</LinkButton></div>} />
      </>
    );
  }
  if (!view || !resp) return <><h1 className="sr-only">جارٍ فتح الملف</h1><LoadingRegion label="جارٍ فتح الملف" cards={3} /></>;
  const ended = view.machine === "review" || view.machine === "resolved";
  if (ended) return <Debrief r={resp} busy={busy} send={send} />;
  const newEv = Math.max(0, view.evidence.length - seenEv);
  return (
    <>
      <EntryHook surface="case_return" caseId={id} />
      <header className="ref-hero play-hero">
        <div className="row row-between"><span className="kicker">{view.tutorial ? "ملف تمهيدي" : "قضية"}</span>{view.preview && <Badge tone="warning" title="هذه القضية لم تكتمل مراجعتها الخبيرة بعد">نسخة تجريبية</Badge>}</div>
        <h1 className="text-page-title">{view.title_ar}</h1>
      </header>
      <nav className="play-tabs" role="tablist" aria-label="أقسام التحقيق">
        {TABS.map(([k, label, Icon]) => (
          <button key={k} role="tab" aria-selected={tab === k} id={`tab-${k}`} aria-controls="panel" onClick={() => setTab(k)}>
            <Icon size={22} /><span>{label}</span>
            {k === "evidence" && newEv > 0 && tab !== "evidence" && <span className="count" aria-label={`${newEv} جديد`}>{newEv}</span>}
          </button>
        ))}
      </nav>
      <div id="panel" role="tabpanel" aria-labelledby={`tab-${tab}`} ref={main} tabIndex={-1} className="stack-lg" style={{ outline: "none" }}>
        {error && <div role="alert" className="callout" data-tone="negative"><div className="grow">{error.message}</div><Button variant="ghost" size="sm" onClick={clearError}>إغلاق</Button></div>}
        {tab === "brief" && <BriefTab view={view} busy={busy} send={send} last={last} goto={go} />}
        {tab === "evidence" && <EvidenceTab view={view} busy={busy} onTag={(e, c) => send({ op: "tag", evidence_id: e, cls: c })} />}
        {tab === "people" && <PeopleTab key={focusChar ?? "all"} view={view} busy={busy} send={send} initial={focusChar} />}
        {tab === "board" && <BoardTab view={view} busy={busy} send={send} />}
        {tab === "time" && <TimeTab view={view} busy={busy} send={send} last={last} />}
        {tab === "journal" && <JournalTab view={view} busy={busy} send={send} last={last} />}
        {tab === "deduce" && <DeduceTab view={view} busy={busy} send={send} />}
      </div>
    </>
  );
}
