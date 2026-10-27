"use client";
import { useEffect, useRef, useState } from "react";
import { allTokens, api, deviceSeed, gentleMode, nextEntry, pushRecentHook, recentHooks } from "@/lib/client";
import { LinkButton } from "./ui/button";
import { SearchIcon } from "./ui/icons";

interface Resolved { id: string; kind: string; text_ar: string; cta_ar?: string; cta_href?: string }
const MARK: Record<string, string> = { teaser: "خيط جديد", welcome_back: "عودة", cliffhanger: "لم ينتهِ بعد", skill: "مهارة اليوم", challenge: "تحدٍّ" };

/** One spoiler-safe "new lead" at EVERY entry (a fresh visit to landing/home, opening a case, returning to a case). */
export function EntryHook({ surface, caseId }: { surface: "landing" | "home" | "case_open" | "case_return"; caseId?: string }) {
  const [hook, setHook] = useState<Resolved | null>(null);
  const fired = useRef(false);
  useEffect(() => {
    if (fired.current) return; // StrictMode double-invoke guard
    fired.current = true;
    const run = async () => {
      try {
        const r = await api<{ hook: Resolved }>("/api/hook", { surface, case_id: caseId, entry_counter: nextEntry(), recent_ids: recentHooks(), seed: deviceSeed(), gentle: gentleMode(), tokens: allTokens() });
        setHook(r.hook); pushRecentHook(r.hook.id);
      } catch { setHook({ id: "offline", kind: "teaser", text_ar: "في ملف ما تفصيلة صغيرة تنتظر من يلاحظها.", cta_ar: "ابدأ", cta_href: "/start" }); }
    };
    void run();
  }, [surface, caseId]);
  if (!hook) return <div className="lead-card lead-pending" aria-hidden><span className="skeleton skeleton-line" style={{ inlineSize: "30%" }} /><span className="skeleton skeleton-line" /><span className="skeleton skeleton-line" style={{ inlineSize: "80%" }} /></div>;
  return (
    <aside className="lead-card animate-rise" data-kind={hook.kind} aria-label="تلميح الدخول">
      <span className="mark"><SearchIcon size={18} />{MARK[hook.kind] ?? "تلميح"}</span>
      <p>{hook.text_ar}</p>
      {hook.cta_href && hook.cta_ar && <LinkButton variant="outline" size="sm" href={hook.cta_href} style={{ alignSelf: "flex-start" }}>{hook.cta_ar}</LinkButton>}
    </aside>
  );
}
