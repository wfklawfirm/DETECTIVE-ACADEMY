"use client";
import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Field } from "@/components/ui/form";
import { Callout } from "@/components/ui/feedback";
import { api, ApiError } from "@/lib/client";

export default function ForgotPassword() {
  const [email, setEmail]   = useState("");
  const [busy, setBusy]     = useState(false);
  const [done, setDone]     = useState(false);
  const [devToken, setDevToken] = useState<string | null>(null);
  const [err, setErr]       = useState<string | null>(null);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true); setErr(null);
    try {
      const res = await api<{ ok: boolean; dev_token?: string }>("/api/auth/forgot", { email });
      setDone(true);
      if (res.dev_token) setDevToken(res.dev_token);
    } catch (x) {
      setErr(x instanceof ApiError ? x.message : "تعذّر الاتصال");
    } finally {
      setBusy(false);
    }
  };

  return (
    <>
      <div className="ref-hero">
        <p className="ref-hero-kicker">الحساب</p>
        <h1 className="ref-hero-title">استرجاع كلمة المرور</h1>
        <p className="ref-hero-hook">أدخل بريدك الإلكتروني وسنرسل لك رابط الاسترجاع.</p>
      </div>

      {done ? (
        <div className="stack">
          <Callout tone="positive">
            إذا كان البريد الإلكتروني مسجلاً، ستصلك رسالة استرجاع قريباً.
          </Callout>
          {devToken && (
            <Callout tone="info">
              <strong>بيئة التطوير:</strong>{" "}
              <Link href={`/reset?token=${devToken}`} className="link">
                انقر هنا لإعادة تعيين كلمة المرور
              </Link>
            </Callout>
          )}
          <Link href="/account" className="link dim-2">
            العودة إلى الدخول
          </Link>
        </div>
      ) : (
        <form className="account-form" onSubmit={submit}>
          <Field label="البريد الإلكتروني">
            {(p) => (
              <input
                {...p}
                className="input"
                type="email"
                autoComplete="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            )}
          </Field>
          {err && <Callout tone="negative">{err}</Callout>}
          <div className="account-form-actions">
            <Button type="submit" variant="primary" size="lg" block loading={busy}>
              إرسال رابط الاسترجاع
            </Button>
            <Link href="/account" className="link dim-2 text-center">
              تذكّرت كلمة المرور؟ سجّل الدخول
            </Link>
          </div>
        </form>
      )}
    </>
  );
}
