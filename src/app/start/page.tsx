"use client";
import Link from "next/link";
import { useState } from "react";

const LINES = [
  "وصلتك رسالة بلا اسم مرسل:",
  "«دفتر التجربة اختفى. الجميع يقول إن هادي أخذه. السجلات تقول شيئاً آخر. تحقق قبل أن تحكم.»",
  "لا أحد سيخبرك بالنتيجة. لديك ملف، وسجلات، وبضعة شهود.",
];
export default function Start() {
  const [n, setN] = useState(1);
  return (
    <div className="wrap-narrow stack" style={{ paddingBlockStart: 32 }}>
      <p className="kicker">رسالة مجهولة · ٠٣:١٢</p>
      <div className="cold-open" aria-live="polite">
        {LINES.slice(0, n).map((l, i) => <p key={i} style={{ animationDelay: "0s", opacity: 1 }}>{l}</p>)}
      </div>
      {n < LINES.length ? (
        <button className="btn" onClick={() => setN(n + 1)}>التالي</button>
      ) : (
        <div className="stack">
          <Link className="btn primary" href="/play/c000_lost_notebook">افتح الملف</Link>
          <p className="small dim">لا حاجة إلى حساب الآن. تقدّمك يُحفظ على جهازك، ويمكنك إنشاء حساب بعد أن ترى النتيجة.</p>
        </div>
      )}
    </div>
  );
}
