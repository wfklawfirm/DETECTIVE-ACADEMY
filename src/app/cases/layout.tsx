import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "القضايا",
  description: "تصفّح قضايا Detective Academy: ألغاز خيالية تعتمد على الأدلة الحقيقية — من جرائم السرقة إلى قضايا الاختفاء. كل قضية مختبر استدلالي مستقل.",
  robots: { index: true, follow: true },
  openGraph: {
    title: "القضايا · Detective Academy",
    description: "ألغاز خيالية مبنية على أدلة حقيقية — تقرأ الملفات وتستجوب الشهود وتثبت حقيقة كل قضية.",
    type: "website",
    siteName: "Detective Academy",
  },
  twitter: { card: "summary", title: "القضايا · Detective Academy" },
  alternates: { canonical: "/cases" },
};

export default function CasesLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
