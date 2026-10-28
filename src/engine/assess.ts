import type { CaseFile, PlayState, Submission } from "./types";
import type { CaseUi, ScoringSpec } from "./ui-types";
import { EngineError } from "./state";
import { contentTokens } from "../lib/arabic";
import { hintPenalty as hintPenaltyOf } from "./hints";

export interface CriterionResult {
  id: string; name_ar: string; weight: number; fraction: number | null; level: number | null; status: "scored" | "pending_human";
  feedback_ar: string[]; evidence_of_performance: string[];
}
export interface AssessmentResult {
  provisional: true;
  disclaimer_ar: string;
  total_pct: number | null; // deterministic part only, renormalised
  deterministic_weight: number;
  criteria: CriterionResult[];
  caps_applied: string[];
  accepted_grade: number;
  hints_used: number;
  needs_human_review: boolean;
  review_ticket: { seq: number; justification: string };
}

const DISCLAIMER = "هذه درجة تعليمية مبدئية مبنية على قواعد معلنة ومرتبطة بسلوكك داخل القضية. ليست مقياساً نفسياً مقنناً ولا حكماً على ذكائك، وجزء الحجة المكتوبة ينتظر مراجعة بشرية.";

export function validateSubmission(c: CaseFile, ui: CaseUi, st: PlayState, s: Omit<Submission, "seq">): void {
  if (!c.hypotheses.some((h) => h.id === s.conclusion_hypothesis_id)) throw new EngineError("bad_conclusion", "الاستنتاج المختار غير معروف");
  if (!(s.confidence >= 0 && s.confidence <= 100)) throw new EngineError("bad_value", "الثقة بين 0 و100");
  if (s.cited.length < 1) throw new EngineError("need_citation", "اذكر دليلاً واحداً على الأقل");
  if (s.cited.length > 12) throw new EngineError("too_many", "عدد الأدلة المذكورة كبير");
  for (const ct of s.cited) if (!st.evidence.includes(ct.evidence_id)) throw new EngineError("not_owned", "تستشهد بدليل لا تملكه");
  const lim = new Set(ui.limit_menu.map((m) => m.id)), mc = new Set(ui.mind_change_menu.map((m) => m.id));
  for (const l of s.limit_choice_ids) if (!lim.has(l)) throw new EngineError("bad_limit", "حد استنتاج غير معروف");
  for (const m of s.would_change_mind_ids) if (!mc.has(m)) throw new EngineError("bad_mind", "خيار غير معروف");
  if (s.justification.length > 4000) throw new EngineError("too_long", "الحجة طويلة جداً");
}

const levelFor = (c: CaseFile, crit: string, f: number) => {
  const lv = c.rubric.criteria.find((x) => x.id === crit)?.levels ?? [];
  const best = [...lv].sort((a, b) => b.score - a.score).find((l) => l.score / 4 <= f + 1e-9);
  return best ? best.score : 0;
};

