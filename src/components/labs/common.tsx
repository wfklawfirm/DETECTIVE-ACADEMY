"use client";
import { useEffect, useRef, type ReactNode } from "react";
import Link from "next/link";
import type { Lab } from "@/engine/labs";
import { Button } from "../ui/button";
import { Card } from "../ui/card";

interface FirstLesson { id: string; title_ar: string }
interface NextLab { id: string; title_ar: string; skill_ar: string }

/** Closing card shared by every lab kind: the score line, the transfer question, the explicit limit ("what this cannot prove") and a retry.
 *  Also saves lab completion to the server once per session. */
export function LabEnd({ lab, summary, onRetry, firstLesson, nextLab }: { lab: Lab; summary: ReactNode; onRetry: () => void; firstLesson?: FirstLesson | null; nextLab?: NextLab | null }) {
  const saved = useRef(false);
  useEffect(() => {
    if (saved.current) return;
    saved.current = true;
    fetch("/api/labs/progress", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ lab_id: lab.id }),
    }).catch(() => {/* best-effort; no UI feedback needed */});
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  return (
    <Card as="section" aria-live="polite" aria-label="خلاصة المختبر">
      <p>{summary} الغرض هنا فهم الفكرة، والنتيجة لا تُحفظ ولا تدخل في ملفك.</p>
      <p><b>سؤال للتفكير: </b>{lab.transfer_ar}</p>
      <div className="lab-limit"><b>ما لا يثبته هذا المختبر: </b>{lab.boundary_ar}</div>
      {lab.illustrative_ar && <p className="small dim">{lab.illustrative_ar}</p>}
      <Button variant="secondary" onClick={onRetry}>أعد المحاولة</Button>
      {firstLesson && (
        <Link href={`/academy/${firstLesson.id}`} className="lab-end-lesson-link">
          تعمّق في الدرس المرتبط: {firstLesson.title_ar} ←
        </Link>
      )}
      {nextLab && (
        <Link href={`/labs/${nextLab.id}`} className="lab-end-next-link">
          <span className="lab-end-next-label">المختبر التالي</span>
          <span className="lab-end-next-title">{nextLab.title_ar}</span>
          <span className="small dim">{nextLab.skill_ar}</span>
        </Link>
      )}
    </Card>
  );
}

/** Deterministic shuffle (no Math.random, so server and client agree and tests are stable). Never returns the original order. */
export function shuffled<T>(xs: T[], seed: string): T[] {
  let h = 2166136261;
  for (const c of seed) h = Math.imul(h ^ c.charCodeAt(0), 16777619) >>> 0;
  const rnd = () => { h = (Math.imul(h, 1664525) + 1013904223) >>> 0; return h / 4294967296; };
  const a = [...xs];
  for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [a[i], a[j]] = [a[j]!, a[i]!]; }
  if (a.length > 1 && a.every((x, i) => x === xs[i])) a.push(a.shift()!);
  return a;
}

/** Accepts Arabic-Indic digits and the Arabic decimal/thousands separators. */
export function parseNum(s: string): number | null {
  const t = s.trim().replace(/[٠-٩]/g, (d) => String("٠١٢٣٤٥٦٧٨٩".indexOf(d))).replace(/[۰-۹]/g, (d) => String("۰۱۲۳۴۵۶۷۸۹".indexOf(d))).replace(/[٫,]/g, ".").replace(/[٬\s]/g, "").replace(/−/g, "-");
  if (!/^-?\d+(\.\d+)?$/.test(t)) return null;
  return Number(t);
}
