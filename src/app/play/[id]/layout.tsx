import type { Metadata } from "next";
import { getActorFromCookies } from "@/server/auth";
import { getPlayable } from "@/server/content";

export async function generateMetadata({ params }: { params: Promise<{ id: string }> }): Promise<Metadata> {
  const { id } = await params;
  let title = "تحقيق جارٍ";
  let description = "افتح ملف القضية، اقرأ الأدلة، استجوب الشهود، وابنِ حجتك خطوة بخطوة.";
  try {
    await getActorFromCookies();
    const c = await getPlayable(id);
    if (c) {
      title = c.ui.cover.title_ar;
      description = `${c.ui.cover.tagline_ar} — قضية في Detective Academy تتمرّن فيها على قراءة الأدلة والاستدلال.`;
    }
  } catch { /* unauthenticated or DB unavailable — fall back to generic */ }
  return {
    title,
    description,
    robots: { index: false, follow: false },
    openGraph: { title: `${title} · Detective Academy`, description, type: "article", siteName: "Detective Academy" },
    twitter: { card: "summary", title: `${title} · Detective Academy` },
  };
}

export default function PlayLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
