import Link from "next/link";
import type { ReactNode } from "react";
import { RIGHTS_LABEL } from "@/engine/knowledge-labels";
import { UNREVIEWED_NOTE, REFERENCE_PAGES, sourceRefs, type RulebookData } from "@/engine/reference";
import { Card, PageHead } from "../ui/card";
import { Callout } from "../ui/feedback";
import { LinkIcon, SearchIcon, FlaskIcon, ScaleIcon, ShieldIcon, UsersIcon } from "../ui/icons";

/** Every reference page opens with the same shape: title, a one-line mystery hook, then the provenance note. */
export function RefHead({ title, hook, kicker = "مرجع المحقق", note = true }: { title: string; hook: string; kicker?: string; note?: boolean }) {
  return (
    <>
      <PageHead title={title} kicker={kicker} />
      <aside className="lead-card animate-rise" aria-label="خيط الصفحة">
        <span className="mark"><SearchIcon size={18} />خيط</span>
        <p>{hook}</p>
      </aside>
      {note && <Callout tone="warning" title="مادة أولية">{UNREVIEWED_NOTE}</Callout>}
    </>
  );
}

/** Related reference pages, shown at the bottom of each page. */
export function MoreReference({ current }: { current: string }) {
  return (
    <nav aria-label="مراجع أخرى" className="stack-sm">
      <h2 className="text-label section-title">مراجع أخرى</h2>
      <ul className="list">
        {REFERENCE_PAGES.filter((p) => p.href !== current).map((p) => (
          <li key={p.href}><Link className="row-link" href={p.href}><span className="grow"><b>{p.title}</b><span className="small dim">{p.hint}</span></span></Link></li>
        ))}
      </ul>
    </nav>
  );
}

export function Paras({ text, className = "" }: { text: string; className?: string }) {
  return <>{text.split("\n").filter(Boolean).map((p, i) => <p key={i} className={className}>{p}</p>)}</>;
}

/** Sources behind a card. Protected sources are shown by title/year only, never excerpted. */
export function SourcesBox({ ids, compact }: { ids: string[]; compact?: boolean }) {
  const refs = sourceRefs(ids);
  if (!refs.length) return null;
  return (
    <details className="card card-flat">
      <summary>المصادر ({refs.length})</summary>
      {!compact && <p className="small dim">المصدر المحمي بحقوق نشر يُذكر هنا للإحالة فقط؛ لا ننسخ نصه.</p>}
      <ul className="stack-sm">
        {refs.map((s) => (
          <li key={s.id} className="small">
            {s.url && !compact ? <a href={s.url} rel="noopener noreferrer" target="_blank" lang="en" dir="ltr">{s.title}</a> : <span lang="en" dir="ltr">{s.title}</span>}
            {s.year ? ` (${s.year})` : ""}{compact ? "" : ` — ${RIGHTS_LABEL[s.rights ?? "UNKNOWN"] ?? s.rights}`}
          </li>
        ))}
      </ul>
    </details>
  );
}

export function KoLinkRow({ links }: { links: { id: string; name: string }[] }) {
  if (!links.length) return null;
  return (
    <div className="stack-sm">
      <span className="text-label dim"><LinkIcon size={14} style={{ verticalAlign: "-2px" }} /> مفاهيم مرتبطة في الموسوعة</span>
      <ul className="row" style={{ listStyle: "none", padding: 0, margin: 0, gap: "0.4rem" }}>
        {links.map((k) => <li key={k.id}><Link className="badge badge-outline" href={`/knowledge/${k.id}`}>{k.name}</Link></li>)}
      </ul>
    </div>
  );
}

const ICONS: Record<RulebookData["sections"][number]["icon"], ReactNode> = {
  magnifier: <SearchIcon size={26} />, speech: <UsersIcon size={26} />, flask: <FlaskIcon size={26} />, scale: <ScaleIcon size={26} />, shield: <ShieldIcon size={26} />,
};
/** Section pictogram for the illustrated rule list. */
export function RuleIcon({ name }: { name: RulebookData["sections"][number]["icon"] }) {
  return <span className="ico" aria-hidden style={{ color: "var(--accent)" }}>{ICONS[name]}</span>;
}

export function Section({ title, hook, children, id }: { title: string; hook?: string; children: ReactNode; id?: string }) {
  return (
    <section className="stack" id={id} aria-labelledby={id ? `${id}-h` : undefined} style={{ scrollMarginBlockStart: "calc(var(--header-height) + 0.75rem)" }}>
      <h2 className="text-section-title" id={id ? `${id}-h` : undefined}>{title}</h2>
      {hook && <p className="narrative">{hook}</p>}
      {children}
    </section>
  );
}

export { Card };
