"use client";
import { useCallback, useEffect, useState } from "react";
import { useMe } from "@/components/Shell";
import { Badge } from "@/components/ui/badge";
import { Button, LinkButton } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Callout, EmptyState, LoadingRegion } from "@/components/ui/feedback";
import { Field } from "@/components/ui/form";
import { StudioIcon } from "@/components/ui/icons";
import { api, ApiError } from "@/lib/client";

interface Ver { case_id: string; version: string; status: string; qa_ok: boolean | null; gates: Record<string, string>; all_approved: boolean; created_by: string | null }
interface Ticket { code: string; case_id: string; justification: string; created_at: string }
const ROLE_AR: Record<string, string> = { narrative_editor: "المحرر السردي", scientific_reviewer: "المراجع العلمي", learning_designer: "مصمم التعلّم", age_appropriateness: "ملاءمة العمر", cultural_reviewer: "المراجع الثقافي", legal_rights: "الحقوق والقانون", safety: "السلامة" };

export default function Studio() {
  const { me } = useMe();
  const [vers, setVers] = useState<Ver[]>([]);
  const [tix, setTix] = useState<Ticket[]>([]);
  const [msg, setMsg] = useState<string | null>(null);
  const [loaded, setLoaded] = useState(false);
  const [fb, setFb] = useState<Record<string, { level: string; text: string }>>({});
  const load = useCallback(async () => {
    try { setVers((await api<{ versions: Ver[] }>("/api/studio/versions")).versions); } catch (e) { setMsg(e instanceof ApiError ? e.message : "خطأ"); }
    try { setTix((await api<{ tickets: Ticket[] }>("/api/studio/tickets")).tickets); } catch { /* editors cannot read tickets */ }
    setLoaded(true);
  }, []);
  useEffect(() => { if (me?.user) void load(); }, [me, load]);
  const act = async (fn: () => Promise<unknown>) => { setMsg(null); try { await fn(); await load(); } catch (e) { setMsg(e instanceof ApiError ? e.message : "خطأ"); } };
  if (!me?.user || !["editor", "reviewer", "admin"].includes(me.user.role)) return <><div className="ref-hero"><p className="ref-hero-kicker">استوديو</p><h1 className="ref-hero-title">الاستوديو</h1></div><EmptyState icon={<StudioIcon size={28} />} title="للمحررين والمراجعين فقط" action={<LinkButton variant="primary" href="/account?next=/studio">سجّل الدخول</LinkButton>} /></>;
  const role = me.user.role;
  const canReview = role === "reviewer" || role === "admin";
  return (
    <>
      <div className="ref-hero">
        <p className="ref-hero-kicker">استوديو المحتوى</p>
        <h1 className="ref-hero-title">مراجعة القضايا</h1>
        <p className="ref-hero-hook">لا تُنشر قضية إلا بعد موافقة سبع بوابات على نسخة المحتوى، وموافقة المراجع لا تكون من كاتب النسخة نفسه.</p>
      </div>
      {role === "admin" && <div className="row"><LinkButton href="/studio/library">المكتبة البحثية (للمدير)</LinkButton></div>}
      {msg && <Callout tone="negative" role="alert">{msg}</Callout>}
      {!loaded && <LoadingRegion cards={2} />}
      <div className="grid-2">
      {vers.map((v) => (
        <Card as="section" key={v.case_id + v.version}>
          <div className="row row-between"><h2 className="card-title mono">{v.case_id}@{v.version}</h2><Badge tone={v.status === "published" ? "positive" : "warning"}>{v.status}</Badge></div>
          <p className="small">فحص الجودة الآلي: {v.qa_ok === null ? "—" : v.qa_ok ? <span className="ok">ناجح</span> : <span className="err">فاشل</span>}</p>
          <ul className="list list-flush">{Object.entries(v.gates).map(([r, st]) => (
            <li key={r} className="board-row">
              <div className="row row-between"><span>{ROLE_AR[r] ?? r}</span><Badge tone={st === "approved" ? "positive" : st === "changes_requested" ? "warning" : "neutral"}>{st === "approved" ? "معتمد" : st === "changes_requested" ? "تعديلات مطلوبة" : "قيد الانتظار"}</Badge></div>
              {canReview && ["draft", "in_review", "approved"].includes(v.status) && <div className="row"><Button size="sm" variant="secondary" onClick={() => act(() => api("/api/studio/review", { case_id: v.case_id, version: v.version, role: r, status: "approved" }))}>اعتمد</Button><Button size="sm" variant="ghost" onClick={() => act(() => api("/api/studio/review", { case_id: v.case_id, version: v.version, role: r, status: "changes_requested", notes: "يحتاج تعديلاً" }))}>تعديلات</Button></div>}
            </li>))}</ul>
          {role === "admin" && v.all_approved && v.status !== "published" && <Button variant="primary" onClick={() => act(() => api("/api/studio/publish", { case_id: v.case_id, version: v.version }))}>انشر</Button>}
        </Card>
      ))}
      </div>
      {canReview && (
        <section className="stack"><h2 className="text-section-title">طلبات مراجعة الحجج ({tix.length})</h2>
          <div className="grid-2">
          {tix.map((t) => { const f = fb[t.code] ?? { level: "2", text: "" }; return (
            <Card key={t.code}><span className="mono">{t.code} · {t.case_id}</span><p>{t.justification}</p>
              <Field label="المستوى">{(p) => <select {...p} value={f.level} onChange={(e) => setFb({ ...fb, [t.code]: { ...f, level: e.target.value } })}>{[0, 1, 2, 3, 4].map((n) => <option key={n}>{n}</option>)}</select>}</Field>
              <Field label="الملاحظات">{(p) => <input {...p} className="input" placeholder="ملاحظات للمتعلّم (لا درجات أدبية)" value={f.text} onChange={(e) => setFb({ ...fb, [t.code]: { ...f, text: e.target.value } })} />}</Field>
              <Button variant="secondary" disabled={f.text.length < 3} onClick={() => act(() => api("/api/studio/tickets", { code: t.code, level: Number(f.level), feedback: f.text }))}>أرسل</Button></Card>); })}
          </div>
        </section>
      )}
    </>
  );
}
