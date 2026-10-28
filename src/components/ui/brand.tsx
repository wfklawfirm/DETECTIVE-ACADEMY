import Link from "next/link";

/**
 * ATHAR mark — magnifier with fingerprint inside.
 * Uses currentColor so it inverts automatically in dark/light themes.
 * The outer ring has a subtle "motion streak" arc matching the uploaded logo.
 */
export function AtharMark({ size = 32, className }: { size?: number; className?: string }) {
  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox="0 0 100 100"
      fill="none"
      aria-hidden
      focusable="false"
    >
      {/* Motion / swipe streak behind the lens */}
      <path
        d="M8 52 Q4 30 18 15"
        stroke="currentColor"
        strokeWidth="3"
        strokeLinecap="round"
        opacity="0.35"
      />
      <path
        d="M10 60 Q2 38 14 20"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        opacity="0.2"
      />

      {/* Outer magnifier ring */}
      <circle cx="42" cy="42" r="30" stroke="currentColor" strokeWidth="7" />

      {/* Fingerprint arcs — 5 concentric loops, largest to smallest */}
      <path
        d="M22 48 Q20 34 32 26 Q44 18 56 26 Q66 34 62 48"
        stroke="currentColor"
        strokeWidth="3.2"
        strokeLinecap="round"
        fill="none"
      />
      <path
        d="M26 50 Q24 38 34 31 Q44 24 54 31 Q62 38 60 50"
        stroke="currentColor"
        strokeWidth="3.2"
        strokeLinecap="round"
        fill="none"
      />
      <path
        d="M30 52 Q28 42 36 36 Q44 30 52 36 Q58 42 57 52"
        stroke="currentColor"
        strokeWidth="3.2"
        strokeLinecap="round"
        fill="none"
      />
      <path
        d="M34 54 Q32 46 38 41 Q44 36 50 41 Q54 46 53 54"
        stroke="currentColor"
        strokeWidth="3.2"
        strokeLinecap="round"
        fill="none"
      />
      <path
        d="M38 56 Q36 50 41 46 Q44 43 47 46 Q50 50 50 56"
        stroke="currentColor"
        strokeWidth="3.2"
        strokeLinecap="round"
        fill="none"
      />

      {/* Magnifier handle */}
      <line x1="64" y1="64" x2="82" y2="82" stroke="currentColor" strokeWidth="9" strokeLinecap="round" />
    </svg>
  );
}

/** Header lockup: mark + «Detective Academy» wordmark. */
export function BrandWordmark({ href = "/home" }: { href?: string }) {
  return (
    <Link href={href} className="brand" aria-label="Detective Academy — الرئيسية">
      <AtharMark className="brand-mark" size={30} />
      <span className="brand-text" aria-hidden>
        <span className="brand-name">Detective</span>
        <span className="brand-latin">Academy</span>
      </span>
    </Link>
  );
}
