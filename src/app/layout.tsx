import type { Metadata, Viewport } from "next";
import "@fontsource/amiri/arabic-400.css";
import "@fontsource/amiri/arabic-700.css";
import "@fontsource/amiri/latin-400.css";
import "@fontsource/ibm-plex-sans-arabic/arabic-400.css";
import "@fontsource/ibm-plex-sans-arabic/arabic-600.css";
import "@fontsource/ibm-plex-sans-arabic/latin-400.css";
import "@fontsource/ibm-plex-mono/latin-400.css";
import "@fontsource/reem-kufi/arabic-400.css";
import "../styles/globals.css";
import { Shell } from "@/components/Shell";
import { NO_FLASH_SCRIPT } from "@/components/ui/prefs";

export const metadata: Metadata = {
  title: { default: "أَثَر — تحقيقات تتعلّم منها", template: "%s · أَثَر" },
  description: "منصة عربية للألغاز التحقيقية القائمة على الأدلة: تقرأ الملفات، تستجوب الشهود، وتتعلّم كيف تعرف ما الذي تثبته الأدلة فعلاً.",
  robots: { index: false, follow: false },
  applicationName: "أثر",
  appleWebApp: { capable: true, title: "أثر", statusBarStyle: "black-translucent" },
};
export const viewport: Viewport = { width: "device-width", initialScale: 1, themeColor: "#0b1115", colorScheme: "dark light" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ar" dir="rtl" data-theme="dark" suppressHydrationWarning>
      <head><script dangerouslySetInnerHTML={{ __html: NO_FLASH_SCRIPT }} /></head>
      <body>
        <Shell>{children}</Shell>
      </body>
    </html>
  );
}
