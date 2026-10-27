"use client";
import { useId, type ReactNode } from "react";
import { cx } from "./button";

/** Owns id / label / hint / error wiring so no control is ever an unlabeled visual label. */
export function Field({ label, hint, error, children, className }: { label: ReactNode; hint?: ReactNode; error?: ReactNode; className?: string; children: (p: { id: string; "aria-describedby"?: string; "aria-invalid"?: boolean }) => ReactNode }) {
  const id = useId();
  const desc = [hint && `${id}-h`, error && `${id}-e`].filter(Boolean).join(" ") || undefined;
  return (
    <div className={cx("field", className)}>
      <label htmlFor={id}>{label}</label>
      {children({ id, "aria-describedby": desc, "aria-invalid": error ? true : undefined })}
      {hint && <p id={`${id}-h`} className="field-hint">{hint}</p>}
      {error && <p id={`${id}-e`} className="field-error" role="alert">{error}</p>}
    </div>
  );
}

export interface Opt { value: string; label: ReactNode; help?: ReactNode; tone?: "positive" | "negative" }

/** Radio / checkbox group as large tappable rows. Real inputs for native semantics; radio rows carry no aria-pressed. */
export function ChoiceGroup({ label, labelledBy, name, options, value, onChange, multiple, disabled, states, className }: {
  label?: string; labelledBy?: string; name: string; options: Opt[]; value: string | string[] | null; onChange: (v: string) => void; multiple?: boolean; disabled?: boolean; states?: Record<string, "correct" | "wrong">; className?: string;
}) {
  const sel = (v: string) => (multiple ? (value as string[]).includes(v) : value === v);
  return (
    <div className={cx("choices", className)} role={multiple ? "group" : "radiogroup"} aria-label={label} aria-labelledby={labelledBy}>
      {options.map((o) => (
        <label key={o.value} className="choice" data-state={states?.[o.value]}>
          <input type={multiple ? "checkbox" : "radio"} name={name} checked={sel(o.value)} disabled={disabled} onChange={() => onChange(o.value)} />
          <span>{o.label}{o.help && <span className="small dim" style={{ display: "block" }}>{o.help}</span>}</span>
        </label>
      ))}
    </div>
  );
}

/** Small option switcher: a radiogroup of native radios drawn as a pill strip. */
export function SegmentedControl({ label, name, options, value, onChange, disabled, className }: { label: string; name: string; options: Opt[]; value: string; onChange: (v: string) => void; disabled?: boolean; className?: string }) {
  return (
    <div className={cx("seg", className)} role="radiogroup" aria-label={label}>
      {options.map((o) => (
        <label key={o.value} className="seg-opt" data-tone={o.tone}>
          <input type="radio" name={name} checked={value === o.value} disabled={disabled} onChange={() => onChange(o.value)} />
          <span>{o.label}</span>
        </label>
      ))}
    </div>
  );
}

export function Toggle({ label, hint, checked, onChange, disabled }: { label: string; hint?: ReactNode; checked: boolean; onChange: (v: boolean) => void; disabled?: boolean }) {
  const id = useId();
  return (
    <div className="toggle-row">
      <span className="toggle-text"><b id={`${id}-l`}>{label}</b>{hint && <span className="small dim">{hint}</span>}</span>
      <button type="button" role="switch" className="toggle" aria-checked={checked} aria-labelledby={`${id}-l`} disabled={disabled} onClick={() => onChange(!checked)} />
    </div>
  );
}
