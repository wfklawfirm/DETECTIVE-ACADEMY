"use client";
import { Badge } from "../ui/badge";
import { Button } from "../ui/button";
import { Card, CardTitle } from "../ui/card";
import { Callout } from "../ui/feedback";
import { SegmentedControl } from "../ui/form";
import type { View } from "./usePlay";

type Send = (r: Record<string, unknown>) => Promise<unknown>;
const DIRS = [["supports", "يدعم", "positive"], ["weakens", "يُضعف", "negative"], ["neutral", "لا يحسم", undefined]] as const;
const STANCE_AR = { open: "مفتوحة", leading: "الأرجح الآن", ruled_out: "مستبعدة" } as const;

export function BoardTab({ view, busy, send }: { view: View; busy: boolean; send: Send }) {
  const added = view.hypotheses.filter((h) => h.entry);
  const notAdded = view.hypotheses.filter((h) => !h.entry);
  return (
    <div className="stack-lg">
      <div className="stack-sm">
        <h2 className="text-section-title">لوحة الفرضيات</h2>
        <p className="dim small">أضف الفرضيات التي تراها معقولة، واربط بكل واحدة ما يدعمها أو يضعفها. يمكنك تغيير رأيك: كل تعديل يُسجَّل، وتغيير الرأي أمام دليل جديد علامة جودة.</p>
      </div>
      {notAdded.length > 0 && (
        <Card><CardTitle level={3}>فرضيات يمكن إضافتها</CardTitle>
          {notAdded.map((h) => <div key={h.id} className="board-row"><span>{h.statement_ar}</span><Button variant="secondary" size="sm" style={{ alignSelf: "flex-start" }} disabled={busy} onClick={() => send({ op: "hyp_add", hypothesis_id: h.id })}>أضِف إلى اللوحة</Button></div>)}
        </Card>
      )}
      {added.length === 0 && <Callout tone="info">لوحتك فارغة. ابدأ بإضافة فرضية.</Callout>}
      {added.map((h) => {
        const en = h.entry!;
        return (
          <Card as="section" key={h.id} className="hyp" data-stance={en.stance} aria-label={h.statement_ar}>
            <div className="row row-between" style={{ alignItems: "flex-start" }}>
              <h3 className="card-title grow">{h.statement_ar}</h3>
              <Badge tone={en.stance === "leading" ? "brand" : en.stance === "ruled_out" ? "negative" : "neutral"}>{STANCE_AR[en.stance]}</Badge>
            </div>
            <div className="field">
              <label htmlFor={`conf-${h.id}`}>درجة ترجيحك لها: <span className="mono">{en.confidence ?? "—"}</span>{en.confidence !== null && "٪"}</label>
              <input id={`conf-${h.id}`} type="range" min={0} max={100} step={5} value={en.confidence ?? 0} disabled={busy}
                onChange={(e) => { /* optimistic only on release */ void e; }}
                onMouseUp={(e) => send({ op: "hyp_conf", hypothesis_id: h.id, value: Number((e.target as HTMLInputElement).value) })}
                onTouchEnd={(e) => send({ op: "hyp_conf", hypothesis_id: h.id, value: Number((e.target as HTMLInputElement).value) })}
                onKeyUp={(e) => send({ op: "hyp_conf", hypothesis_id: h.id, value: Number((e.target as HTMLInputElement).value) })} />
              <p className="field-hint">هذه «نسبة ترجيح» لما تراه أرجح بناءً على الأدلة التي بين يديك، وليست احتمالاً محسوباً.</p>
            </div>
            <SegmentedControl label="حالة الفرضية" name={`stance-${h.id}`} value={en.stance} disabled={busy}
              options={(["open", "leading", "ruled_out"] as const).map((s) => ({ value: s, label: STANCE_AR[s] }))}
              onChange={(s) => send({ op: "hyp_stance", hypothesis_id: h.id, stance: s, evidence_ids: s === "ruled_out" ? Object.keys(en.links).filter((k) => en.links[k] === "weakens") : undefined })} />
            {en.stance === "ruled_out" && Object.values(en.links).every((d) => d !== "weakens") && <Callout tone="warning">لاستبعاد فرضية اربط بها دليلاً واحداً على الأقل «يُضعفها».</Callout>}
            <details>
              <summary>ربط الأدلة ({Object.keys(en.links).length})</summary>
              {view.evidence.length === 0 ? <p className="dim">لا أدلة بعد.</p> : view.evidence.map((e) => (
                <div key={e.id} className="board-row">
                  <span>{e.title_ar}</span>
                  <SegmentedControl label={`علاقة ${e.title_ar} بالفرضية`} name={`link-${h.id}-${e.id}`} value={en.links[e.id] ?? ""} disabled={busy}
                    options={DIRS.map(([d, l, tone]) => ({ value: d, label: l, tone }))} onChange={(d) => send({ op: "hyp_link", hypothesis_id: h.id, evidence_id: e.id, dir: d })} />
                </div>
              ))}
            </details>
            <p className="small dim">سجل المراجعات: {en.revisions.length} تعديل</p>
          </Card>
        );
      })}
    </div>
  );
}
