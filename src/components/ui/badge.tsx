import type { HTMLAttributes } from "react";
import { cx } from "./button";

export type Tone = "neutral" | "brand" | "positive" | "negative" | "warning" | "info";
/** The only place status colours are spent as backgrounds. */
export function Badge({ tone = "neutral", outline, latin, className, ...rest }: HTMLAttributes<HTMLSpanElement> & { tone?: Tone; outline?: boolean; latin?: boolean }) {
  return <span className={cx("badge", tone !== "neutral" && `badge-${tone}`, outline && "badge-outline", latin && "badge-latin", className)} {...rest} />;
}

/** Segments + number + label: three redundant encodings, so colour is never the only signal. */
export function MasteryMeter({ level, max = 6, label, a11yLabel, className }: { level: number; max?: number; label?: string; a11yLabel: string; className?: string }) {
  return (
    <span className={cx("meter", className)} role="img" aria-label={a11yLabel}>
      <span className="meter-segs" aria-hidden>{Array.from({ length: max }, (_, i) => <i key={i} data-on={i < level} />)}</span>
      <span className="meter-num" aria-hidden>{level}/{max}</span>
      {label && <span className="small dim" aria-hidden>{label}</span>}
    </span>
  );
}
