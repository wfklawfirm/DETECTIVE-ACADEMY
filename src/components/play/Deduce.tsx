"use client";
import { useState } from "react";
import type { View } from "./usePlay";

export function DeduceTab({ view, busy, send }: { view: View; busy: boolean; send: (r: Record<string, unknown>) => Promise<unknown> }) {
  const [concl, setConcl] = useState("");
  const [conf, setConf] = useState(60);
  const [cited, setCited] = useState<Record<string, "supports" | "limits" | "rules_out" | "">>({});
  const [lim, setLim] = useState<string[]>([]);
  const [mind, setMind] = useState<string[]>([]);
  const [just, setJust] = useState("");
  const [share, setShare] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const open = view.sub === "deducing";
  const tog = (arr: string[], set: (v: string[]) => void, id: string) => set(arr.includes(id) ? arr.filter((x) => x !== id) : [...arr, id]);
  if (!open) {
    return (
      <div className="stack">
        <h2>الاستنتاج النهائي</h2>
        <p>حين تشعر أن لديك ما يكفي، ستختار استنتاجك، وتذكر الأدلة التي تستند إليها، وما لا تستطيع أدلتك قوله، وما الذي قد يغيّر رأيك. لا يمكن التراجع بعد التقديم.</p>
        <p className="dim small">لديك الآن {view.evidence.length} دليلاً{view.locked_evidence_count > 0 ? ` و${view.locked_evidence_count} لم يُكشف` : ""}. لا بأس أن ترتاب في استنتاجك؛ قيّم ثقتك بصدق.</p>
        <button className="btn primary" disabled={busy} onClick={() => send({ op: "deduce", open: true })}>ابدأ الاستنتاج النهائي</button>
      </div>
    );
  }
  const submit = async () => {
    const list = Object.entries(cited).filter(([, r]) => r).map(([evidence_id, role]) => ({ evidence_id, role }));
    if (!concl) return setErr("اختر استنتاجاً.");
    if (list.length < 1) return setErr("اذكر دليلاً واحداً على الأقل وحدّد علاقته باستنتاجك.");
    setErr(null);
    await send({ op: "submit", conclusion_hypothesis_id: concl, confidence: conf, cited: list, limit_choice_ids: lim, would_change_mind_ids: mind, justification: just, share_for_review: share });
  };
  return (
    <form className="stack" onSubmit={(e) => { e.preventDefault(); void submit(); }}>
      <div className="row" style={{ justifyContent: "space-between" }}><h2 style={{ margin: 0 }}>الاستنتاج النهائي</h2><button type="button" className="btn ghost sm" disabled={busy} onClick={() => send({ op: "deduce", open: false })}>← عودة للتحقيق</button></div>
      <fieldset className="card" style={{ border: "1px solid var(--line)" }}><legend>١. ما استنتاجك؟</legend>
        {view.hypotheses.map((h) => <label key={h.id} style={{ display: "flex", gap: 12, alignItems: "flex-start", fontWeight: 400 }}><input type="radio" name="concl" checked={concl === h.id} onChange={() => setConcl(h.id)} /><span>{h.statement_ar}</span></label>)}
      </fieldset>
      <div className="card"><label htmlFor="fconf">٢. ما درجة ترجيحك لهذا الاستنتاج؟ <span className="mono">{conf}</span>٪</label><input id="fconf" type="range" min={0} max={100} step={5} value={conf} onChange={(e) => setConf(Number(e.target.value))} /><p className="small dim">ثقة عالية بلا أدلة كافية تُحاسَب كما تُحاسَب الثقة المنخفضة رغم أدلة قوية.</p></div>
      <fieldset className="card" style={{ border: "1px solid var(--line)" }}><legend>٣. أي الأدلة تستند إليها؟ وكيف؟</legend>
        {view.evidence.map((e) => (
          <div key={e.id} className="board-row"><span>{e.title_ar}</span>
            <select aria-label={`علاقة ${e.title_ar} باستنتاجك`} value={cited[e.id] ?? ""} onChange={(ev) => setCited((s) => ({ ...s, [e.id]: ev.target.value as "supports" })) }>
              <option value="">لا أستند إليه</option><option value="supports">يدعم استنتاجي</option><option value="limits">يحدّ منه</option><option value="rules_out">يستبعد بديلاً</option>
            </select></div>
        ))}
      </fieldset>
      <fieldset className="card" style={{ border: "1px solid var(--line)" }}><legend>٤. ما الذي لا تستطيع أدلتك إثباته؟</legend>
        {view.limit_menu.map((m) => <label key={m.id} style={{ display: "flex", gap: 12, fontWeight: 400 }}><input type="checkbox" checked={lim.includes(m.id)} onChange={() => tog(lim, setLim, m.id)} /><span>{m.label_ar}</span></label>)}
      </fieldset>
      <fieldset className="card" style={{ border: "1px solid var(--line)" }}><legend>٥. ما الذي قد يغيّر رأيك؟</legend>
        {view.mind_change_menu.map((m) => <label key={m.id} style={{ display: "flex", gap: 12, fontWeight: 400 }}><input type="checkbox" checked={mind.includes(m.id)} onChange={() => tog(mind, setMind, m.id)} /><span>{m.label_ar}</span></label>)}
      </fieldset>
      <div className="card"><label htmlFor="just">٦. حجتك بكلماتك (اختياري)</label><textarea id="just" value={just} maxLength={4000} onChange={(e) => setJust(e.target.value)} />
        <p className="small dim">لا يُقيَّم الإسهاب ولا الأسلوب. يقرؤها مراجع بشري إن طلبت ذلك فقط؛ ولا تُحتسب آلياً.</p>
        <label style={{ display: "flex", gap: 12, fontWeight: 400 }}><input type="checkbox" checked={share} onChange={(e) => setShare(e.target.checked)} /><span>أرسل حجتي لمراجعة بشرية (تحصل على رمز لمتابعة الملاحظات، دون الكشف عن هويتك)</span></label></div>
      {err && <p role="alert" className="err">{err}</p>}
      <button className="btn primary" disabled={busy}>قدّم الاستنتاج</button>
    </form>
  );
}
