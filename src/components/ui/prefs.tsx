"use client";
import { createContext, useCallback, useContext, useEffect, useState, type ReactNode } from "react";
import { ls } from "@/lib/client";
import { setSfx, sfxOn } from "@/lib/sfx";

export type ThemePref = "dark" | "light" | "system";
interface Prefs { theme: ThemePref; largeText: boolean; reduceMotion: boolean; sfx: boolean; setTheme: (t: ThemePref) => void; setLargeText: (v: boolean) => void; setReduceMotion: (v: boolean) => void; setSfxOn: (v: boolean) => void }
const Ctx = createContext<Prefs>({ theme: "dark", largeText: false, reduceMotion: false, sfx: false, setTheme() {}, setLargeText() {}, setReduceMotion() {}, setSfxOn() {} });
export const usePrefs = () => useContext(Ctx);

const THEME_COLOR = { dark: "#0b1115", light: "#f2efe8" } as const;
export function resolveTheme(p: ThemePref): "dark" | "light" {
  if (p !== "system") return p;
  try { return window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark"; } catch { return "dark"; }
}
function apply(theme: ThemePref, large: boolean, motionOff: boolean) {
  const r = document.documentElement, t = resolveTheme(theme);
  r.setAttribute("data-theme", t);
  if (large) r.setAttribute("data-text-size", "large"); else r.removeAttribute("data-text-size");
  if (motionOff) r.setAttribute("data-motion", "off"); else r.removeAttribute("data-motion");
  document.querySelectorAll('meta[name="theme-color"]').forEach((m) => m.setAttribute("content", THEME_COLOR[t]));
}

/** Inline script that runs before first paint (no flash). Mirrors apply(); every storage access is guarded. */
export const NO_FLASH_SCRIPT = `(function(){try{var d=document.documentElement,g=function(k){try{return localStorage.getItem(k)}catch(e){return null}};var t=g("athar.theme");if(t!=="light"&&t!=="system")t="dark";if(t==="system"){t=window.matchMedia&&window.matchMedia("(prefers-color-scheme: light)").matches?"light":"dark"}d.setAttribute("data-theme",t);if(g("athar.text")==="large")d.setAttribute("data-text-size","large");if(g("athar.motion")==="off")d.setAttribute("data-motion","off");var m=document.querySelector('meta[name="theme-color"]');if(m)m.setAttribute("content",t==="light"?"${THEME_COLOR.light}":"${THEME_COLOR.dark}")}catch(e){document.documentElement.setAttribute("data-theme","dark")}})();`;

export function PrefsProvider({ children }: { children: ReactNode }) {
  const [theme, setT] = useState<ThemePref>("dark");
  const [largeText, setL] = useState(false);
  const [reduceMotion, setM] = useState(false);
  const [sfx, setS] = useState(false);
  useEffect(() => {
    const t = ls.get("athar.theme");
    setT(t === "light" || t === "system" ? t : "dark");
    setL(ls.get("athar.text") === "large");
    setM(ls.get("athar.motion") === "off");
    setS(sfxOn());
  }, []);
  // follow the OS only while the user picked "system"
  useEffect(() => {
    if (theme !== "system") return;
    let mq: MediaQueryList | null = null;
    try { mq = window.matchMedia("(prefers-color-scheme: light)"); } catch { return; }
    const on = () => apply("system", largeText, reduceMotion);
    mq.addEventListener("change", on);
    return () => mq?.removeEventListener("change", on);
  }, [theme, largeText, reduceMotion]);
  const setTheme = useCallback((t: ThemePref) => { setT(t); ls.set("athar.theme", t); apply(t, largeText, reduceMotion); }, [largeText, reduceMotion]);
  const setLargeText = useCallback((v: boolean) => { setL(v); if (v) ls.set("athar.text", "large"); else ls.del("athar.text"); apply(theme, v, reduceMotion); }, [theme, reduceMotion]);
  const setReduceMotion = useCallback((v: boolean) => { setM(v); if (v) ls.set("athar.motion", "off"); else ls.del("athar.motion"); apply(theme, largeText, v); }, [theme, largeText]);
  const setSfxOn = useCallback((v: boolean) => { setSfx(v); setS(v); }, []);
  return <Ctx.Provider value={{ theme, largeText, reduceMotion, sfx, setTheme, setLargeText, setReduceMotion, setSfxOn }}>{children}</Ctx.Provider>;
}
