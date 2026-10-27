import Link from "next/link";

export interface Card { case_id: string; title_ar: string; kicker_ar: string; tagline_ar: string; glyph: string; accent: string; minutes: number; difficulty: number; age_band: string; tutorial?: boolean; preview?: boolean }
export interface Prog { case_id: string; title_ar: string; machine: string; done: boolean; evidence_count: number; locked_count: number; updated_at: string }

export function CaseCard({ c, p }: { c: Card; p?: Prog }) {
  const href = p && !p.done ? `/play/${c.case_id}` : `/case/${c.case_id}`;
  return (
    <Link href={href} className="card case-card" data-accent={c.accent}>
      <span className="glyph" aria-hidden>{c.glyph}</span>
      <span className="kicker">{c.kicker_ar}</span>
      <h3 style={{ margin: 0 }}>{c.title_ar}</h3>
      <p className="dim" style={{ margin: 0 }}>{c.tagline_ar}</p>
      <div className="row small">
        <span className="chip">{c.minutes} دقيقة</span>
        <span className="chip">{"●".repeat(c.difficulty)}{"○".repeat(Math.max(0, 5 - c.difficulty))} <span className="sr-only">الصعوبة {c.difficulty} من 5</span></span>
        {c.preview && <span className="chip amber">نسخة تجريبية قيد المراجعة</span>}
        {p?.done && <span className="chip green">أُنجزت</span>}
        {p && !p.done && <span className="chip cyan">قيد التحقيق · {p.evidence_count} دليلاً</span>}
      </div>
    </Link>
  );
}

