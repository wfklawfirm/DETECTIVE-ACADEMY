"use client";
import { Suspense, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Field } from "@/components/ui/form";
import { Callout } from "@/components/ui/feedback";
import { api, ApiError } from "@/lib/client";

function ResetForm() {
  const router = useRouter();
  const params = useSearchParams();
  const token = params.get("token") ?? "";

  const [pass, setPass]       = useState("");
  const [confirm, setConfirm] = useState("");
  const [busy, setBusy]       = useState(false);
  const [err, setErr]         = useState<string | null>(null);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (pass !== confirm) { setErr("كلمتا المرور غير متطابقتين"); return; }
    if (pass.length < 10)  { setErr("كلمة المرور يجب أن تكون 10 أحرف على الأقل"); return; }
    setBusy(true); setErr(null);
    try {
      await api("/api/auth/reset", { token, password: pass });
      router.push("/account?reset=1");
    } catch (x) {
      setErr(x instanceof ApiError ? x.message : "تعذّر الاتصال");
    } finally {
      setBusy(false);
    }
  };

  if (!token) return (
    <Callout tone="negative">
      رابط الاسترجاع غير صالح.{" "}
      <Link href="/forgot" className="link">طلب رابط جديد</Link>
    </Callout>
  );

  return (
    <form className="account-form" onSubmit={submit}>
      <Field label="كلمة المرور الجديدة">
        {(p) => (
          <input {...p} className="input" type="password" autoComplete="new-password"
            minLength={10} required value={pass} onChange={(e) => setPass(e.target.value)} />
        )}
      </Field>
      <Field label="تأكيد كلمة المرور">
        {(p) => (
          <input {...p} className="input" type="password" autoComplete="new-password"
            minLength={10} required value={confirm} onChange={(e) => setConfirm(e.target.value)} />
        )}
      </Field>
      {err && <Callout tone="negative">{err}</Callout>}
      <div className="account-form-actions">
        <Button type="submit" variant="primary" size="lg" block loading={busy}>
          تعيين كلمة المرور
        </Button>
        <Link href="/account" className="link dim-2 text-center">العودة إلى الدخول</Link>
      </div>
    </form>
  );
}

export default function ResetPassword() {
  return (
    <>
      <div className="ref-hero">
        <p className="ref-hero-kicker">الحساب</p>
        <h1 className="ref-hero-title">تعيين كلمة مرور جديدة</h1>
        <p className="ref-hero-hook">اختر كلمة مرور جديدة لا تقل عن 10 أحرف.</p>
      </div>
      <Suspense>
        <ResetForm />
      </Suspense>
    </>
  );
}
