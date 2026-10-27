"use client";
import { useState } from "react";
import { api } from "@/lib/client";

export function AgeGate({ onDone }: { onDone: () => Promise<void> }) {
  const [msg, setMsg] = useState<string | null>(null);
  const pick = async (band: "16-17" | "18+" | "under16") => {
    const r = await api<{ allowed: boolean; message?: string }>("/api/age", { band });
    if (!r.allowed) setMsg(r.message ?? "المنصة غير متاحة لفئتك العمرية حالياً.");
    else await onDone();
  };
  return (
    <div className="age-gate" role="dialog" aria-modal="true" aria-labelledby="ag-t">
      <div className="card wrap-narrow stack">
        <h2 id="ag-t">قبل أن نبدأ</h2>
        {msg ? <p role="alert">{msg}</p> : (
          <>
            <p>أثر موجّهة لمن هم في السادسة عشرة فأكثر. اختر فئتك العمرية لنعرض لك ما يناسبك. لا نسأل عن تاريخ ميلادك ولا عن هويتك، ونحفظ الفئة فقط على جهازك.</p>
            <div className="stack">
              <button className="btn primary" onClick={() => pick("16-17")}>عمري بين 16 و17 سنة</button>
              <button className="btn primary" onClick={() => pick("18+")}>عمري 18 سنة أو أكثر</button>
              <button className="btn ghost" onClick={() => pick("under16")}>عمري أقل من 16 سنة</button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
