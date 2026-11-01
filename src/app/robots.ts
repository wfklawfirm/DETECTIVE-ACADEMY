import type { MetadataRoute } from "next";

const BASE = "https://detectiveacademy.app";

/**
 * Beta: block all crawlers.
 * When ready to open, change disallow to:
 *   allow: ["/", "/cases", "/labs", "/academy", "/knowledge", "/season",
 *            "/glossary", "/biases", "/methods", "/reasoning", "/rulebook",
 *            "/archetypes", "/atlas", "/books", "/skills", "/heritage",
 *            "/gallery", "/sounds", "/sources", "/credits"]
 *   disallow: ["/api/", "/studio/", "/account", "/profile", "/play/", "/home",
 *              "/forgot", "/reset", "/report"]
 */
export default function robots(): MetadataRoute.Robots {
  return {
    rules: { userAgent: "*", disallow: "/" },
    sitemap: `${BASE}/sitemap.xml`,
  };
}
