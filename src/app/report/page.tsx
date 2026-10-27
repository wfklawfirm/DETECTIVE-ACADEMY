"use client";
import { useState } from "react";
import { api, ApiError } from "@/lib/client";

export default function Report() {
  const [kind, setKind] = useState("error"); const [body, setBody] = useState(""); const [done, setDone] = useState(false); const [err, setErr] = useState<string | null>(null);
  const caseId = typeof window !== "undefined" ? new URLSearchParams(location.search).get("case") ?? undefined : undefined;
  if (done) return <div className="wrap-narrow stack"><h1>شكراً</h1><p role="status">وصل بلاغك إلى فريق المراجعة.</p></div>;
  return (
    <form className="wrap-narrow stack" onSubmit={async (e) => { e.preventDefault(); setErr(null); try { await api("/api/report", { kind, body, case_id: caseId }); setDone(true); } catch (x) { setErr(x instanceof ApiError ? x.message : "فشل الإرسال"); } }}>
      <h1>أبلِغ عن مشكلة</h1>
      <label htmlFor="k">نوع البلاغ</label>
      <select id="k" value={kind} onChange={(e) => setKind(e.target.value)}><option value="error">خطأ علمي أو في القضية</option><option value="safety">محتوى غير مناسب أو مقلق</option><option value="rights">حقوق ملكية أو تشابه مع عمل آخر</option><option value="other">أخرى</option></select>
      <label htmlFor="b">التفاصيل</label><textarea id="b" required minLength={5} maxLength={2000} value={body} onChange={(e) => setBody(e.target.value)} />
      <p className="small dim">لا تكتب بيانات شخصية. إن كنت في ضائقة نفسية فتواصل مع من تثق به أو مع خدمات الطوارئ المحلية.</p>
      {err && <p role="alert" className="err">{err}</p>}
      <button className="btn primary">أرسل</button>
    </form>
  );
}
