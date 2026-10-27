"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { createContext, useCallback, useContext, useEffect, useState } from "react";
import { api, setGentle, type Me } from "@/lib/client";
import { setSfx, sfxOn } from "@/lib/sfx";
import { AgeGate } from "./AgeGate";

interface Ctx { me: Me | null; refresh: () => Promise<void> }
const MeCtx = createContext<Ctx>({ me: null, refresh: async () => {} });
export const useMe = () => useContext(MeCtx);

const NAV = [
  { href: "/home", label: "ملفاتي" },
  { href: "/cases", label: "القضايا" },
  { href: "/academy", label: "الأكاديمية" },
  { href: "/knowledge", label: "الموسوعة" },
  { href: "/labs", label: "مختبرات" },
  { href: "/challenges", label: "تحديات" },
  { href: "/profile", label: "مهاراتي" },
];

export function Shell({ children }: { children: React.ReactNode }) {
  const path = usePathname();
  const [me, setMe] = useState<Me | null>(null);
  const [ready, setReady] = useState(false);
  const [sfx, setSfxState] = useState(false);
  useEffect(() => { setSfxState(sfxOn()); }, []);
  const refresh = useCallback(async () => {
    try { const m = await api<Me>("/api/me"); setMe(m); if (m.user) setGentle(m.user.gentle_hooks); } catch { /* offline */ }
    setReady(true);
  }, []);
  useEffect(() => { void refresh(); }, [refresh]);
  const needsGate = ready && me && !me.age_band && !path.startsWith("/privacy");
  const playing = path.startsWith("/play/");
  const staff = me?.user && ["editor", "reviewer", "admin"].includes(me.user.role);
  return (
    <MeCtx.Provider value={{ me, refresh }}>
      <div className="app">
        <header className="topbar">
          <div className="wrap">
            <Link href="/" className="brand" aria-label="أثر — الصفحة الرئيسية"><b>أَثَر</b><small>ATHAR</small></Link>
            <nav className="nav" aria-label="التنقل الرئيسي">
              {NAV.map((n) => <Link key={n.href} href={n.href} aria-current={path === n.href || path.startsWith(n.href + "/") ? "page" : undefined}>{n.label}</Link>)}
              {staff && <Link href="/studio" aria-current={path.startsWith("/studio") ? "page" : undefined}>الاستوديو</Link>}
              <Link href="/account" aria-current={path === "/account" ? "page" : undefined}>{me?.user ? (me.user.display_name ?? "حسابي") : "دخول"}</Link>
            </nav>
          </div>
        </header>
        <main id="main" className={playing ? "playing" : undefined} tabIndex={-1}>{children}</main>
        {!playing && (
          <footer className="footer">
            <div className="wrap">
              <span>أثر · نموذج تجريبي. القصص كلها من تأليفنا وشخصياتها خيالية.</span>
              <span><Link href="/privacy">الخصوصية والسلامة</Link> · <Link href="/report">أبلِغ عن مشكلة</Link> · <Link href="/skills">المهارات</Link> · <Link href="/gallery">المعرض</Link> · <Link href="/credits">الاعتمادات</Link> · <button className="linklike" aria-pressed={sfx} onClick={() => { setSfx(!sfx); setSfxState(!sfx); }}>المؤثرات الصوتية: {sfx ? "مفعّلة" : "مطفأة"}</button></span>
            </div>
          </footer>
        )}
        {needsGate && <AgeGate onDone={refresh} />}
      </div>
    </MeCtx.Provider>
  );
}
