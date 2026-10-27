import type { PlayerView } from "@/engine/project";
import type { Actor } from "@/server/auth";
import { handlePlay, type PlayOp, type PlayResponse } from "@/server/play";

export const guest = (band: "16-17" | "18+" | "13-15" = "18+"): Actor => ({ kind: "device", user: null, ageBand: band });

export class Session {
  token: string | null = null;
  last!: PlayResponse;
  constructor(public caseId: string, public actor: Actor = guest()) {}
  async do(op: PlayOp): Promise<PlayResponse> {
    this.last = await handlePlay(this.actor, this.caseId, op, this.token);
    if (this.last.token) this.token = this.last.token;
    return this.last;
  }
  get view(): PlayerView { return this.last.view; }
  /** Exhaust every legitimate way of discovering evidence (what a thorough player does). */
  async exhaust(): Promise<void> {
    await this.do({ op: "start" });
    for (let round = 0; round < 12; round++) {
      const before = this.view.evidence.length + this.view.facts.length + this.view.stats.actions_taken;
      for (const a of this.view.actions) { try { await this.do({ op: "act", action_id: a.id }); } catch { /* exhausted */ } }
      for (const c of this.view.characters) {
        if (!c.interview_open) continue;
        for (const t of c.topics) { try { await this.do({ op: "ask", character_id: c.id, topic_id: t.id }); } catch { /* closed */ } }
        for (const e of [...this.view.evidence]) { try { await this.do({ op: "present", evidence_id: e.id, character_id: c.id }); } catch { /* none */ } }
      }
      const after = this.view.evidence.length + this.view.facts.length + this.view.stats.actions_taken;
      if (after === before) break;
    }
  }
}
