"use client";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { useMe } from "@/components/Shell";
import { Button } from "@/components/ui/button";
import { ErrorState } from "@/components/ui/feedback";
import { ChoiceGroup, Field, Toggle } from "@/components/ui/form";
import { useToast } from "@/components/ui/toast";
import { api, ApiError, setGentle } from "@/lib/client";

export default function Account() {
  const { me, refresh } = useMe();
  const router          = useRouter();
  const toast           = useToast();
  const [mode, setMode] = useState<"login" | "register">("login");
  const [f, setF]       = useState({ email: "", password: "", display_name: "", adult: false });
  const [err, setErr]   = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [delPass, setDelPass] = useState("");

  const next     = typeof window !== "undefined" ? new URLSearchParams(location.search).get("next") : null;
  const safeNext = next && next.startsWith("/") && !next.startsWith("//") ? next : "/home";

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true); setErr(null);
    try {
      if (mode === "register") await api("/api/auth/register", f);
      else await api("/api/auth/login", { email: f.email, password: f.password });
      await refresh();
      router.push(safeNext);
    } catch (x) {
      setErr(x instanceof ApiError ? x.message : "تعذّر الاتصال");
    } finally {
      setBusy(false);
    }
  };

  /* ── Logged-in view ─────────────────────────────────────────── */
  if (me?.user) {
    return (
      <>
        {/* Hero */}
        <header className="account-hero">
          <div className="account-hero-inner">
            <div className="account-hero-text">
              <p className="account-hero-kicker">إعدادات الحساب</p>
              <h1 className="account-hero-name">{me.user.display_name ?? "محقق"}</h1>
              <p className="account-hero-email">{me.user.email ?? ""}</p>
            </div>
            <span className="account-hero-avatar" aria-hidden>🪪</span>
          </div>
        </header>

        {/* Settings card */}
        <div className="account-card">
          <p className="account-card-kicker">التفضيلات</p>
          <Toggle
            label="وضع هادئ"
            hint="تلميحات الدخول أقصر وأقل تشويقاً."
            checked={me.user.gentle_hooks}
            onChange={async (v) => {
              await api("/api/auth/settings", { gentle_hooks: v });
              setGentle(v);
              await refresh();
              toast(v ? "فُعّل الوضع الهادئ" : "أُلغي الوضع الهادئ");
            }}
          />
        </div>

        {/* Logout */}
        <Button
          variant="secondary"
          block
          onClick={async () => {
            await api("/api/auth/logout", {});
            await refresh();
            router.push("/");
          }}
        >
          تسجيل الخروج
        </Button>

        {/* Danger zone */}
        <div className="account-danger-zone">
          <p className="account-danger-kicker">منطقة الخطر</p>
          <h3 className="account-danger-title">حذف الحساب</h3>
          <p className="account-danger-body">يحذف حسابك وتقدّمك نهائياً. للتأكيد أدخل كلمة المرور.</p>
          <Field label="كلمة المرور" error={err}>
            {(p) => (
              <input
                {...p}
                className="input"
                type="password"
                autoComplete="current-password"
                value={delPass}
                onChange={(e) => setDelPass(e.target.value)}
              />
            )}
          </Field>
          <Button
            variant="destructive"
            disabled={!delPass}
            onClick={async () => {
              try {
                await api("/api/auth/delete", { password: delPass, confirm: true });
                await refresh();
                router.push("/");
              } catch (x) {
                setErr(x instanceof ApiError ? x.message : "فشل");
              }
            }}
          >
            احذف حسابي نهائياً
          </Button>
        </div>
      </>
    );
  }

  /* ── Auth form ──────────────────────────────────────────────── */
  return (
    <>
      {/* Hero */}
      <header className="account-hero">
        <div className="account-hero-inner">
          <div className="account-hero-text">
            <p className="account-hero-kicker">
              {mode === "login" ? "مرحباً بعودتك" : "انضم إلى الأكاديمية"}
            </p>
            <h1 className="account-hero-name">
              {mode === "login" ? "تسجيل الدخول" : "إنشاء حساب"}
            </h1>
            <p className="account-hero-note">
              الحساب اختياري. بدونه يُحفظ تقدّمك على هذا الجهاز فقط. الحسابات للبالغين (١٨+) حالياً.
            </p>
          </div>
          <span className="account-hero-avatar" aria-hidden>
            {mode === "login" ? "🔑" : "🪪"}
          </span>
        </div>
      </header>

      <form className="account-form" onSubmit={submit}>
        <Field label="البريد الإلكتروني">
          {(p) => (
            <input
              {...p} className="input" type="email" autoComplete="email" required
              value={f.email} onChange={(e) => setF({ ...f, email: e.target.value })}
            />
          )}
        </Field>

        {mode === "register" && (
          <Field label="الاسم الظاهر (اختياري)">
            {(p) => (
              <input
                {...p} className="input" maxLength={40}
                value={f.display_name} onChange={(e) => setF({ ...f, display_name: e.target.value })}
              />
            )}
          </Field>
        )}

        <Field label={`كلمة المرور${mode === "register" ? " (١٠ أحرف على الأقل)" : ""}`}>
          {(p) => (
            <input
              {...p} className="input" type="password"
              autoComplete={mode === "login" ? "current-password" : "new-password"}
              required minLength={mode === "register" ? 10 : 1}
              value={f.password} onChange={(e) => setF({ ...f, password: e.target.value })}
            />
          )}
        </Field>

        {mode === "register" && (
          <ChoiceGroup
            multiple label="تأكيد العمر" name="adult"
            value={f.adult ? ["adult"] : []}
            onChange={() => setF({ ...f, adult: !f.adult })}
            options={[{ value: "adult", label: "أؤكد أن عمري ١٨ سنة أو أكثر." }]}
          />
        )}

        {err && <ErrorState title={err} />}

        <div className="account-form-actions">
          <Button type="submit" variant="primary" size="lg" block loading={busy}>
            {mode === "login" ? "دخول" : "إنشاء الحساب"}
          </Button>
          <Button
            variant="ghost" block
            onClick={() => { setMode(mode === "login" ? "register" : "login"); setErr(null); }}
          >
            {mode === "login" ? "ليس لدي حساب — أنشئ حساباً" : "لدي حساب — سجّل الدخول"}
          </Button>
        </div>
      </form>
    </>
  );
}
