import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { CERTAINTY_AR, STATUS_AR, type MasteryStatus } from "@/engine/mastery";

export interface SkillItem { ko_id: string; name_ar: string; status: MasteryStatus; certainty: 0 | 1 | 2; cases: string[]; track: string | null; lesson_id: string | null }
const STEP: Record<MasteryStatus, number> = { insufficient_evidence: 0, emerging: 1, developing: 2, secure: 3 };

/** Verbal status + 3 segments + certainty dots. No percentages, no ranking, no comparison with other people. */
export function SkillCard({ s }: { s: SkillItem }) {
  const on = STEP[s.status];
  return (
    <Card flat>
      <div className="row row-between"><b>{s.name_ar}</b>{s.track && <Badge>مسار {s.track}</Badge>}</div>
      <span className="meter" role="img" aria-label={`${STATUS_AR[s.status]}. ${CERTAINTY_AR[s.certainty]}`}>
        <span className="meter-segs" aria-hidden>{[0, 1, 2].map((i) => <i key={i} data-on={i < on} />)}</span>
        <span className="small" aria-hidden>{STATUS_AR[s.status]}</span>
      </span>
      <p className="small dim" aria-hidden>{CERTAINTY_AR[s.certainty]}</p>
      <p className="small dim">من: {s.cases.join("، ")}</p>
    </Card>
  );
}
