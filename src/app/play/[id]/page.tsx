"use client";
import Link from "next/link";
import { use, useEffect, useRef, useState } from "react";
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

const TABS = [["brief", "الملف", "▤"], ["evidence", "الأدلة", "◫"], ["people", "الشخصيات", "☺"], ["board", "اللوحة", "◈"], ["time", "الزمن", "◷"], ["journal", "المفكرة", "✎"], ["deduce", "الاستنتاج", "⚖"]] as const;
type Tab = (typeof TABS)[number][0];

export default function Play({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const { resp, view, error, busy, last, send, clearError } = usePlay(id);
  const [tab, setTab] = useState<Tab>("brief");
  const [seenEv, setSeenEv] = useState(0);
  const main = useRef<HTMLDivElement>(null);
  const [focusChar, setFocusChar] = useState<string | null>(null);
  const go = (t: string, charId?: string) => { setFocusChar(charId ?? null); setTab(t as Tab); };
  useEffect(() => { main.current?.focus({ preventScroll: true }); window.scrollTo({ top: 0 }); }, [tab]);
  useEffect(() => { if (tab === "evidence" && view) setSeenEv(view.evidence.length); }, [tab, view]);

  if (error && !view) {
    return (
      <div className="wrap-narrow stack"><h1>تعذّر فتح الملف</h1><p role="alert">{error.message}</p>
        <div className="row"><button className="btn" onClick={() => location.reload()}>أعد المحاولة</button><Link className="btn ghost" href="/cases">القضايا</Link></div></div>
    );
  }
  if (!view || !resp) return <div className="wrap"><p className="dim" role="status">جارٍ فتح الملف…</p></div>;
  const ended = view.machine === "review" || view.machine === "resolved";
  if (ended) return <Debrief r={resp} busy={busy} send={send} />;
  const newEv = Math.max(0, view.evidence.length - seenEv);
  return (
    <>
      <div className="wrap" style={{ paddingBlockEnd: 8 }}>
        <EntryHook surface="case_return" caseId={id} />
        <div className="row" style={{ justifyContent: "space-between" }}>
          <div><p className="kicker" style={{ margin: 0 }}>{view.tutorial ? "ملف تمهيدي" : "قضية"}</p><h1 style={{ fontSize: "1.6rem", margin: 0 }}>{view.title_ar}</h1></div>
          {view.preview && <span className="chip amber" title="هذه القضية لم تكتمل مراجعتها الخبيرة بعد">نسخة تجريبية</span>}
        </div>
      </div>
      <nav className="play-tabs" role="tablist" aria-label="أقسام التحقيق">
        {TABS.map(([k, label, ico]) => (
          <button key={k} role="tab" aria-selected={tab === k} id={`tab-${k}`} aria-controls="panel" onClick={() => setTab(k)}>
            <span className="ico" aria-hidden>{ico}</span><span>{label}</span>
            {k === "evidence" && newEv > 0 && tab !== "evidence" && <span className="badge" aria-label={`${newEv} جديد`}>{newEv}</span>}
          </button>
        ))}
      </nav>
      <div className="wrap" id="panel" role="tabpanel" aria-labelledby={`tab-${tab}`} ref={main} tabIndex={-1} style={{ outline: "none", paddingBlockStart: 16 }}>
        {error && <div role="alert" className="card" style={{ borderColor: "var(--rose)", marginBlockEnd: 12 }}><span className="err">{error.message}</span> <button className="btn ghost sm" onClick={clearError}>إغلاق</button></div>}
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
