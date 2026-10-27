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
    <section className="lantern stack-lg" style={{ padding: "1.5rem 1rem", minBlockSize: "70dvh", justifyContent: "space-between" }}>
      <div className="stack-lg">
        <div className="row row-between"><span className="stamp">رسالة مجهولة · ٠٣:١٢</span><StepDots total={LINES.length} current={n - 1} label={`الخطوة ${n} من ${LINES.length}`} /></div>
        <div className="cold-open" aria-live="polite">
          {LINES.slice(0, n).map((l, i) => <p key={i} className="reveal">{l}</p>)}
        </div>
      </div>
      {n < LINES.length ? (
        <Button variant="secondary" size="lg" block onClick={() => setN(n + 1)}>التالي</Button>
      ) : (
        <div className="stack">
          <LinkButton variant="primary" size="lg" block href="/play/c000_lost_notebook">افتح الملف</LinkButton>
          <p className="small dim">لا حاجة إلى حساب الآن. تقدّمك يُحفظ على جهازك، ويمكنك إنشاء حساب بعد أن ترى النتيجة.</p>
        </div>
      )}
    </section>
  );
}
