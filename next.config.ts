import { readdirSync, statSync } from "node:fs";
import type { NextConfig } from "next";

// Everything under content/ is bundled for runtime reads EXCEPT the (large, admin-only) research library,
// which is added only to the routes that read it. Computed from the directory so new content folders are picked up.
const contentGlobs = readdirSync("./content")
  .filter((n) => n !== "research")
  .map((n) => (statSync(`./content/${n}`).isDirectory() ? `./content/${n}/**/*` : `./content/${n}`));

const securityHeaders = [
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "X-Frame-Options", value: "DENY" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" },
  {
    key: "Content-Security-Policy",
    value:
      "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; font-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'",
  },
];

const nextConfig: NextConfig = {
  poweredByHeader: false,
  reactStrictMode: true,
  serverExternalPackages: ["@libsql/client"],
  // runtime reads of content and migrations must be bundled into the serverless output
  outputFileTracingIncludes: {
    "/**": [...contentGlobs, "./migrations/**/*"],
    "/studio/library": ["./content/research/**/*"],
    "/studio/library/[...path]": ["./content/research/**/*"],
  },
  async headers() {
    return [{ source: "/:path*", headers: securityHeaders }];
  },
};
export default nextConfig;
