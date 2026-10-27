"use client";
import type { Resp, View } from "./usePlay";

export function BriefTab({ view, busy, send, last, goto }: { view: View; busy: boolean; send: (r: Record<string, unknown>) => Promise<Resp | null>; last: Resp["extra"] | null; goto: (t: string, charId?: string) => void }) {
  const first = view.evidence.length === 0 && view.stats.actions_taken <= 1;
  const groups: [string, string][] = [["examine", "اطّلع على"], ["search_location", "ابحث في"], ["interview", "قابل"], ["request_lab_test", "اطلب فحصاً"]];
  return (
    <div className="stack">
      {first && <div className="cold-open" aria-label="افتتاحية">{view.cold_open_ar.map((l, i) => <p key={i}>{l}</p>)}</div>}
      <section className="card stack"><p className="kicker">الدور</p><p style={{ margin: 0 }}>{view.premise.player_role_ar}</p><p className="kicker">المكان والزمان</p><p style={{ margin: 0 }}>{view.premise.setting_ar}</p></section>
      {view.stage_hook_ar && <p className="dim" style={{ fontFamily: "var(--f-display)", fontSize: "1.2rem" }}>{view.stage_hook_ar}</p>}
      <section className="stack"><h2>ما نعرفه حتى الآن</h2>
        <ul>{view.facts.map((f) => <li key={f.id}>{f.statement_ar}</li>)}</ul>
        <p className="small dim">هذه الوقائع المسلَّم بها في بداية الملف. ما عداها عليك إثباته.</p></section>
      <section className="stack"><h2>ماذا تفعل الآن؟</h2>
        {view.actions.length === 0 && <p className="dim">لا إجراءات متاحة الآن.</p>}
        {groups.map(([type, title]) => { const acts = view.actions.filter((a) => a.type === type); return acts.length ? (
          <div key={type} className="stack"><h3 className="small dim" style={{ margin: 0, fontFamily: "var(--f-ui)" }}>{title}</h3>
            {acts.map((a) => <button key={a.id} className="btn" style={{ justifyContent: "flex-start", textAlign: "start" }} disabled={busy} onClick={async () => { const r = await send({ op: "act", action_id: a.id }); if (a.type === "interview") goto("people", a.target_id); void r; }}>{a.label_ar}</button>)}
          </div>) : null; })}
      </section>
      {last?.granted_evidence?.length ? <p role="status" className="ok">أُضيف {last.granted_evidence.length} دليل إلى خزانتك. <button className="btn ghost sm" onClick={() => goto("evidence")}>افتح الخزانة</button></p> : null}
    </div>
  );
}
