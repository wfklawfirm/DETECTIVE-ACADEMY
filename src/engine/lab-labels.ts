/** Client-safe lab labels. No node:* imports here: client components must import from this file, never from ./labs. */
export type LabKind = "classify" | "order" | "match" | "slider" | "spot" | "measure" | "conclude";
export const KIND_LABEL: Record<LabKind, string> = {
  classify: "صنّف في خانات", order: "رتّب الخطوات", match: "طابق الأزواج", slider: "نموذج بمنزلقات", spot: "اكتشف الخلل في وثيقة", measure: "قِس واحسب", conclude: "اختر الاستنتاج المسوَّغ",
};
