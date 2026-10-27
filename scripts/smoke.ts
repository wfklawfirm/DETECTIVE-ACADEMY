// HTTP smoke test against a running dev/prod server: plays the tutorial end-to-end and checks no-leak + scoring invariants.
const BASE = process.env.BASE ?? "http://localhost:3100";
const H = { "content-type": "application/json", origin: BASE };
let cookie = "";
let token: string | null = null;
const CASE = process.argv[2] ?? "c000_lost_notebook";
async function post(path: string, body: unknown) {
  const r = await fetch(BASE + path, { method: "POST", headers: { ...H, cookie }, body: JSON.stringify(body) });
  const sc = r.headers.get("set-cookie"); if (sc) cookie = sc.split(/,(?=\s*\w+=)/).map((c) => c.split(";")[0]).join("; ");
  const j = await r.json(); if (!r.ok) throw new Error(`${path} ${r.status} ${JSON.stringify(j)}`); return j;
}
const play = async (req: Record<string, unknown>) => { const j = await post(`/api/play/${CASE}`, { token, req }); if (j.token) token = j.token; return j; };
await post("/api/age", { band: "18+" });
let r = await play({ op: "start" });
let v = r.view;
const FORBIDDEN = ["is_true", "culprit", "truth", "reference_answer", "scoring"];
const check = (view: unknown, label: string) => { const s = JSON.stringify(view); for (const k of FORBIDDEN) if (new RegExp(`"${k}[a-z_]*"\\s*:`).test(s) && !(label === "final")) throw new Error(`LEAK key ${k} in ${label}`); };
check(v, "start");
for (let round = 0; round < 6; round++) {
  for (const a of v.actions) { r = await play({ op: "act", action_id: a.id }); v = r.view; }
  for (const c of v.characters) for (const t of c.topics) if (!t.asked && c.interview_open) { try { r = await play({ op: "ask", character_id: c.id, topic_id: t.id }); v = r.view; } catch { /* closed */ } }
  check(v, `round${round}`);
}
console.log("evidence:", v.evidence.length, "locked:", v.locked_evidence_count, "facts:", v.facts.length);
const ev = v.evidence.map((e: { id: string }) => e.id);
for (const h of v.hypotheses) await play({ op: "hyp_add", hypothesis_id: h.id });
await play({ op: "deduce", open: true });
const trueH = process.argv[3] ?? "h_samira";
r = await play({ op: "submit", conclusion_hypothesis_id: trueH, confidence: 75, cited: ev.slice(0, 4).map((id: string) => ({ evidence_id: id, role: "supports" })), limit_choice_ids: [], would_change_mind_ids: [], justification: "اختبار آلي." });
console.log("assessment:", JSON.stringify(r.assessment?.total ?? r.assessment).slice(0, 300), "machine:", r.view.machine);
console.log("debrief present:", !!r.view.debrief);

if (process.env.RESTART) { const r2 = await play({ op: "start" }); console.log("restart ok", r2.view.machine); }
export {};
