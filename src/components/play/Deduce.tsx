"use client";
import { useState } from "react";
import { Button } from "../ui/button";
import { Callout } from "../ui/feedback";
import { ChoiceGroup, Field } from "../ui/form";
import { BackIcon } from "../ui/icons";
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
        <h2 className="text-section-title">الاستنتاج النهائي</h2>
        <p>حين تشعر أن لديك ما يكفي، ستختار استنتاجك، وتذكر الأدلة التي تستند إليها، وما لا تستطيع أدلتك قوله، وما الذي قد يغيّر رأيك. لا يمكن التراجع بعد التقديم.</p>
        <p className="dim small">لديك الآن {view.evidence.length} دليلاً{view.locked_evidence_count > 0 ? ` و${view.locked_evidence_count} لم يُكشف` : ""}. لا بأس أن ترتاب في استنتاجك؛ قيّم ثقتك بصدق.</p>
        <Button variant="primary" size="lg" block disabled={busy} onClick={() => send({ op: "deduce", open: true })}>ابدأ الاستنتاج النهائي</Button>
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
    <form className="stack-lg" onSubmit={(e) => { e.preventDefault(); void submit(); }}>
      <div className="row row-between"><h2 className="text-section-title">الاستنتاج النهائي</h2><Button type="button" variant="ghost" size="sm" disabled={busy} onClick={() => send({ op: "deduce", open: false })}><BackIcon size={20} />عودة للتحقيق</Button></div>
      <fieldset className="card"><legend id="lg-concl">١. ما استنتاجك؟</legend>
        <ChoiceGroup labelledBy="lg-concl" name="concl" value={concl} onChange={setConcl} options={view.hypotheses.map((h) => ({ value: h.id, label: h.statement_ar }))} />
      </fieldset>
      <div className="card"><Field label={<>٢. ما درجة ترجيحك لهذا الاستنتاج؟ <span className="mono">{conf}</span>٪</>} hint="ثقة عالية بلا أدلة كافية تُحاسَب كما تُحاسَب الثقة المنخفضة رغم أدلة قوية.">{(p) => <input {...p} type="range" min={0} max={100} step={5} value={conf} onChange={(e) => setConf(Number(e.target.value))} />}</Field></div>
      <fieldset className="card"><legend>٣. أي الأدلة تستند إليها؟ وكيف؟</legend>
        {view.evidence.map((e) => (
          <div key={e.id} className="board-row"><span>{e.title_ar}</span>
            <select aria-label={`علاقة ${e.title_ar} باستنتاجك`} value={cited[e.id] ?? ""} onChange={(ev) => setCited((s) => ({ ...s, [e.id]: ev.target.value as "supports" })) }>
              <option value="">لا أستند إليه</option><option value="supports">يدعم استنتاجي</option><option value="limits">يحدّ منه</option><option value="rules_out">يستبعد بديلاً</option>
            </select></div>
        ))}
      </fieldset>
      <fieldset className="card"><legend id="lg-lim">٤. ما الذي لا تستطيع أدلتك إثباته؟</legend>
        <ChoiceGroup multiple labelledBy="lg-lim" name="lim" value={lim} onChange={(id) => tog(lim, setLim, id)} options={view.limit_menu.map((m) => ({ value: m.id, label: m.label_ar }))} />
      </fieldset>
      <fieldset className="card"><legend id="lg-mind">٥. ما الذي قد يغيّر رأيك؟</legend>
        <ChoiceGroup multiple labelledBy="lg-mind" name="mind" value={mind} onChange={(id) => tog(mind, setMind, id)} options={view.mind_change_menu.map((m) => ({ value: m.id, label: m.label_ar }))} />
      </fieldset>
      <div className="card">
        <Field label="٦. حجتك بكلماتك (اختياري)" hint="لا يُقيَّم الإسهاب ولا الأسلوب. يقرؤها مراجع بشري إن طلبت ذلك فقط؛ ولا تُحتسب آلياً.">{(p) => <textarea {...p} className="textarea" value={just} maxLength={4000} onChange={(e) => setJust(e.target.value)} />}</Field>
        <ChoiceGroup multiple label="مشاركة الحجة" name="share" value={share ? ["share"] : []} onChange={() => setShare(!share)} options={[{ value: "share", label: "أرسل حجتي لمراجعة بشرية (تحصل على رمز لمتابعة الملاحظات، دون الكشف عن هويتك)" }]} />
      </div>
      {err && <Callout tone="negative" role="alert">{err}</Callout>}
      <Button type="submit" variant="primary" size="lg" block disabled={busy}>قدّم الاستنتاج</Button>
    </form>
  );
}
