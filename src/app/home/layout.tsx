import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "الرئيسية",
  description: "لوحة تحكم المحقق — قضاياك الجارية ومستواك وما يُنتظرك.",
  robots: { index: false, follow: false },
};

export default function HomeLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
