import type { ReactNode } from "react";
import { cx } from "./button";
import { AlertIcon, InfoIcon, CheckIcon } from "./icons";

export const Skeleton = ({ className }: { className?: string }) => <span className={cx("skeleton", className)} aria-hidden />;
export function SkeletonCard({ lines = 2 }: { lines?: number }) {
  return (
    <div className="card" aria-hidden>
      <Skeleton className="skeleton-title" />
      {Array.from({ length: lines }, (_, i) => <Skeleton key={i} className="skeleton-line" />)}
    </div>
  );
}
/** Skeletons, not spinners: a page that reflows is worse than a slow one. */
export function LoadingRegion({ label = "جارٍ التحميل", cards = 3 }: { label?: string; cards?: number }) {
  return (
    <div role="status" aria-live="polite" className="stack">
      <span className="sr-only">{label}…</span>
      {Array.from({ length: cards }, (_, i) => <SkeletonCard key={i} />)}
    </div>
  );
}
export function EmptyState({ title, body, action, icon }: { title: string; body?: ReactNode; action?: ReactNode; icon?: ReactNode }) {
  return <div className="card empty">{icon && <span className="ico" aria-hidden>{icon}</span>}<p className="card-title">{title}</p>{body && <p className="small dim-2">{body}</p>}{action}</div>;
}
export function ErrorState({ title = "تعذّر التحميل", body, action }: { title?: string; body?: ReactNode; action?: ReactNode }) {
  return <div className="card error-state" role="alert"><div className="row" style={{ flexWrap: "nowrap", alignItems: "flex-start" }}><AlertIcon className="ico" /><div className="stack-sm grow"><p className="card-title">{title}</p>{body && <p className="small">{body}</p>}{action}</div></div></div>;
}
export function Callout({ tone = "info", title, children, icon, role }: { tone?: "info" | "positive" | "warning" | "negative" | "brand"; title?: string; children: ReactNode; icon?: ReactNode; role?: "status" | "alert" }) {
  const I = tone === "warning" || tone === "negative" ? AlertIcon : tone === "positive" ? CheckIcon : InfoIcon;
  return <div className="callout" data-tone={tone} role={role}><span className="ico" aria-hidden>{icon ?? <I size={20} />}</span><div className="grow">{title && <b>{title}</b>}{children}</div></div>;
}
