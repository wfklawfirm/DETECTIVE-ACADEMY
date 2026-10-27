"use client";
import type { View } from "./usePlay";

type Send = (r: Record<string, unknown>) => Promise<unknown>;
const DIRS = [["supports", "يدعم", "sup"], ["weakens", "يُضعف", "weak"], ["neutral", "لا يحسم", ""]] as const;
const STANCE_AR = { open: "مفتوحة", leading: "الأرجح الآن", ruled_out: "مستبعدة" } as const;

export function BoardTab({ view, busy, send }: { view: View; busy: boolean; send: Send }) {
  const added = view.hypotheses.filter((h) => h.entry);
  const notAdded = view.hypotheses.filter((h) => !h.entry);
  return (
    <div className="stack">
      <h2>لوحة الفرضيات</h2>
      <p className="dim small">أضف الفرضيات التي تراها معقولة، واربط بكل واحدة ما يدعمها أو يضعفها. يمكنك تغيير رأيك: كل تعديل يُسجَّل، وتغيير الرأي أمام دليل جديد علامة جودة.</p>
      {notAdded.length > 0 && (
        <div className="card stack"><h3>فرضيات يمكن إضافتها</h3>
          {notAdded.map((h) => <div key={h.id} className="row"><span style={{ flex: "1 1 240px" }}>{h.statement_ar}</span><button className="btn sm" disabled={busy} onClick={() => send({ op: "hyp_add", hypothesis_id: h.id })}>أضِف إلى اللوحة</button></div>)}
        </div>
      )}
      {added.length === 0 && <p>لوحتك فارغة. ابدأ بإضافة فرضية.</p>}
      {added.map((h) => {
        const en = h.entry!;
        return (
          <section key={h.id} className="card hyp stack" data-stance={en.stance} aria-label={h.statement_ar}>
            <div className="row" style={{ justifyContent: "space-between" }}>
              <h3 style={{ margin: 0, flex: "1 1 260px" }}>{h.statement_ar}</h3>
              <span className={`chip ${en.stance === "leading" ? "amber" : en.stance === "ruled_out" ? "rose" : ""}`}>{STANCE_AR[en.stance]}</span>
            </div>
            <div>
              <label htmlFor={`conf-${h.id}`}>درجة ترجيحك لها: <span className="mono">{en.confidence ?? "—"}</span>{en.confidence !== null && "٪"}</label>
              <input id={`conf-${h.id}`} type="range" min={0} max={100} step={5} value={en.confidence ?? 0} disabled={busy}
                onChange={(e) => { /* optimistic only on release */ void e; }}
                onMouseUp={(e) => send({ op: "hyp_conf", hypothesis_id: h.id, value: Number((e.target as HTMLInputElement).value) })}
                onTouchEnd={(e) => send({ op: "hyp_conf", hypothesis_id: h.id, value: Number((e.target as HTMLInputElement).value) })}
                onKeyUp={(e) => send({ op: "hyp_conf", hypothesis_id: h.id, value: Number((e.target as HTMLInputElement).value) })} />
              <p className="small dim">هذه «نسبة ترجيح» لما تراه أرجح بناءً على الأدلة التي بين يديك، وليست احتمالاً محسوباً.</p>
            </div>
            <div className="seg" role="group" aria-label="حالة الفرضية">
              {(["open", "leading", "ruled_out"] as const).map((s) => <button key={s} aria-pressed={en.stance === s} disabled={busy}
                onClick={() => send({ op: "hyp_stance", hypothesis_id: h.id, stance: s, evidence_ids: s === "ruled_out" ? Object.keys(en.links).filter((k) => en.links[k] === "weakens") : undefined })}>{STANCE_AR[s]}</button>)}
            </div>
            {en.stance === "ruled_out" && Object.values(en.links).every((d) => d !== "weakens") && <p className="small err">لاستبعاد فرضية اربط بها دليلاً واحداً على الأقل «يُضعفها».</p>}
            <details>
              <summary>ربط الأدلة ({Object.keys(en.links).length})</summary>
              {view.evidence.length === 0 ? <p className="dim">لا أدلة بعد.</p> : view.evidence.map((e) => (
                <div key={e.id} className="board-row">
                  <span>{e.title_ar}</span>
                  <div className="seg" role="group" aria-label={`علاقة ${e.title_ar} بالفرضية`}>
                    {DIRS.map(([d, l, cls]) => <button key={d} className={cls} aria-pressed={en.links[e.id] === d} disabled={busy} onClick={() => send({ op: "hyp_link", hypothesis_id: h.id, evidence_id: e.id, dir: d })}>{l}</button>)}
                  </div>
                </div>
              ))}
            </details>
            <p className="small dim" style={{ margin: 0 }}>سجل المراجعات: {en.revisions.length} تعديل</p>
          </section>
        );
      })}
    </div>
  );
}
