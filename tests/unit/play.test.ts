import { beforeAll, describe, expect, it } from "vitest";
import { forbiddenKeysIn } from "@/engine/leak";
import { migrate } from "@/server/db";
import { syncFileCases } from "@/server/content";
import { Session, guest } from "./helpers";

beforeAll(async () => { await migrate(); await syncFileCases(); });

describe("tutorial play-through", () => {
  it("starts with no evidence and never exposes hidden truth keys", async () => {
    const s = new Session("c000_lost_notebook");
    const r = await s.do({ op: "start" });
    expect(r.view.evidence).toHaveLength(0);
    expect(r.view.machine).toBe("investigating");
    expect(forbiddenKeysIn(r.view, [])).toEqual([]);
    const j = JSON.stringify(r);
    for (const bad of ["is_true", "culprit_ids", "reference_answer_ar", "solution", "accepted_conclusions", "link_key", "source_key"]) expect(j).not.toContain(`"${bad}"`);
  });
  it("hides mirror ASK_ actions and compare_evidence from the player", async () => {
    const s = new Session("c001_last_observation");
    const r = await s.do({ op: "start" });
    expect(r.view.actions.some((a) => a.id.startsWith("ask_") || a.type === "compare_evidence")).toBe(false);
  });
  it("rejects direct use of mirror actions", async () => {
    const s = new Session("c000_lost_notebook"); await s.do({ op: "start" });
    await expect(s.do({ op: "act", action_id: "ask_samira_f_spill" })).rejects.toThrow();
  });
  it("evidence is only gained through gated actions (cannot cite what you do not hold)", async () => {
    const s = new Session("c000_lost_notebook"); await s.do({ op: "start" });
    await s.do({ op: "deduce", open: true });
    await expect(s.do({ op: "submit", conclusion_hypothesis_id: "h_samira", confidence: 80, cited: [{ evidence_id: "ev_note_shelf", role: "supports" }], limit_choice_ids: [], would_change_mind_ids: [], justification: "" })).rejects.toThrow();
  });
  it("a thorough player can reach the full evidence set and every view stays leak-free", async () => {
    const s = new Session("c000_lost_notebook");
    await s.exhaust();
    expect(s.view.evidence.length).toBe(7);
    expect(forbiddenKeysIn(s.view, [])).toEqual([]);
  });
});

describe("assessment resists gaming", () => {
  const submit = async (s: Session, concl: string, conf: number, citedIds: string[], limits: string[], mind: string[]) => {
    await s.do({ op: "deduce", open: true });
    return s.do({ op: "submit", conclusion_hypothesis_id: concl, confidence: conf, cited: citedIds.map((evidence_id) => ({ evidence_id, role: "supports" as const })), limit_choice_ids: limits, would_change_mind_ids: mind, justification: "" });
  };
  it("T07: the right answer with thin evidence and no work scores low", async () => {
    const s = new Session("c000_lost_notebook"); await s.exhaust();
    const first = s.view.evidence[0]!.id;
    const r = await submit(s, "h_samira", 95, [first], [], []);
    expect(r.assessment!.total_pct!).toBeLessThan(55);
  });
  it("T08: a thorough, well-reasoned submission beats the lazy one", async () => {
    const lazy = new Session("c000_lost_notebook"); await lazy.exhaust();
    const a = await submit(lazy, "h_samira", 95, [lazy.view.evidence[0]!.id], [], []);
    const good = new Session("c000_lost_notebook"); await good.exhaust();
    for (const e of good.view.evidence) await good.do({ op: "tag", evidence_id: e.id, cls: ({ ev_jamal_statement: "claim", ev_hadi_statement: "claim" } as Record<string, "claim">)[e.id] ?? "primary_record" });
    const b = await submit(good, "h_samira", 78, ["ev_lab_sheet", "ev_jamal_statement", "ev_cleaning_ticket", "ev_note_shelf"], ["l_why", "l_time"], ["m_late_sign"]);
    expect(b.assessment!.total_pct!).toBeGreaterThan(a.assessment!.total_pct!);
  });
  it("T09: a confidently wrong conclusion is capped low", async () => {
    const s = new Session("c000_lost_notebook"); await s.exhaust();
    const r = await submit(s, "h_hadi", 98, s.view.evidence.map((e) => e.id), ["l_why", "l_time"], ["m_late_sign"]);
    expect(r.assessment!.total_pct!).toBeLessThanOrEqual(45);
  });
  it("citing everything is not rewarded over citing the right things", async () => {
    const all = new Session("c000_lost_notebook"); await all.exhaust();
    const ra = await submit(all, "h_samira", 78, all.view.evidence.map((e) => e.id), ["l_why", "l_time"], ["m_late_sign"]);
    const pick = new Session("c000_lost_notebook"); await pick.exhaust();
    const rp = await submit(pick, "h_samira", 78, ["ev_lab_sheet", "ev_jamal_statement", "ev_cleaning_ticket", "ev_note_shelf"], ["l_why", "l_time"], ["m_late_sign"]);
    expect(rp.assessment!.total_pct!).toBeGreaterThanOrEqual(ra.assessment!.total_pct!);
  });
  it("marks results provisional and never auto-scores the written argument", async () => {
    const s = new Session("c000_lost_notebook"); await s.exhaust();
    await s.do({ op: "deduce", open: true });
    const r = await s.do({ op: "submit", conclusion_hypothesis_id: "h_samira", confidence: 70, cited: [{ evidence_id: s.view.evidence[0]!.id, role: "supports" }], limit_choice_ids: [], would_change_mind_ids: [], justification: "نص طويل جداً ومنمّق ".repeat(30), share_for_review: true });
    expect(r.assessment!.provisional).toBe(true);
    expect(r.assessment!.criteria.some((c) => c.status === "pending_human")).toBe(true);
    expect(r.review_ticket).toMatch(/^[A-Z0-9]{6,12}$/);
    const long = r.assessment!.total_pct;
    const s2 = new Session("c000_lost_notebook"); await s2.exhaust(); await s2.do({ op: "deduce", open: true });
    const r2 = await s2.do({ op: "submit", conclusion_hypothesis_id: "h_samira", confidence: 70, cited: [{ evidence_id: s2.view.evidence[0]!.id, role: "supports" }], limit_choice_ids: [], would_change_mind_ids: [], justification: "" });
    expect(r2.assessment!.total_pct).toBe(long);
  });
  it("debrief appears only after submission", async () => {
    const s = new Session("c000_lost_notebook"); const r = await s.do({ op: "start" });
    expect(r.view.debrief).toBeNull(); expect(r.view.transfer_task).toBeNull();
    await s.exhaust(); await s.do({ op: "deduce", open: true });
    const r2 = await s.do({ op: "submit", conclusion_hypothesis_id: "h_samira", confidence: 70, cited: [{ evidence_id: s.view.evidence[0]!.id, role: "supports" }], limit_choice_ids: [], would_change_mind_ids: [], justification: "" });
    expect(r2.view.debrief).not.toBeNull();
  });
});

