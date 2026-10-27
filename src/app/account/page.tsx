"use client";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { useMe } from "@/components/Shell";
import { Button } from "@/components/ui/button";
import { Card, CardTitle, PageHead } from "@/components/ui/card";
import { Callout } from "@/components/ui/feedback";
import { ChoiceGroup, Field, Toggle } from "@/components/ui/form";
import { useToast } from "@/components/ui/toast";
import { api, ApiError, setGentle } from "@/lib/client";

export default function Account() {
  const { me, refresh } = useMe();
  const router = useRouter();
  const toast = useToast();
  const [mode, setMode] = useState<"login" | "register">("login");
  const [f, setF] = useState({ email: "", password: "", display_name: "", adult: false });
  const [err, setErr] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [del, setDel] = useState("");
  const next = typeof window !== "undefined" ? new URLSearchParams(location.search).get("next") : null;
  const safeNext = next && next.startsWith("/") && !next.startsWith("//") ? next : "/home";
  const submit = async (e: React.FormEvent) => {
    e.preventDefault(); setBusy(true); setErr(null);
    try {
      if (mode === "register") await api("/api/auth/register", f); else await api("/api/auth/login", { email: f.email, password: f.password });
      await refresh(); router.push(safeNext);
    } catch (x) { setErr(x instanceof ApiError ? x.message : "تعذّر الاتصال"); } finally { setBusy(false); }
  };
  if (me?.user) {
    return (
      <>
        <PageHead title="حسابي" lead={`مرحباً ${me.user.display_name ?? ""}. تقدّمك محفوظ في حسابك.`} />
        <Card>
          <Toggle label="وضع هادئ" hint="تلميحات الدخول أقصر وأقل تشويقاً." checked={me.user.gentle_hooks} onChange={async (v) => { await api("/api/auth/settings", { gentle_hooks: v }); setGentle(v); await refresh(); toast(v ? "فُعّل الوضع الهادئ" : "أُلغي الوضع الهادئ"); }} />
        </Card>
        <Button variant="secondary" block onClick={async () => { await api("/api/auth/logout", {}); await refresh(); router.push("/"); }}>تسجيل الخروج</Button>
        <hr className="divider" />
        <Card as="section">
          <CardTitle>حذف الحساب</CardTitle>
          <p className="small dim">يحذف حسابك وتقدّمك نهائياً. للتأكيد أدخل كلمة المرور.</p>
          <Field label="كلمة المرور" error={err}>{(p) => <input {...p} className="input" type="password" autoComplete="current-password" value={del} onChange={(e) => setDel(e.target.value)} />}</Field>
          <Button variant="destructive" disabled={!del} onClick={async () => { try { await api("/api/auth/delete", { password: del, confirm: true }); await refresh(); router.push("/"); } catch (x) { setErr(x instanceof ApiError ? x.message : "فشل"); } }}>احذف حسابي نهائياً</Button>
        </Card>
      </>
    );
  }
  return (
    <form className="stack" onSubmit={submit}>
      <PageHead title={mode === "login" ? "تسجيل الدخول" : "إنشاء حساب"} lead="الحساب اختياري. بدونه يُحفظ تقدّمك على هذا الجهاز فقط. الحسابات للبالغين (١٨+) حالياً." />
      <Field label="البريد الإلكتروني">{(p) => <input {...p} className="input" type="email" autoComplete="email" required value={f.email} onChange={(e) => setF({ ...f, email: e.target.value })} />}</Field>
      {mode === "register" && <Field label="الاسم الظاهر (اختياري)">{(p) => <input {...p} className="input" maxLength={40} value={f.display_name} onChange={(e) => setF({ ...f, display_name: e.target.value })} />}</Field>}
      <Field label={`كلمة المرور${mode === "register" ? " (١٠ أحرف على الأقل)" : ""}`}>{(p) => <input {...p} className="input" type="password" autoComplete={mode === "login" ? "current-password" : "new-password"} required minLength={mode === "register" ? 10 : 1} value={f.password} onChange={(e) => setF({ ...f, password: e.target.value })} />}</Field>
      {mode === "register" && <ChoiceGroup multiple label="تأكيد العمر" name="adult" value={f.adult ? ["adult"] : []} onChange={() => setF({ ...f, adult: !f.adult })} options={[{ value: "adult", label: "أؤكد أن عمري ١٨ سنة أو أكثر." }]} />}
      {err && <Callout tone="negative" role="alert">{err}</Callout>}
      <Button type="submit" variant="primary" size="lg" block loading={busy}>{mode === "login" ? "دخول" : "إنشاء الحساب"}</Button>
      <Button variant="ghost" block onClick={() => { setMode(mode === "login" ? "register" : "login"); setErr(null); }}>{mode === "login" ? "ليس لدي حساب" : "لدي حساب"}</Button>
    </form>
  );
}
