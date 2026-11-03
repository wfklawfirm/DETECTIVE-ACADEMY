import type { Metadata, Viewport } from "next";
import "@fontsource/amiri/arabic-400.css";
import "@fontsource/amiri/arabic-700.css";
import "@fontsource/amiri/latin-400.css";
import "@fontsource/ibm-plex-sans-arabic/latin-400.css";
import "@fontsource/ibm-plex-mono/latin-400.css";
import "@fontsource/reem-kufi/arabic-400.css";
import localFont from "next/font/local";
import "../styles/globals.css";
import "../styles/redesign.css";
import { Shell } from "@/components/Shell";
import { NO_FLASH_SCRIPT } from "@/components/ui/prefs";

/* Arabic UI font via next/font: preloaded, with size-adjusted fallback (less layout shift). */
const plexArabic = localFont({
  src: [
    { path: "../../node_modules/@fontsource/ibm-plex-sans-arabic/files/ibm-plex-sans-arabic-arabic-400-normal.woff2", weight: "400", style: "normal" },
    { path: "../../node_modules/@fontsource/ibm-plex-sans-arabic/files/ibm-plex-sans-arabic-arabic-600-normal.woff2", weight: "600", style: "normal" },
  ],
  variable: "--font-plex-ar",
  display: "swap",
});

export const metadata: Metadata = {
  title: { default: "Detective Academy — تحقيقات تتعلّم منها", template: "%s · Detective Academy" },
  description: "منصة عربية للألغاز التحقيقية القائمة على الأدلة: تقرأ الملفات، تستجوب الشهود، وتتعلّم كيف تعرف ما الذي تثبته الأدلة فعلاً.",
  robots: { index: false, follow: false },
  applicationName: "Detective Academy",
  appleWebApp: { capable: true, title: "Detective Academy", statusBarStyle: "black-translucent" },
  openGraph: {
    type: "website",
    siteName: "Detective Academy",
    title: "Detective Academy — تحقيقات تتعلّم منها",
    description: "منصة عربية للألغاز التحقيقية القائمة على الأدلة: تقرأ الملفات، تستجوب الشهود، وتتعلّم كيف تعرف ما الذي تثبته الأدلة فعلاً.",
    locale: "ar_SA",
  },
  twitter: {
    card: "summary",
    title: "Detective Academy — تحقيقات تتعلّم منها",
    description: "منصة عربية للألغاز التحقيقية القائمة على الأدلة: تقرأ الملفات، تستجوب الشهود، وتتعلّم كيف تعرف ما الذي تثبته الأدلة فعلاً.",
  },
};
export const viewport: Viewport = { width: "device-width", initialScale: 1, themeColor: "#111619", colorScheme: "dark light" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ar" dir="rtl" data-theme="dark" className={plexArabic.variable} suppressHydrationWarning>
      <head><script dangerouslySetInnerHTML={{ __html: NO_FLASH_SCRIPT }} /></head>
      <body>
        <Shell>{children}</Shell>
      </body>
    </html>
  );
}
