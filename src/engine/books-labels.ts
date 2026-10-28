/** Client-safe labels and types for the book concept notes. No node:fs here. */
export const SKILLS = ["evidence_handling", "scene_documentation", "timing", "witness_reliability", "lab_limits", "reporting"] as const;
export type Skill = (typeof SKILLS)[number];
export const SKILL_LABEL: Record<Skill, string> = {
  evidence_handling: "التعامل مع الأدلة", scene_documentation: "توثيق المشهد", timing: "التوقيت والتسلسل",
  witness_reliability: "موثوقية الشهود", lab_limits: "حدود المختبر", reporting: "كتابة التقرير",
};
export const AGE_LABEL = { all: "لكل الأعمار", "13-15": "١٣–١٥", "16-18": "١٦–١٨", "18+": "١٨ فأكثر" } as const;
export const SAFETY_LABEL = { safe: "آمن", conceptual: "مفهومي فقط", sensitive: "حساس" } as const;
export const INCLUSION_LABEL = { included: "مشمول", excluded: "مستبعد" } as const;
export const REASON_LABEL: Record<string, string> = {
  ok: "مادة تعليمية مناسبة", conceptual_only: "مفاهيم فقط", principles_only: "مبادئ عامة فقط",
  graphic: "وصف صادم", weapon_operational: "تفاصيل تشغيلية للأسلحة", out_of_scope_teens: "لا يناسب الفئة العمرية",
  outside_mission: "خارج رسالة المنصة", front_back_matter: "مقدمات أو فهارس",
};
export type BookConceptView = {
  id: string; book_id: string; section_id: string; section_title_ar: string; ref_ar: string; title_ar: string; summary_ar: string;
  age_band: keyof typeof AGE_LABEL; safety_level: keyof typeof SAFETY_LABEL; skill: Skill;
};
