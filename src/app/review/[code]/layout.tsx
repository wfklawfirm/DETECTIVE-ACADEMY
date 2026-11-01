import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "مراجعة التحقيق",
  description: "راجع أداءك في القضية — الأدلة التي استخدمتها، الفرضيات التي اتبعتها، والخطوات التي يمكن تحسينها.",
  robots: { index: false, follow: false },
};

export default function ReviewLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
