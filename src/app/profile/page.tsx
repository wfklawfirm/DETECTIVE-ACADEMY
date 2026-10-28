"use client";
import { useEffect, useState } from "react";
import { useMe } from "@/components/Shell";
import { SkillCard, type SkillItem } from "@/components/home/SkillCard";
import { LinkButton } from "@/components/ui/button";
import { Card, PageHead, RowLink, SectionTitle } from "@/components/ui/card";
import { Callout, EmptyState, ErrorState, LoadingRegion } from "@/components/ui/feedback";
import { ProfileIcon, SearchIcon, TargetIcon } from "@/components/ui/icons";
import { allTokens, api } from "@/lib/client";

interface Data { submitted_cases: number; skills: SkillItem[]; next: { ko_id: string; name_ar: string; kind: "lesson" | "case"; lesson_id?: string; lesson_title_ar: string | null } | null }
const DISCLAIMER = "هذا تقدير تعليمي مبدئي مبني على قضاياك المنجزة وقواعد معلنة. ليس اختباراً مقنَّناً، ولا يصلح للمفاضلة بين الأشخاص، ولا يغلق عليك شيئاً. كلما أنجزت قضايا أكثر صار التقدير أوضح.";

export default function Profile() {
  const { me } = useMe();
  const [d, setD] = useState<Data | null>(null);
  const [failed, setFailed] = useState(false);
  useEffect(() => { api<Data>("/profile/data", { tokens: allTokens() }).then(setD).catch(() => setFailed(true)); }, []);
  return (
    <>
      <PageHead title="مهاراتي" />
      <aside className="lead-card" aria-label="تلميح">
        <span className="mark"><SearchIcon size={18} />سؤال المحقق</span>
        <p>أي عادة تفكير تعمل بصمت في كل قضية تحلّها؟</p>
      </aside>
      <RowLink href="/account" icon={<ProfileIcon size={22} />} title={me?.user ? (me.user.display_name ?? "حسابي") : "الحساب وتسجيل الدخول"} hint={me?.user ? "إعدادات الحساب" : "اختياري: لحفظ تقدّمك خارج هذا الجهاز"} />
      {failed ? <ErrorState title="تعذّر تحميل مهاراتك" /> : !d ? <LoadingRegion cards={3} /> : d.submitted_cases === 0 ? (
        <EmptyState icon={<TargetIcon size={28} />} title="لا مهارات بعد" body="أكمل قضية لتظهر مهاراتك هنا. لن نعرض شيئاً لم يحدث فعلاً." action={<LinkButton variant="primary" href="/cases">اختر قضية</LinkButton>} />
      ) : (
        <>
          <Callout tone="info">{DISCLAIMER}</Callout>
          {d.next && (
            <Card as="section" aria-labelledby="nx-h" raised>
              <p className="text-label">اقتراح للخطوة التالية</p>
              <h2 id="nx-h" className="card-title">{d.next.name_ar}</h2>
              <p className="small dim-2">{d.next.kind === "lesson" && d.next.lesson_title_ar ? `درس قصير يقوّي هذه العادة: «${d.next.lesson_title_ar}».` : "جرّب قضية أخرى تستخدم هذه العادة."} هذا اقتراح فقط ولا يقفل شيئاً.</p>
              <LinkButton variant="outline" size="sm" href={d.next.kind === "lesson" && d.next.lesson_id ? `/academy/${d.next.lesson_id}` : "/cases"} style={{ alignSelf: "flex-start" }}>{d.next.kind === "lesson" ? "افتح الدرس" : "اختر قضية"}</LinkButton>
            </Card>
          )}
          <SectionTitle>المهارات</SectionTitle>
          <p className="small dim-2">المهارة تحتاج قضيتين على الأقل قبل أن نقول عنها شيئاً.</p>
          <ul className="list">{d.skills.map((s) => <li key={s.ko_id}><SkillCard s={s} /></li>)}</ul>
        </>
      )}
    </>
  );
}
