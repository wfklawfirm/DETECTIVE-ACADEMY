import type { Ko } from "./knowledge";

export const TYPE_LABEL: Record<Ko["type"], string> = {
  forensic_concept: "مفهوم من علم الأدلة", reasoning_skill: "مهارة استدلال", narrative_pattern: "نمط لغز",
  case_mechanic: "آلية لعب", character_design_pattern: "نمط شخصية", learning_assessment: "تقييم تعلّم", product_opportunity: "فرصة منتج",
};
export const CONF_LABEL = { high: "ثقة عالية", medium: "ثقة متوسطة", low: "ثقة منخفضة" } as const;
export const STATUS_LABEL = { evidence_based: "مبني على أدلة", design_hypothesis: "فرضية تصميم", expert_practice: "ممارسة مهنية" } as const;
export const RIGHTS_LABEL: Record<string, string> = {
  PUBLIC_DOMAIN: "ملكية عامة", OPEN_LICENSE: "ترخيص مفتوح", LICENSED: "مرخّص", COPYRIGHTED_RESTRICTED: "محمي — يُشار إليه فقط", UNKNOWN: "غير محسوم",
};
