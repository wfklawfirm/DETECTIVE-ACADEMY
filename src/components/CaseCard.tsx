import { Badge } from "./ui/badge";
import { MasteryMeter } from "./ui/badge";
import { CardLink, Dossier } from "./ui/card";
import { ChevronIcon } from "./ui/icons";

export interface Card { case_id: string; title_ar: string; kicker_ar: string; tagline_ar: string; glyph: string; accent: string; minutes: number; difficulty: number; age_band: string; tutorial?: boolean; preview?: boolean }
export interface Prog { case_id: string; title_ar: string; machine: string; done: boolean; evidence_count: number; locked_count: number; updated_at: string }

/** A case cover: dossier tab (kicker) + full-width card. Status is a Badge; difficulty is segments + number + label. */
export function CaseCard({ c, p }: { c: Card; p?: Prog }) {
  const href = p && !p.done ? `/play/${c.case_id}` : `/case/${c.case_id}`;
  return (
    <Dossier tab={c.kicker_ar}>
      <CardLink href={href} className="dossier-cover">
        <span className="glyph" aria-hidden>{c.glyph}</span>
        <div className="row" style={{ flexWrap: "nowrap", alignItems: "flex-start" }}>
          <div className="stack-sm grow">
            <h3 className="card-title">{c.title_ar}</h3>
            <p className="small dim-2">{c.tagline_ar}</p>
          </div>
          <ChevronIcon className="chev" size={20} />
        </div>
        <div className="row small">
          <Badge>{c.minutes} دقيقة</Badge>
          {c.preview && <Badge tone="warning">نسخة تجريبية قيد المراجعة</Badge>}
          {p?.done && <Badge tone="positive">أُنجزت</Badge>}
          {p && !p.done && <Badge tone="brand">قيد التحقيق · {p.evidence_count} دليلاً</Badge>}
        </div>
        <MasteryMeter level={c.difficulty} max={5} label="الصعوبة" a11yLabel={`الصعوبة ${c.difficulty} من 5`} />
      </CardLink>
    </Dossier>
  );
}
