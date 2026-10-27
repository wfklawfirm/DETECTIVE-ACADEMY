import { cx } from "./button";

export function ProgressBar({ value, max = 100, tone, label, className }: { value: number; max?: number; tone?: "positive" | "info"; label: string; className?: string }) {
  const pct = Math.max(0, Math.min(100, max ? (value / max) * 100 : 0));
  return <div className={cx("progress", className)} data-tone={tone} role="progressbar" aria-label={label} aria-valuemin={0} aria-valuemax={max} aria-valuenow={value}><i style={{ inlineSize: `${pct}%` }} /></div>;
}
/** Dots, not a bar, so steps stay countable. */
export function StepDots({ total, current, label }: { total: number; current: number; label: string }) {
  return <span className="dots" role="img" aria-label={label}>{Array.from({ length: total }, (_, i) => <i key={i} data-state={i < current ? "done" : i === current ? "current" : "todo"} />)}</span>;
}
/** Small ring; the value is always printed inside, never conveyed by arc length alone. */
export function ProgressRing({ value, max = 100, size = 56, text, label }: { value: number; max?: number; size?: number; text?: string; label: string }) {
  const r = 20, c = 2 * Math.PI * r, f = max ? Math.max(0, Math.min(1, value / max)) : 0;
  return (
    <span className="ring" style={{ inlineSize: size, blockSize: size }} role="img" aria-label={label}>
      <svg viewBox="0 0 48 48" aria-hidden><circle className="track" cx="24" cy="24" r={r} fill="none" strokeWidth="5" /><circle className="arc" cx="24" cy="24" r={r} fill="none" strokeWidth="5" strokeDasharray={c} strokeDashoffset={c * (1 - f)} /></svg>
      <span className="val" aria-hidden>{text ?? Math.round(value)}</span>
    </span>
  );
}
