"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { EntryHook } from "@/components/EntryHook";
import { allTokens, api } from "@/lib/client";
import { CaseCard, type Card, type Prog } from "@/components/CaseCard";

export default function Home() {
  const [d, setD] = useState<{ cards: Card[]; cases: Prog[] } | null>(null);
  useEffect(() => { void api<{ cards: Card[]; cases: Prog[] }>("/api/progress", { tokens: allTokens() }).then(setD); }, []);
  const open = d?.cases.filter((c) => !c.done).sort((a, b) => b.updated_at.localeCompare(a.updated_at)) ?? [];
  const doneIds = new Set(d?.cases.filter((c) => c.done).map((c) => c.case_id));
  const next = d?.cards.filter((c) => !doneIds.has(c.case_id) && !open.some((o) => o.case_id === c.case_id)) ?? [];
  return (
    <div className="wrap stack">
      <EntryHook surface="home" />
      <h1>ملفاتي</h1>
      {!d ? <p className="dim">جارٍ التحميل…</p> : (
        <>
          {open.length > 0 && (
            <section className="stack"><h2>أكمل التحقيق</h2>
              <div className="grid cols-2">{open.map((p) => { const c = d.cards.find((x) => x.case_id === p.case_id); return c ? <CaseCard key={p.case_id} c={c} p={p} /> : null; })}</div>
            </section>
          )}
          {next.length > 0 && (
            <section className="stack"><h2>{open.length ? "ملفات أخرى" : "ابدأ من هنا"}</h2>
              <div className="grid cols-2">{next.map((c) => <CaseCard key={c.case_id} c={c} />)}</div>
            </section>
          )}
          {doneIds.size > 0 && <p><Link href="/profile">شاهد مهاراتك المبدئية ←</Link></p>}
        </>
      )}
    </div>
  );
}
