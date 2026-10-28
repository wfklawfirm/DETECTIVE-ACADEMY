"use client";
import type { ReactNode } from "react";
import type { Lab } from "@/engine/labs";
import { Button } from "../ui/button";
import { Card } from "../ui/card";

/** Closing card shared by every lab kind: the score line, the transfer question, the explicit limit ("what this cannot prove") and a retry. */
export function LabEnd({ lab, summary, onRetry }: { lab: Lab; summary: ReactNode; onRetry: () => void }) {
  return (
    <Card as="section" aria-live="polite" aria-label="خلاصة المختبر">
      <p>{summary} الغرض هنا فهم الفكرة، والنتيجة لا تُحفظ ولا تدخل في ملفك.</p>
      <p><b>سؤال للتفكير: </b>{lab.transfer_ar}</p>
      <div className="lab-limit"><b>ما لا يثبته هذا المختبر: </b>{lab.boundary_ar}</div>
      {lab.illustrative_ar && <p className="small dim">{lab.illustrative_ar}</p>}
      <Button variant="secondary" onClick={onRetry}>أعد المحاولة</Button>
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
