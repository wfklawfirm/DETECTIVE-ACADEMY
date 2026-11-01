import type { Metadata } from "next";
import { getActorFromCookies } from "@/server/auth";
import { getPlayable } from "@/server/content";

export async function generateMetadata({ params }: { params: Promise<{ id: string }> }): Promise<Metadata> {
  const { id } = await params;
  let title = "تفاصيل القضية";
  let description = "اقرأ ملف القضية، تعرّف على الشخصيات والأدلة، وابدأ التحقيق.";
  try {
    await getActorFromCookies();
    const c = await getPlayable(id);
    if (c) {
      title = c.ui.cover.title_ar;
      const kicker = c.ui.cover.kicker_ar;
      description = `${kicker} — ${c.ui.cover.tagline_ar}`;
    }
  } catch { /* unauthenticated or DB unavailable — fall back to generic */ }
  return {
    title,
    description,
    robots: { index: false, follow: false },
    openGraph: { title: `${title} · Detective Academy`, description, type: "article", siteName: "Detective Academy" },
    twitter: { card: "summary", title: `${title} · Detective Academy` },
    alternates: { canonical: `/case/${id}` },
  };
}

export default function CaseDetailLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
