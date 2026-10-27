"use client";
import { useCallback, useEffect, useRef, useState } from "react";
import { api, ApiError, getToken, setToken } from "@/lib/client";
import { playSfx, type Sfx } from "@/lib/sfx";
import type { PlayResponse } from "@/server/play";
import type { PlayerView } from "@/engine/project";

export type View = PlayerView;
export type Resp = Omit<PlayResponse, "view"> & { view: PlayerView };

/** Thin client for the server-authoritative play API. All game logic lives on the server; this only sends intents. */
export function usePlay(caseId: string) {
  const [resp, setResp] = useState<Resp | null>(null);
  const [error, setError] = useState<{ code: string; message: string } | null>(null);
  const [busy, setBusy] = useState(false);
  const [last, setLast] = useState<Resp["extra"] | null>(null);
  const tokenRef = useRef<string | null>(null);
  const evCount = useRef(0);
  const booted = useRef(false);

  const send = useCallback(async (req: Record<string, unknown>): Promise<Resp | null> => {
    setBusy(true); setError(null);
    try {
      const r = await api<Resp>(`/api/play/${caseId}`, { token: tokenRef.current, req });
      if (r.token) { tokenRef.current = r.token; setToken(caseId, r.token); }
      const n = r.view.evidence.length;
      const sound: Sfx | null = req.op === "start" ? "open" : n > evCount.current ? "paper" : req.op === "submit" ? "confirm" : req.op === "hyp_add" || req.op === "note" ? "pen" : req.op === "hyp_link" || req.op === "hyp_stance" ? "drop" : null;
      evCount.current = n; if (sound) playSfx(sound);
      setResp(r); setLast(r.extra);
      return r;
    } catch (e) {
      playSfx("error");
      if (e instanceof ApiError) setError({ code: e.code, message: e.message }); else setError({ code: "net", message: "تعذّر الاتصال. تحقق من الشبكة وحاول مرة أخرى." });
      return null;
    } finally { setBusy(false); }
  }, [caseId]);

  useEffect(() => {
    if (booted.current) return; booted.current = true;
    tokenRef.current = getToken(caseId);
    void send({ op: "start" });
  }, [caseId, send]);

  return { resp, view: resp?.view ?? null, error, busy, last, send, clearError: () => setError(null) };
}
