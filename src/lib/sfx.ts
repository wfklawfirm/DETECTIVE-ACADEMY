"use client";
import { ls } from "./client";

/** Optional interface sounds. Off by default; the choice lives only in this browser. Sounds are short CC0 / public-domain clips (see /credits). */
export type Sfx = "open" | "paper" | "click" | "confirm" | "error" | "drop" | "pen" | "panel" | "lock";
const FILE: Record<Sfx, string> = { open: "AUD-0001", paper: "AUD-0146", click: "AUD-0022", confirm: "AUD-0025", error: "AUD-0029", drop: "AUD-0042", pen: "AUD-0047", panel: "AUD-0033", lock: "AUD-0019" };
const KEY = "athar.sfx";
export const sfxOn = (): boolean => ls.get(KEY) === "1";
export function setSfx(on: boolean): void { if (on) ls.set(KEY, "1"); else ls.del(KEY); }
const cache = new Map<Sfx, HTMLAudioElement>();
export function playSfx(s: Sfx): void {
  if (typeof window === "undefined" || !sfxOn()) return;
  try {
    let a = cache.get(s);
    if (!a) { a = new Audio(`/assets/sfx/${FILE[s]}.ogg`); a.volume = 0.35; a.preload = "auto"; cache.set(s, a); }
    a.currentTime = 0; void a.play().catch(() => { /* autoplay blocked: stay silent */ });
  } catch { /* no audio support */ }
}