describe("flagship time lab", () => {
  it("grants the normalised-times evidence only with correct offsets and skew", async () => {
    const s = new Session("c001_last_observation"); await s.exhaust();
    const have = new Set(s.view.evidence.map((e) => e.id));
    expect(have.has("ev_obs_log") && have.has("ev_press_board") && have.has("ev_archive_log")).toBe(true);
    const lab = s.view.labs[0]!;
    const bad = await s.do({ op: "lab", lab_id: lab.id, inputs: {} });
    expect(bad.extra.lab!.converged).toBe(false);
    expect(s.view.evidence.some((e) => e.id === "ev_lab_norm")).toBe(false);
    const ok = await s.do({ op: "lab", lab_id: lab.id, inputs: { "ev_press_board.offset_h": 3, "ev_press_board.skew_min": 4, "ev_archive_log.offset_h": 3, "ev_archive_log.skew_min": 4 } });
    expect(ok.extra.lab!.converged).toBe(true);
    expect(s.view.evidence.some((e) => e.id === "ev_lab_norm")).toBe(true);
  });
});

describe("age gating", () => {
  it("13-15 cannot open a 16+ case", async () => {
    await expect(new Session("c001_last_observation", guest("13-15")).do({ op: "start" })).rejects.toThrow();
  });
  it("no age band => refused", async () => {
    await expect(new Session("c000_lost_notebook", { kind: "device", user: null, ageBand: null }).do({ op: "start" })).rejects.toThrow();
  });
});

describe("flagship «الرصد الأخير» end-to-end", () => {
  it("a careful player reaches the correct conclusion and scores well; a guesser does not", async () => {
    const s = new Session("c001_last_observation"); await s.exhaust();
    const lab = s.view.labs[0]!;
    await s.do({ op: "lab", lab_id: lab.id, inputs: { "ev_press_board.offset_h": 3, "ev_press_board.skew_min": 4, "ev_archive_log.offset_h": 3, "ev_archive_log.skew_min": 4 } });
    expect(s.view.evidence.length).toBe(16);
    const trueH = "h_hisham";
    const cls: Record<string, "claim" | "primary_record" | "redisplay"> = { ev_reem_warning: "claim", ev_press_board: "redisplay", ev_yusuf_statement: "claim", ev_nadir_statement: "claim", ev_bulletin_form: "primary_record" };
    for (const e of s.view.evidence) await s.do({ op: "tag", evidence_id: e.id, cls: cls[e.id] ?? "primary_record" });
    await s.do({ op: "deduce", open: true });
    const r = await s.do({ op: "submit", conclusion_hypothesis_id: trueH, confidence: 80, cited: ["ev_reem_hdr", "ev_hisham_hdr", "ev_chat_log", "ev_ws_log", "ev_lab_norm"].map((evidence_id) => ({ evidence_id, role: "supports" as const })), limit_choice_ids: ["l_intent", "l_read_receipt"], would_change_mind_ids: ["m_other_user", "m_gps_fault"], justification: "" });
    expect(r.assessment!.accepted_grade).toBe(1);
    expect(r.assessment!.total_pct!).toBeGreaterThanOrEqual(60);
    const g = new Session("c001_last_observation"); await g.do({ op: "start" }); await g.do({ op: "deduce", open: true });
    await expect(g.do({ op: "submit", conclusion_hypothesis_id: trueH, confidence: 99, cited: [{ evidence_id: "ev_reem_hdr", role: "supports" }], limit_choice_ids: [], would_change_mind_ids: [], justification: "" })).rejects.toThrow();
  });
});