/** Deterministic, explainable assessment. Free-text justification is NEVER auto-scored for content: it is queued for human review. */
export function assess(c: CaseFile, ui: CaseUi, sc: ScoringSpec, st: PlayState, sub: Submission): AssessmentResult {
  const evT = (id: string) => c.evidence.find((e) => e.id === id)?.title_ar ?? id;
  const hyT = (id: string) => c.hypotheses.find((h) => h.id === id)?.statement_ar ?? id;
  const crits: CriterionResult[] = [];
  const caps: string[] = [];
  const hintsUsed = st.hints.length;
  const hintPenalty = hintPenaltyOf(st.hints, c.hint_ladder);

  for (const crit of c.rubric.criteria) {
    const kind = sc.criteria_map[crit.id];
    const weight = crit.weight ?? 0;
    const fb: string[] = [], eop: string[] = [];
    let f: number | null = null;
    switch (kind) {
      case "source_typing": {
        const keys = Object.entries(sc.source_key);
        let ok = 0, tagged = 0;
        for (const [e, cls] of keys) {
          const got = st.source_tags[e];
          if (got) tagged++;
          if (got === cls) ok++;
          else if (got) fb.push(`صنّفت «${evT(e)}» على أنه ${labelOf(ui, got)}؛ التصنيف الأدق في هذه القضية: ${labelOf(ui, cls)}.`);
          else if (st.evidence.includes(e)) fb.push(`لم تصنّف مصدر «${evT(e)}»؛ التصنيف يغيّر وزن الدليل.`);
        }
        f = keys.length ? ok / keys.length : 1;
        eop.push(`صنّفت ${tagged} من ${keys.length} مصدراً، وأصبت ${ok}.`);
        break;
      }
      case "conflict_resolution": {
        let got = 0;
        const req = sc.lab_requirement;
        if (req) {
          const converged = st.lab_runs.some((r) => r.lab_id === req.lab_id && r.converged);
          if (converged) { got = 1; eop.push("نفّذت مختبر الزمن بمدخلات متسقة وأفضت إلى تطابق الأزمنة."); }
          else if (st.lab_runs.some((r) => r.lab_id === req.lab_id)) { got = 0.3; fb.push("شغّلت المختبر لكن مدخلاتك لم تُوحّد الأزمنة؛ راجع الإزاحة الزمنية وانحراف الساعة المذكورين في الأدلة."); }
          else fb.push("لم تُشغّل مختبر الزمن؛ بدونه يبقى تفسير اختلاف الأزمنة ادعاءً غير مختبر.");
        }
        if (sc.timeline_requirement?.length) {
          const tr = sc.timeline_requirement;
          const good = tr.filter((r) => { const p = st.timeline.find((t) => t.evidence_id === r.evidence_id); return p && Math.abs(p.utc_minute - r.utc_minute) <= r.tol; }).length;
          const tf = good / tr.length;
          if (tf > 0) eop.push(`وضعت ${good} من ${tr.length} على الخط الزمني في موضعها الصحيح (±${tr[0]!.tol} د).`);
          else fb.push("لم تضع الأحداث على الخط الزمني بالتوقيت الموحّد.");
          got = req ? Math.max(got, 0.5 * got + 0.5 * tf) : tf;
          if (req && got === 1 && tf < 1) got = 0.85;
        }
        f = got;
        break;
      }
      case "hypothesis_links": {
        let ok = 0, total = 0, wrong = 0;
        const owned = new Set(st.evidence);
        for (const [h, m] of Object.entries(sc.link_key)) {
          for (const [e, d] of Object.entries(m)) {
            if (!owned.has(e)) continue;
            total++;
            const g = st.hypotheses[h]?.links[e];
            if (g === d) ok++;
            else if (g && g !== "neutral") { wrong++; fb.push(`ربطت «${evT(e)}» بفرضية «${hyT(h)}» باتجاه ${dirAr(g)}، والأقرب إلى الأدلة: ${dirAr(d)}.`); }
          }
        }
        const touchedHyps = Object.values(st.hypotheses).filter((h) => Object.keys(h.links).length > 0).length;
        f = total ? Math.max(0, ok - 0.5 * wrong) / total : 0;
        if (touchedHyps < 2) { f = Math.min(f, 0.5); fb.push("قارنت فرضية واحدة فقط؛ المقارنة بين فرضيتين على الأقل شرط للدرجة الكاملة."); }
        eop.push(`ربطت ${touchedHyps} فرضية بأدلة؛ ${ok} من ${total} روابط مُقدَّرة وافقت تحليل الأدلة.`);
        break;
      }
      case "uncertainty": {
        const acc = sc.accepted_conclusions[sub.conclusion_hypothesis_id];
        const band = sc.confidence_band[sub.conclusion_hypothesis_id];
        let cal = 0.5;
        if (band) {
          if (sub.confidence >= band[0] && sub.confidence <= band[1]) cal = 1;
          else { const d = sub.confidence < band[0] ? band[0] - sub.confidence : sub.confidence - band[1]; cal = Math.max(0, 1 - d / 50); fb.push(`ثقتك ${sub.confidence}% خارج النطاق المعقول لهذا الاستنتاج (${band[0]}–${band[1]}%)، وسبب ذلك مبيّن في الشرح الختامي.`); }
        }
        const chosen = new Set(sub.limit_choice_ids);
        const reqHit = sc.required_limits.filter((l) => chosen.has(l)).length;
        const bad = sc.invalid_limits.filter((l) => chosen.has(l)).length;
        const limf = Math.max(0, reqHit - bad) / Math.max(1, sc.required_limits.length);
        if (limf < 1) fb.push("حدود الاستنتاج التي ذكرتها لا تغطي كل ما لا تستطيع الأدلة إثباته.");
        const mc = new Set(sub.would_change_mind_ids);
        const mcOk = sc.valid_mind_changers.filter((m) => mc.has(m)).length > 0 ? 1 : 0;
        if (!mcOk) fb.push("لم تحدد دليلاً جديداً يمكنه فعلاً تغيير رأيك؛ هذا من علامات التفكير العلمي.");
        f = (acc ? 0.4 * cal + 0.4 * limf + 0.2 * mcOk : 0.2 * cal + 0.2 * limf);
        eop.push(`ثقة ${sub.confidence}%، حدود مذكورة ${sub.limit_choice_ids.length}، أدلة قد تغيّر الرأي ${sub.would_change_mind_ids.length}.`);
        break;
      }
      case "revision": {
        const leadSeq = Object.entries(st.hypotheses).flatMap(([h, e]) => e.revisions.filter((r) => r.kind === "stance" && r.detail.endsWith("->leading")).map((r) => ({ h, seq: r.seq, ev: r.evidence_count })));
        const refuted = new Set(sc.refuted_hypotheses);
        const ledLoser = leadSeq.some((l) => refuted.has(l.h));
        const finalOk = (sc.accepted_conclusions[sub.conclusion_hypothesis_id]?.grade ?? 0) > 0;
        if (!leadSeq.length) { f = 0.5; fb.push("لم تُعلن فرضية «رائدة» أثناء التحقيق؛ إعلان الفرضية وتعديلها يُظهر مراجعة رأيك عند ظهور الدليل."); }
        else if (ledLoser && finalOk) { f = 1; eop.push("بدأت بفرضية ثم عدّلت موقفك بعد أدلة جديدة إلى استنتاج متسق مع الأدلة — مراجعة مبررة."); }
        else if (ledLoser && !finalOk) { f = 0; fb.push("بقيت على فرضية تنقضها أدلة أتيحت لك."); }
        else { f = finalOk ? 1 : 0.2; eop.push(finalOk ? "ثبتّ على فرضية متسقة مع الأدلة دون تعسف." : "ثبتّ على فرضية لا تدعمها الأدلة."); }
        break;
      }
      case "elimination": {
        const bad = Object.entries(st.hypotheses).filter(([h, e]) => e.stance === "ruled_out" && sc.refuted_hypotheses.includes(h));
        const wrongOut = Object.entries(st.hypotheses).filter(([h, e]) => e.stance === "ruled_out" && !sc.refuted_hypotheses.includes(h));
        f = sc.refuted_hypotheses.length ? Math.max(0, bad.length - wrongOut.length) / sc.refuted_hypotheses.length : 1;
        eop.push(`استبعدت ${bad.length} فرضية بدليل مرفق صحيحاً.`);
        if (wrongOut.length) fb.push("استبعدت فرضية لا تقتضيها الأدلة.");
        break;
      }
      case "justification_human": {
        f = null;
        fb.push("الحجة المكتوبة أُرسلت لمراجعة بشرية بحسب سلّم التقييم؛ لا تُمنح درجة آلية على جودة الصياغة.");
        if (sub.justification.trim()) eop.push(`كتبت حجة من ${contentTokens(sub.justification).length} كلمة مفيدة (للمراجِع فقط، لا تدخل في الدرجة).`);
        break;
      }
      default:
        f = null;
    }
    crits.push({ id: crit.id, name_ar: crit.name_ar, weight, fraction: f, level: f === null ? null : levelFor(c, crit.id, f), status: f === null ? "pending_human" : "scored", feedback_ar: fb, evidence_of_performance: eop });
  }

  const scored = crits.filter((x) => x.fraction !== null);
  const wsum = scored.reduce((s, x) => s + x.weight, 0);
  let pct = wsum ? (scored.reduce((s, x) => s + x.weight * (x.fraction ?? 0), 0) / wsum) * 100 : null;
  const accepted = sc.accepted_conclusions[sub.conclusion_hypothesis_id]?.grade ?? 0;
  if (pct !== null) {
    // Guessing guard: right answer alone is never full credit
    const citedDecisive = sc.decisive_evidence.filter((e) => sub.cited.some((c2) => c2.evidence_id === e)).length;
    if (citedDecisive < Math.min(2, sc.decisive_evidence.length)) { pct = Math.min(pct, sc.caps.no_citations_max); caps.push(`سقف ${sc.caps.no_citations_max}% لأن الاستشهاد لا يتضمن دليلين حاسمين على الأقل`); }
    const labConv = sc.lab_requirement ? st.lab_runs.some((r) => r.lab_id === sc.lab_requirement!.lab_id && r.converged) : true;
    const tlOk = sc.timeline_requirement?.length ? sc.timeline_requirement.every((r) => { const p = st.timeline.find((t) => t.evidence_id === r.evidence_id); return p && Math.abs(p.utc_minute - r.utc_minute) <= r.tol; }) : false;
    if (!labConv && !tlOk && (sc.lab_requirement || sc.timeline_requirement)) { pct = Math.min(pct, sc.caps.no_conflict_resolution_max); caps.push(`سقف ${sc.caps.no_conflict_resolution_max}% لأنك لم تحلّ تعارض الأزمنة بالمختبر أو الخط الزمني`); }
    pct = pct * accepted_scale(accepted);
    if (accepted < 1) caps.push(`استنتاجك أُعطي ${Math.round(accepted * 100)}% من اتساق الاستنتاج مع الأدلة`);
    if (hintPenalty > 0) { pct = pct * (1 - hintPenalty); caps.push(`خُفّضت الدرجة ${Math.round(hintPenalty * 100)}% بسبب التلميحات المستخدمة (لا تُحتسب ضد مهارتك، بل ضد استقلالية الحل)`); }
    pct = Math.round(Math.max(0, Math.min(100, pct)));
  }
  return {
    provisional: true, disclaimer_ar: DISCLAIMER, total_pct: pct, deterministic_weight: Number(wsum.toFixed(3)), criteria: crits,
    caps_applied: caps, accepted_grade: accepted, hints_used: hintsUsed, needs_human_review: crits.some((x) => x.status === "pending_human"),
    review_ticket: { seq: sub.seq, justification: sub.justification },
  };
}
const accepted_scale = (g: number) => 0.4 + 0.6 * g; // a wrong conclusion keeps process credit but never exceeds 40%
const labelOf = (ui: CaseUi, id: string) => ui.source_classes.find((s) => s.id === id)?.label_ar ?? id;
const dirAr = (d: string) => (d === "supports" ? "يدعم" : d === "weakens" ? "يضعف" : "لا يميّز");

export interface TransferResult { score_pct: number; right: string[]; missed: string[]; wrong: string[]; note_ar: string }
export function scoreTransfer(sc: ScoringSpec, picked: string[]): TransferResult {
  const key = sc.transfer_key;
  if (!key) throw new EngineError("no_transfer", "لا يوجد اختبار نقل لهذه القضية");
  const p = new Set(picked);
  const right = key.valid.filter((v) => p.has(v)), missed = key.valid.filter((v) => !p.has(v)), wrong = key.invalid.filter((v) => p.has(v));
  const pct = Math.round(Math.max(0, (right.length - wrong.length) / key.valid.length) * 100);
  return { score_pct: pct, right, missed, wrong, note_ar: "قياس نقل المهارة: ثلاثة أسئلة قصيرة لا تغني عن اختبار مستقل متكرر؛ هذه نتيجة أولية على سياق جديد." };
}
