"use client";
import { useEffect, useState } from "react";
import { useMe } from "@/components/Shell";
import { MasteryMeter, Badge } from "@/components/ui/badge";
import { LinkButton } from "@/components/ui/button";
import { Card, PageHead, RowLink, SectionTitle } from "@/components/ui/card";
import { Callout, EmptyState, ErrorState, LoadingRegion } from "@/components/ui/feedback";
import { ProfileIcon, TargetIcon } from "@/components/ui/icons";
import { allTokens, api } from "@/lib/client";

interface Row { ko_id: string; name_ar: string; level: number; cases: string[]; track: string | null }
const LV = ["لم يظهر بعد", "بداية", "ناشئ", "متمكّن", "متقدّم"];
export default function Profile() {
  const { me } = useMe();
  const [d, setD] = useState<{ skills: Row[]; disclaimer_ar: string; submitted_cases: number } | null>(null);
  const [failed, setFailed] = useState(false);
  useEffect(() => { api<typeof d>("/api/profile", { tokens: allTokens() }).then(setD).catch(() => setFailed(true)); }, []);
  return (
    <>
      <PageHead title="مهاراتي" />
      <RowLink href="/account" icon={<ProfileIcon size={22} />} title={me?.user ? (me.user.display_name ?? "حسابي") : "الحساب وتسجيل الدخول"} hint={me?.user ? "إعدادات الحساب" : "اختياري: لحفظ تقدّمك خارج هذا الجهاز"} />
      {failed ? <ErrorState title="تعذّر تحميل مهاراتك" /> : !d ? <LoadingRegion cards={3} /> : d.submitted_cases === 0 ? (
        <EmptyState icon={<TargetIcon size={28} />} title="لا مهارات بعد" body="أكمل قضية لتظهر مهاراتك هنا." action={<LinkButton variant="primary" href="/cases">اختر قضية</LinkButton>} />
      ) : (
        <>
          <Callout tone="info">{d.disclaimer_ar}</Callout>
          <SectionTitle>المهارات</SectionTitle>
          <ul className="list">
            {d.skills.map((s) => (
              <li key={s.ko_id}><Card flat>
                <div className="row row-between"><b>{s.name_ar}</b>{s.track && <Badge>مسار {s.track}</Badge>}</div>
                <MasteryMeter level={s.level} max={4} label={LV[s.level]} a11yLabel={`${LV[s.level]}، ${s.level} من 4`} />
                <p className="small dim">من: {s.cases.join("، ")}</p>
              </Card></li>
            ))}
          </ul>
        </>
      )}
    </>
  );
}
