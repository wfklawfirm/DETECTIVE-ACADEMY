"use client";
import { useState } from "react";
import { Button, LinkButton } from "@/components/ui/button";
import { StepDots } from "@/components/ui/progress";

const LINES = [
  "وصلتك رسالة بلا اسم مرسل:",
  "«دفتر التجربة اختفى. الجميع يقول إن هادي أخذه. السجلات تقول شيئاً آخر. تحقق قبل أن تحكم.»",
  "لا أحد سيخبرك بالنتيجة. لديك ملف، وسجلات، وبضعة شهود.",
];

export default function Start() {
  const [n, setN] = useState(1);

  return (
    <section className="start-screen" aria-label="مشهد الافتتاح">
      {/* Top bar */}
      <div className="start-topbar">
        <span className="start-stamp">رسالة مجهولة · ٠٣:١٢</span>
        <StepDots total={LINES.length} current={n - 1} label={`الخطوة ${n} من ${LINES.length}`} />
      </div>

      {/* Cold open */}
      <div className="start-cold-open" aria-live="polite">
        {LINES.slice(0, n).map((l, i) => (
          <p key={i} className={`start-line${i === n - 1 ? " start-line--new" : ""}`}>{l}</p>
        ))}
      </div>

      {/* CTA */}
      <div className="start-cta">
        {n < LINES.length ? (
          <Button variant="secondary" size="lg" block onClick={() => setN(n + 1)}>
            التالي
          </Button>
        ) : (
          <>
            <LinkButton variant="primary" size="lg" block href="/play/c000_lost_notebook">
              افتح الملف
            </LinkButton>
            <p className="start-note">
              لا حاجة إلى حساب الآن. تقدّمك يُحفظ على جهازك، ويمكنك إنشاء حساب بعد أن ترى النتيجة.
            </p>
          </>
        )}
      </div>
    </section>
  );
}
