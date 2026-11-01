"use client";
import { useEffect, useState } from "react";
import { Button, LinkButton } from "@/components/ui/button";
import { StepDots } from "@/components/ui/progress";
import { allTokens, api } from "@/lib/client";

const LINES = [
  "وصلتك رسالة بلا اسم مرسل:",
  "«دفتر التجربة اختفى. الجميع يقول إن هادي أخذه. السجلات تقول شيئاً آخر. تحقق قبل أن تحكم.»",
  "لا أحد سيخبرك بالنتيجة. لديك ملف، وسجلات، وبضعة شهود.",
];

export default function Start() {
  const [n, setN] = useState(1);
  const [returning, setReturning] = useState<boolean | null>(null);

  // Detect whether user already has progress
  useEffect(() => {
    api<{ cards: unknown[]; cases: { case_id: string; done: boolean }[] }>("/api/progress", { tokens: allTokens() })
      .then((d) => {
        const hasProgress = d.cases.length > 0;
        setReturning(hasProgress);
      })
      .catch(() => setReturning(false));
  }, []);

  // While checking — show nothing yet (avoids flash)
  if (returning === null) return null;

  // Returning user — skip the cold open and send to home
  if (returning) {
    return (
      <section className="start-screen" aria-label="مرحباً بعودتك">
        <div className="start-topbar">
          <span className="start-stamp">أكاديمية المحقق · مركز العمليات</span>
        </div>
        <div className="start-cold-open">
          <p className="start-line start-line--new">مرحباً بعودتك.</p>
          <p className="start-line">تحقيقاتك في انتظارك.</p>
        </div>
        <div className="start-cta">
          <LinkButton variant="primary" size="lg" block href="/home">
            إلى مركز العمليات ←
          </LinkButton>
          <LinkButton variant="secondary" size="lg" block href="/cases">
            كل القضايا
          </LinkButton>
        </div>
      </section>
    );
  }

  // New user — show cold-open sequence
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
