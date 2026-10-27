"use client";
import { useState } from "react";
import { api } from "@/lib/client";
import { Button } from "./ui/button";
import { Callout } from "./ui/feedback";
import { Sheet } from "./ui/sheet";

/** Modal age gate (self-declared band; not identity verification). Not dismissible: a band must be chosen. */
export function AgeGate({ onDone }: { onDone: () => Promise<void> }) {
  const [msg, setMsg] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const pick = async (band: "16-17" | "18+" | "under16") => {
    setBusy(true);
    try {
      const r = await api<{ allowed: boolean; message?: string }>("/api/age", { band });
      if (!r.allowed) setMsg(r.message ?? "المنصة غير متاحة لفئتك العمرية حالياً.");
      else await onDone();
    } catch { setMsg("تعذّر الاتصال. حاول مرة أخرى."); } finally { setBusy(false); }
  };
  return (
    <Sheet open onClose={() => {}} dismissible={false} title="قبل أن نبدأ">
      {msg ? <Callout tone="warning" role="alert">{msg}</Callout> : (
        <>
          <p>أثر موجّهة لمن هم في السادسة عشرة فأكثر. اختر فئتك العمرية لنعرض لك ما يناسبك. لا نسأل عن تاريخ ميلادك ولا عن هويتك، ونحفظ الفئة فقط على جهازك.</p>
          <div className="stack-sm">
            <Button variant="outline" block disabled={busy} onClick={() => pick("16-17")}>عمري بين 16 و17 سنة</Button>
            <Button variant="outline" block disabled={busy} onClick={() => pick("18+")}>عمري 18 سنة أو أكثر</Button>
            <Button variant="ghost" block disabled={busy} onClick={() => pick("under16")}>عمري أقل من 16 سنة</Button>
          </div>
        </>
      )}
    </Sheet>
  );
}
