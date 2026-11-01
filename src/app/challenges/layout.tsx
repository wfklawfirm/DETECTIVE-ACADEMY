import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "التحديات",
  description: "تحديات استدلالية يومية في Detective Academy: تمارين قصيرة على تحليل الأدلة والاستنتاج المنطقي — مقدّرة لاكتشاف نقاط قوتك وثغرات تفكيرك.",
  robots: { index: true, follow: true },
  openGraph: {
    title: "التحديات · Detective Academy",
    description: "تحديات يومية في علم الأدلة والمنطق التحقيقي — كل تحدٍّ مصمَّم ليكشف أين تقف.",
    type: "website",
    siteName: "Detective Academy",
  },
  twitter: { card: "summary", title: "التحديات · Detective Academy" },
  alternates: { canonical: "/challenges" },
};

export default function ChallengesLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
