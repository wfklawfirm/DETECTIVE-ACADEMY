import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "ابدأ أول قضية",
  description: "جرّب Detective Academy مباشرةً: افتح أول ملفّ قضائي خيالي، تعرّف على كيفية قراءة الأدلة، وجرّب الاستجواب — في ١٢ دقيقة.",
  robots: { index: true, follow: true },
  openGraph: {
    title: "ابدأ أول قضية · Detective Academy",
    description: "جرّب منصة Detective Academy مباشرةً — اقرأ الأدلة واستنتج في ١٢ دقيقة.",
    type: "website",
    siteName: "Detective Academy",
  },
  twitter: { card: "summary", title: "ابدأ أول قضية · Detective Academy" },
  alternates: { canonical: "/start" },
};

export default function StartLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
