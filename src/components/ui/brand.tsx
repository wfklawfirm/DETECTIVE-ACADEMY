import Link from "next/link";

/** ATHAR mark: a magnifier ring whose lens holds three concentric trace arcs (a fingerprint-like trail) ending in a single point. */
export function AtharMark({ size = 32, className }: { size?: number; className?: string }) {
  return (
    <svg className={className} width={size} height={size} viewBox="0 0 48 48" fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" aria-hidden focusable="false">
      <circle cx="21" cy="21" r="14.5" strokeWidth="3" />
      <path d="M14.5 24.5a7 7 0 0112.8-3.9" strokeWidth="2.2" />
      <path d="M18 26.5a3.6 3.6 0 016.8-1.6" strokeWidth="2.2" />
      <circle cx="21.4" cy="21.2" r="1.3" fill="currentColor" stroke="none" />
      <path d="M32 32l10.5 10.5" strokeWidth="4" />
    </svg>
  );
}

/** Header lockup: mark + «Detective Academy» wordmark. */
export function BrandWordmark({ href = "/home" }: { href?: string }) {
  return (
    <Link href={href} className="brand" aria-label="Detective Academy — الرئيسية">
      <AtharMark className="brand-mark" size={30} />
      <span className="brand-text" aria-hidden><span className="brand-name">Detective</span><span className="brand-latin">Academy</span></span>
    </Link>
  );
}
