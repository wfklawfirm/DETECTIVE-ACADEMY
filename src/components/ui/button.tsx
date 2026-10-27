import Link from "next/link";
import type { ButtonHTMLAttributes, ComponentProps, ReactNode } from "react";

export type Variant = "primary" | "secondary" | "outline" | "ghost" | "destructive";
export type Size = "sm" | "md" | "lg";
export const cx = (...a: (string | false | null | undefined)[]) => a.filter(Boolean).join(" ");
const face = (variant: Variant, size: Size, block?: boolean, extra?: string) => cx("btn", `btn-${variant}`, size !== "md" && `btn-${size}`, block && "btn-block", extra);

type BtnProps = ButtonHTMLAttributes<HTMLButtonElement> & { variant?: Variant; size?: Size; block?: boolean; loading?: boolean };
export function Button({ variant = "secondary", size = "md", block, loading, className, children, disabled, type = "button", ...rest }: BtnProps) {
  return (
    <button type={type} className={face(variant, size, block, className)} disabled={disabled || loading} data-loading={loading || undefined} aria-busy={loading || undefined} {...rest}>
      {loading && <span className="spinner" aria-hidden />}
      {children}
    </button>
  );
}

type LinkProps = ComponentProps<typeof Link> & { variant?: Variant; size?: Size; block?: boolean };
/** Navigation is a real link, never a button with router.push. */
export function LinkButton({ variant = "secondary", size = "md", block, className, ...rest }: LinkProps) {
  return <Link className={face(variant, size, block, className)} {...rest} />;
}

/** Icon-only control: the accessible label is required. */
export function IconButton({ label, children, className, type = "button", ...rest }: ButtonHTMLAttributes<HTMLButtonElement> & { label: string; children: ReactNode }) {
  return <button type={type} className={cx("icon-btn", className)} aria-label={label} {...rest}>{children}</button>;
}
export function IconLink({ label, children, className, ...rest }: ComponentProps<typeof Link> & { label: string }) {
  return <Link className={cx("icon-btn", className)} aria-label={label} {...rest}>{children}</Link>;
}
