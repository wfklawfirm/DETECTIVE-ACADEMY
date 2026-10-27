"use client";
import { use, useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Callout, ErrorState, LoadingRegion } from "@/components/ui/feedback";
import { Badge } from "@/components/ui/badge";
import { api, ApiError } from "@/lib/client";

export default function Review({ params }: { params: Promise<{ code: string }> }) {
  const { code } = use(params);
  const [t, setT] = useState<{ status: string; level: number | null; feedback_ar: string | null } | null>(null);
  const [err, setErr] = useState<string | null>(null);
  useEffect(() => { api<{ ticket: NonNullable<typeof t> }>(`/api/review/${code}`).then((r) => setT(r.ticket)).catch((e) => setErr(e instanceof ApiError ? e.message : "خطأ")); }, [code]);
  return (
    <>
      <header className="page-head"><h1 className="text-page-title">طلب مراجعة <span className="mono">{code}</span></h1></header>
      {err ? <ErrorState title="تعذّر فتح الطلب" body={err} /> : !t ? <LoadingRegion cards={1} /> : t.status === "pending" ? <Callout tone="warning" title="قيد الانتظار">ما زال طلبك بانتظار مراجع بشري. ارجع لاحقاً بالرمز نفسه.</Callout> : (
        <Card><p>المستوى المقترح: <Badge tone="info">{t.level} من ٤</Badge></p><p>{t.feedback_ar}</p></Card>
      )}
    </>
  );
}
