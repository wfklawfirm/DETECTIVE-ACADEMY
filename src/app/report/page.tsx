"use client";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { PageHead } from "@/components/ui/card";
import { Callout } from "@/components/ui/feedback";
import { Field } from "@/components/ui/form";
import { api, ApiError } from "@/lib/client";

export default function Report() {
  const [kind, setKind] = useState("error"); const [body, setBody] = useState(""); const [done, setDone] = useState(false); const [err, setErr] = useState<string | null>(null); const [busy, setBusy] = useState(false);
  const caseId = typeof window !== "undefined" ? new URLSearchParams(location.search).get("case") ?? undefined : undefined;
  if (done) return <><PageHead title="شكراً" /><Callout tone="positive" role="status">وصل بلاغك إلى فريق المراجعة.</Callout></>;
  return (
    <form className="stack" onSubmit={async (e) => { e.preventDefault(); setErr(null); setBusy(true); try { await api("/api/report", { kind, body, case_id: caseId }); setDone(true); } catch (x) { setErr(x instanceof ApiError ? x.message : "فشل الإرسال"); } finally { setBusy(false); } }}>
      <PageHead title="أبلِغ عن مشكلة" />
      <Field label="نوع البلاغ">{(p) => <select {...p} value={kind} onChange={(e) => setKind(e.target.value)}><option value="error">خطأ علمي أو في القضية</option><option value="safety">محتوى غير مناسب أو مقلق</option><option value="rights">حقوق ملكية أو تشابه مع عمل آخر</option><option value="other">أخرى</option></select>}</Field>
      <Field label="التفاصيل" hint="لا تكتب بيانات شخصية. إن كنت في ضائقة نفسية فتواصل مع من تثق به أو مع خدمات الطوارئ المحلية.">{(p) => <textarea {...p} className="textarea" required minLength={5} maxLength={2000} value={body} onChange={(e) => setBody(e.target.value)} />}</Field>
      {err && <Callout tone="negative" role="alert">{err}</Callout>}
      <Button type="submit" variant="primary" size="lg" block loading={busy}>أرسل</Button>
    </form>
  );
}
