"use client";
import { use, useEffect, useState } from "react";
import { api, ApiError } from "@/lib/client";

export default function Review({ params }: { params: Promise<{ code: string }> }) {
  const { code } = use(params);
  const [t, setT] = useState<{ status: string; level: number | null; feedback_ar: string | null } | null>(null);
  const [err, setErr] = useState<string | null>(null);
  useEffect(() => { void api<{ ticket: NonNullable<typeof t> }>(`/api/review/${code}`).then((r) => setT(r.ticket)).catch((e) => setErr(e instanceof ApiError ? e.message : "خطأ")); }, [code]);
  return (
    <div className="wrap-narrow stack"><h1>طلب مراجعة <span className="mono">{code}</span></h1>
      {err ? <p role="alert" className="err">{err}</p> : !t ? <p className="dim">جارٍ التحميل…</p> : t.status === "pending" ? <p>ما زال طلبك بانتظار مراجع بشري. ارجع لاحقاً بالرمز نفسه.</p> : <><p>المستوى المقترح: <b>{t.level}</b> من ٤</p><div className="card">{t.feedback_ar}</div></>}
    </div>
  );
}
