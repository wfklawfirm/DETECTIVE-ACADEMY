"use client";
import { useCallback, useEffect, useState } from "react";
import { useMe } from "@/components/Shell";
import { api, ApiError } from "@/lib/client";

interface Ver { case_id: string; version: string; status: string; qa_ok: boolean | null; gates: Record<string, string>; all_approved: boolean; created_by: string | null }
interface Ticket { code: string; case_id: string; justification: string; created_at: string }
const ROLE_AR: Record<string, string> = { narrative_editor: "المحرر السردي", scientific_reviewer: "المراجع العلمي", learning_designer: "مصمم التعلّم", age_appropriateness: "ملاءمة العمر", cultural_reviewer: "المراجع الثقافي", legal_rights: "الحقوق والقانون", safety: "السلامة" };

export default function Studio() {
  const { me } = useMe();
  const [vers, setVers] = useState<Ver[]>([]);
  const [tix, setTix] = useState<Ticket[]>([]);
  const [msg, setMsg] = useState<string | null>(null);
  const [fb, setFb] = useState<Record<string, { level: string; text: string }>>({});
  const load = useCallback(async () => {
    try { setVers((await api<{ versions: Ver[] }>("/api/studio/versions")).versions); } catch (e) { setMsg(e instanceof ApiError ? e.message : "خطأ"); }
    try { setTix((await api<{ tickets: Ticket[] }>("/api/studio/tickets")).tickets); } catch { /* editors cannot read tickets */ }
  }, []);
  useEffect(() => { if (me?.user) void load(); }, [me, load]);
  const act = async (fn: () => Promise<unknown>) => { setMsg(null); try { await fn(); await load(); } catch (e) { setMsg(e instanceof ApiError ? e.message : "خطأ"); } };
  if (!me?.user || !["editor", "reviewer", "admin"].includes(me.user.role)) return <div className="wrap"><h1>الاستوديو</h1><p>للمحررين والمراجعين فقط. <a href="/account?next=/studio">سجّل الدخول</a>.</p></div>;
  const role = me.user.role;
  return (
    <div className="wrap stack">
      <h1>استوديو المحتوى</h1>
      <p className="dim small">لا تُنشر قضية إلا بعد موافقة سبع بوابات على نسخة المحتوى الحالية (بصمتها مربوطة)، وموافقة المراجع لا تكون من كاتب النسخة نفسه.</p>
      {msg && <p role="alert" className="err">{msg}</p>}
      {vers.map((v) => (
        <section key={v.case_id + v.version} className="card stack">
          <div className="row" style={{ justifyContent: "space-between" }}><h2 style={{ margin: 0 }} className="mono">{v.case_id}@{v.version}</h2><span className={`chip ${v.status === "published" ? "green" : "amber"}`}>{v.status}</span></div>
          <p className="small">فحص الجودة الآلي: {v.qa_ok === null ? "—" : v.qa_ok ? <span className="ok">ناجح</span> : <span className="err">فاشل</span>}</p>
          <table className="simple"><tbody>{Object.entries(v.gates).map(([r, s]) => (
            <tr key={r}><td>{ROLE_AR[r] ?? r}</td><td>{s === "approved" ? "✓ معتمد" : s === "changes_requested" ? "تعديلات مطلوبة" : "قيد الانتظار"}</td>
              <td>{(role === "reviewer" || role === "admin") && ["draft", "in_review", "approved"].includes(v.status) && <span className="row"><button className="btn sm" onClick={() => act(() => api("/api/studio/review", { case_id: v.case_id, version: v.version, role: r, status: "approved" }))}>اعتمد</button><button className="btn sm ghost" onClick={() => act(() => api("/api/studio/review", { case_id: v.case_id, version: v.version, role: r, status: "changes_requested", notes: "يحتاج تعديلاً" }))}>تعديلات</button></span>}</td></tr>))}</tbody></table>
          {role === "admin" && v.all_approved && v.status !== "published" && <button className="btn primary" onClick={() => act(() => api("/api/studio/publish", { case_id: v.case_id, version: v.version }))}>انشر</button>}
        </section>
      ))}
      {(role === "reviewer" || role === "admin") && (
        <section className="stack"><h2>طلبات مراجعة الحجج ({tix.length})</h2>
          {tix.map((t) => { const f = fb[t.code] ?? { level: "2", text: "" }; return (
            <div key={t.code} className="card stack"><span className="mono">{t.code} · {t.case_id}</span><p>{t.justification}</p>
              <div className="field-row"><select aria-label="المستوى" value={f.level} onChange={(e) => setFb({ ...fb, [t.code]: { ...f, level: e.target.value } })} style={{ inlineSize: 120 }}>{[0, 1, 2, 3, 4].map((n) => <option key={n}>{n}</option>)}</select>
                <input aria-label="الملاحظات" placeholder="ملاحظات للمتعلّم (لا درجات أدبية)" value={f.text} onChange={(e) => setFb({ ...fb, [t.code]: { ...f, text: e.target.value } })} style={{ flex: 1 }} />
                <button className="btn sm" disabled={f.text.length < 3} onClick={() => act(() => api("/api/studio/tickets", { code: t.code, level: Number(f.level), feedback: f.text }))}>أرسل</button></div></div>); })}
        </section>
      )}
    </div>
  );
}
