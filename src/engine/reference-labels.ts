// Client-safe labels and constants for the reference pages (no node:fs here).

export type MethodTier = "strong" | "conditional" | "open" | "unsupported" | "process" | "analogue";
export type GlossaryStatus = "sourced" | "variant" | "proposed";
export type Tone = "neutral" | "brand" | "positive" | "negative" | "warning" | "info";

export const TIER_LABEL: Record<MethodTier, string> = {
  strong: "أساس علمي راسخ نسبياً",
  conditional: "مقبول بشروط وحدود",
  open: "غير محسوم أو فجواته كبيرة",
  unsupported: "غير مدعوم علمياً لهذا الاستعمال",
  process: "إجراء أو ضمان جودة",
  analogue: "مثال تعليمي خيالي",
};
export const TIER_TONE: Record<MethodTier, Tone> = { strong: "positive", conditional: "info", open: "warning", unsupported: "negative", process: "neutral", analogue: "brand" };
/** Order for the validity "ladder" shown at the top of /methods. */
export const TIER_ORDER: MethodTier[] = ["strong", "conditional", "open", "unsupported", "process", "analogue"];

export const LEVEL_LABEL: Record<string, string> = { "13-15": "مستوى 13–15", "16-18": "مستوى 16–18", "18+": "للبالغين (18+)" };
export const GLOSSARY_STATUS_LABEL: Record<GlossaryStatus, string> = {
  sourced: "مصطلح موثّق في مصدر معتمد",
  variant: "موثّق مع صيغ بديلة",
  proposed: "مصطلح مقترح من فريق أثر ولم يُعتمد من جهة رسمية",
};
export const GLOSSARY_STATUS_TONE: Record<GlossaryStatus, Tone> = { sourced: "positive", variant: "info", proposed: "warning" };

export const VIOLENCE_LABEL: Record<string, string> = { V0: "بلا جريمة ضد أشخاص", V1: "مخالفة غير عنيفة", V2: "وفاة خارج الشاشة (16 فما فوق)", V3: "للبالغين فقط" };
export const AGE_BAND_LABEL: Record<string, string> = { "13-15": "13–15 سنة", "16-18": "16–18 سنة", "18+": "18 سنة فما فوق" };

export const PATTERN_AGE_TONE: Record<string, Tone> = { "مناسب": "positive", "بشروط": "warning", "غير مناسب": "negative" };

/** Honest provenance line used on every reference page. */
export const UNREVIEWED_NOTE = "صياغة أولية من مكتبة أثر البحثية بمساعدة الذكاء الاصطناعي. لم يراجعها خبير مستقل بعد، ولم تُختبر مع طلاب، فاعتبرها مادة تعليمية أولية لا مرجعاً علمياً نهائياً.";

export const REFERENCE_PAGES = [
  { href: "/glossary", title: "المسرد الجنائي", hint: "248 مصطلحاً عربياً بتعريفات مختصرة" },
  { href: "/methods", title: "طرق الفحص وحدودها", hint: "ما تستطيع كل طريقة أن تثبته وما لا تستطيع" },
  { href: "/biases", title: "فخاخ العقل", hint: "التحيزات المعرفية بمثال قصير" },
  { href: "/reasoning", title: "أخطاء الاستدلال وقواعد الدليل", hint: "قائمة تقييم الدليل ومبادئ التحقيق الأخلاقي" },
  { href: "/rulebook", title: "دستور اللغز العادل", hint: "قواعد العدالة وكيف تعمل التلميحات" },
  { href: "/atlas", title: "أطلس الأدب البوليسي", hint: "مبادئ وتراث وأنماط حبكة" },
  { href: "/archetypes", title: "أنماط الألغاز", hint: "40 قالباً وما بُني منها" },
] as const;
