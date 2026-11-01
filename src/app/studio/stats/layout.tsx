import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "إحصاءات Studio",
  robots: { index: false, follow: false },
};

export default function StudioStatsLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
