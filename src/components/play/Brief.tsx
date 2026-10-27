"use client";
import { Button } from "../ui/button";
import { Callout } from "../ui/feedback";
import { Card, SectionTitle } from "../ui/card";
import type { Resp, View } from "./usePlay";

export function BriefTab({ view, busy, send, last, goto }: { view: View; busy: boolean; send: (r: Record<string, unknown>) => Promise<Resp | null>; last: Resp["extra"] | null; goto: (t: string, charId?: string) => void }) {
  const first = view.evidence.length === 0 && view.stats.actions_taken <= 1;
  const groups: [string, string][] = [["examine", "اطّلع على"], ["search_location", "ابحث في"], ["interview", "قابل"], ["request_lab_test", "اطلب فحصاً"]];
  return (
    <div className="stack-lg">
      {first && <div className="cold-open lantern" style={{ padding: "1rem" }} aria-label="افتتاحية">{view.cold_open_ar.map((l, i) => <p key={i} className={`reveal stagger-${Math.min(i + 1, 4)}`}>{l}</p>)}</div>}
      <Card as="section" aria-label="الدور والمكان">
        <div><p className="text-label">الدور</p><p>{view.premise.player_role_ar}</p></div>
        <div><p className="text-label">المكان والزمان</p><p>{view.premise.setting_ar}</p></div>
      </Card>
      {view.stage_hook_ar && <p className="narrative dim-2">{view.stage_hook_ar}</p>}
      <section className="stack"><h2 className="text-section-title">ما نعرفه حتى الآن</h2>
        <ul>{view.facts.map((f) => <li key={f.id}>{f.statement_ar}</li>)}</ul>
        <p className="small dim">هذه الوقائع المسلَّم بها في بداية الملف. ما عداها عليك إثباته.</p></section>
      <section className="stack"><h2 className="text-section-title">ماذا تفعل الآن؟</h2>
        {view.actions.length === 0 && <p className="dim">لا إجراءات متاحة الآن.</p>}
        {groups.map(([type, title]) => { const acts = view.actions.filter((a) => a.type === type); return acts.length ? (
          <div key={type} className="stack-sm"><SectionTitle as="h3">{title}</SectionTitle>
            {acts.map((a) => <Button key={a.id} variant="secondary" block className="btn-start" disabled={busy} onClick={async () => { const r = await send({ op: "act", action_id: a.id }); if (a.type === "interview") goto("people", a.target_id); void r; }}>{a.label_ar}</Button>)}
          </div>) : null; })}
      </section>
      {last?.granted_evidence?.length ? <Callout tone="positive" title={`أُضيف ${last.granted_evidence.length} دليل إلى خزانتك`}><Button variant="outline" size="sm" onClick={() => goto("evidence")}>افتح الخزانة</Button></Callout> : null}
    </div>
  );
}
