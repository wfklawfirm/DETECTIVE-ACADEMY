import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Detective Academy — تحقيقات تتعلّم منها",
    short_name: "Detective Academy",
    description: "منصة عربية للألغاز التحقيقية القائمة على الأدلة (نموذج تجريبي).",
    id: "/",
    start_url: "/home",
    scope: "/",
    display: "standalone",
    orientation: "portrait",
    dir: "rtl",
    lang: "ar",
    background_color: "#0b1115",
    theme_color: "#0b1115",
    categories: ["education", "entertainment"],
    icons: [
      { src: "/icons/icon-192.png", sizes: "192x192", type: "image/png", purpose: "any" },
      { src: "/icons/icon-512.png", sizes: "512x512", type: "image/png", purpose: "any" },
      { src: "/icons/maskable-512.png", sizes: "512x512", type: "image/png", purpose: "maskable" },
    ],
    shortcuts: [
      {
        name: "القضايا",
        short_name: "القضايا",
        description: "تصفّح ملفات التحقيق",
        url: "/cases",
        icons: [{ src: "/icons/icon-192.png", sizes: "192x192" }],
      },
      {
        name: "الأكاديمية",
        short_name: "الأكاديمية",
        description: "دروس قصيرة في منهجية التحقيق",
        url: "/academy",
        icons: [{ src: "/icons/icon-192.png", sizes: "192x192" }],
      },
      {
        name: "المختبرات",
        short_name: "المختبرات",
        description: "تمارين تفاعلية قصيرة",
        url: "/labs",
        icons: [{ src: "/icons/icon-192.png", sizes: "192x192" }],
      },
    ],
  };
}
