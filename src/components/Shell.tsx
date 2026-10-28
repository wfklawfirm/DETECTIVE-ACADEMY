"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { createContext, useCallback, useContext, useEffect, useState, type ReactNode } from "react";
import { api, setGentle, type Me } from "@/lib/client";
import { AgeGate } from "./AgeGate";
import { MenuSheet } from "./MenuSheet";
import { BrandWordmark } from "./ui/brand";
import { IconButton, IconLink } from "./ui/button";
import { BackIcon, BookIcon, FolderIcon, HomeIcon, LibraryIcon, MenuIcon, ProfileIcon } from "./ui/icons";
import { PrefsProvider } from "./ui/prefs";
import { ToastProvider } from "./ui/toast";

interface Ctx { me: Me | null; refresh: () => Promise<void> }
const MeCtx = createContext<Ctx>({ me: null, refresh: async () => {} });
export const useMe = () => useContext(MeCtx);

/** Five destinations, no more. Everything else lives in the header menu. */
export const NAV = [
  { href: "/home",      label: "الرئيسية",  Icon: HomeIcon,    match: ["/home", "/challenges"] },
  { href: "/cases",     label: "القضايا",   Icon: FolderIcon,  match: ["/cases", "/case", "/play"] },
  { href: "/academy",   label: "الأكاديمية",Icon: BookIcon,    match: ["/academy"] },
  { href: "/knowledge", label: "الموسوعة",  Icon: LibraryIcon, match: ["/knowledge", "/labs", "/sources", "/skills", "/gallery"] },
  { href: "/profile",   label: "مهاراتي",   Icon: ProfileIcon, match: ["/profile", "/account", "/review", "/studio"] },
] as const;

const inSection = (path: string, bases: readonly string[]) =>
  bases.some((b) => path === b || path.startsWith(b + "/"));

/** Deep screens get a back arrow + context label; top-level screens get the wordmark. */
const BACK: [prefix: string, href: string, label: string][] = [
  ["/play",      "/cases",     "القضايا"],
  ["/case",      "/cases",     "القضايا"],
  ["/academy/",  "/academy",   "الأكاديمية"],
  ["/knowledge/","/knowledge", "الموسوعة"],
  ["/labs/",     "/labs",      "المختبرات"],
  ["/labs",      "/knowledge", "الموسوعة"],
  ["/sources",   "/knowledge", "الموسوعة"],
  ["/skills",    "/knowledge", "الموسوعة"],
  ["/gallery",   "/knowledge", "الموسوعة"],
  ["/credits",   "/home",      "الرئيسية"],
  ["/privacy",   "/home",      "الرئيسية"],
  ["/report",    "/home",      "الرئيسية"],
  ["/challenges","/home",      "الرئيسية"],
  ["/account",   "/profile",   "مهاراتي"],
  ["/studio",    "/profile",   "مهاراتي"],
  ["/review",    "/profile",   "مهاراتي"],
  ["/start",     "/",          "الصفحة الأولى"],
];

const WIDE = ["/studio", "/gallery", "/credits", "/sources", "/skills"];

export function Shell({ children }: { children: ReactNode }) {
  return <PrefsProvider><ToastProvider><Inner>{children}</Inner></ToastProvider></PrefsProvider>;
}

function Inner({ children }: { children: ReactNode }) {
  const path = usePathname() ?? "/";
  const [me, setMe] = useState<Me | null>(null);
  const [ready, setReady] = useState(false);
  const [menu, setMenu] = useState(false);

  const refresh = useCallback(async () => {
    try {
      const m = await api<Me>("/api/me");
      setMe(m);
      if (m.user) setGentle(m.user.gentle_hooks);
    } catch { /* offline */ }
    setReady(true);
  }, []);

  useEffect(() => { void refresh(); }, [refresh]);
  useEffect(() => { setMenu(false); }, [path]);

  const needsGate = ready && !!me && !me.age_band && !path.startsWith("/privacy");
  const playing   = path.startsWith("/play/");
  const landing   = path === "/";
  const showNav   = !playing && !landing && !path.startsWith("/start");
  const staff     = !!me?.user && ["editor", "reviewer", "admin"].includes(me.user.role);
  const back      = BACK.find(([p]) => (p.endsWith("/") ? path.startsWith(p) : path === p || path.startsWith(p + "/")));
  const wide      = WIDE.some((w) => path === w || path.startsWith(w + "/"));

  return (
    <MeCtx.Provider value={{ me, refresh }}>
      {/* Desktop sidebar — hidden on mobile/tablet via CSS */}
      {showNav && (
        <nav className="desktop-sidebar" aria-label="التنقل الرئيسي">
          <div className="sidebar-brand">
            <BrandWordmark href="/home" />
          </div>
          <div className="sidebar-nav">
            {NAV.map(({ href, label, Icon, match }) => {
              const cur = inSection(path, match);
              return (
                <Link key={href} href={href} aria-current={cur ? "page" : undefined}>
                  <span className="nav-icon" aria-hidden><Icon size={20} /></span>
                  <span>{label}</span>
                </Link>
              );
            })}
          </div>
          <div className="sidebar-footer">
            Detective Academy · نموذج تجريبي
          </div>
        </nav>
      )}

      <div
        className={`frame${showNav ? " has-bottom-nav" : ""}`}
        data-wide={wide || undefined}
      >
        <a className="skip" href="#main">تجاوز إلى المحتوى</a>

        {/* Mobile + tablet header */}
        <header className="app-header">
          <div className="app-header-inner">
            {back ? (
              <>
                <IconLink href={back[1]} label={`رجوع إلى ${back[2]}`}><BackIcon /></IconLink>
                <span className="app-header-title" aria-hidden>{back[2]}</span>
              </>
            ) : (
              <>
                <BrandWordmark href={landing ? "/" : "/home"} />
                <span className="app-header-spacer" />
              </>
            )}
            <IconButton
              label="القائمة"
              aria-haspopup="dialog"
              aria-expanded={menu}
              onClick={() => setMenu(true)}
            >
              <MenuIcon />
            </IconButton>
          </div>
        </header>

        <main
          id="main"
          className={`page${playing ? " with-tabs" : ""}`}
          tabIndex={-1}
        >
          {children}
        </main>

        {!playing && (
          <footer
            className="page small dim"
            style={{
              flex: "none",
              paddingBlock: 0,
              paddingBlockEnd: showNav
                ? "calc(var(--bottom-nav-height) + env(safe-area-inset-bottom) + 1rem)"
                : "1.5rem",
            }}
          >
            Detective Academy · نموذج تجريبي. القصص كلها من تأليفنا وشخصياتها خيالية.
          </footer>
        )}

        {/* Mobile + tablet bottom nav */}
        {showNav && (
          <nav className="bottom-nav" aria-label="التنقل الرئيسي">
            <ul>
              {NAV.map(({ href, label, Icon, match }) => {
                const cur = inSection(path, match);
                return (
                  <li key={href}>
                    <Link href={href} aria-current={cur ? "page" : undefined}>
                      <Icon size={24} />
                      <span>{label}</span>
                    </Link>
                  </li>
                );
              })}
            </ul>
          </nav>
        )}
      </div>

      <MenuSheet
        open={menu}
        onClose={() => setMenu(false)}
        path={path}
        me={me}
        staff={staff}
      />

      {needsGate && <AgeGate onDone={refresh} />}
    </MeCtx.Provider>
  );
}
