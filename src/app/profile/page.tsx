"use client";
import { useEffect, useState } from "react";
import { useMe } from "@/components/Shell";
import { SkillCard, type SkillItem } from "@/components/home/SkillCard";
import { LinkButton } from "@/components/ui/button";
import { Callout, EmptyState, ErrorState, LoadingRegion } from "@/components/ui/feedback";
import { ProfileIcon, SearchIcon, TargetIcon } from "@/components/ui/icons";
import { allTokens, api } from "@/lib/client";
import Link from "next/link";

interface Data {
  submitted_cases: number;
  skills: SkillItem[];
  next: {
    ko_id: string;
    name_ar: string;
    kind: "lesson" | "case";
    lesson_id?: string;
    lesson_title_ar: string | null;
  } | null;
}

const DISCLAIMER =
  "هذا تقدير تعليمي مبدئي مبني على قضاياك المنجزة وقواعد معلنة. ليس اختباراً مقنَّناً، ولا يصلح للمفاضلة بين الأشخاص، ولا يغلق عليك شيئاً. كلما أنجزت قضايا أكثر صار التقدير أوضح.";

/* ── Rank helper ─────────────────────────────────────────────── */
function rankFor(submittedCases: number) {
  if (submittedCases >= 8) return { ar: "محقق أول", en: "Lead Detective", icon: "🏆" };
  if (submittedCases >= 5) return { ar: "محقق متقدم", en: "Senior Investigator", icon: "🔎" };
  if (submittedCases >= 3) return { ar: "محقق", en: "Investigator", icon: "🔍" };
  if (submittedCases >= 1) return { ar: "متدرب", en: "Trainee", icon: "📋" };
  return { ar: "مجنّد جديد", en: "Recruit", icon: "🪪" };
}

/* ── Skill meter ─────────────────────────────────────────────── */
function SkillMeter({ value, max = 5 }: { value: number; max?: number }) {
  const pct = Math.min(100, Math.round((value / max) * 100));
  return (
    <div className="skill-meter" aria-hidden>
      <div className="skill-meter-bar" style={{ width: `${pct}%` }} />
    </div>
  );
}

/* ── Profile page ─────────────────────────────────────────────── */
export default function Profile() {
  const { me } = useMe();
  const [d, setD] = useState<Data | null>(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    api<Data>("/profile/data", { tokens: allTokens() })
      .then(setD)
      .catch(() => setFailed(true));
  }, []);

  const rank = d ? rankFor(d.submitted_cases) : null;

  return (
    <>
      {/* ── Profile hero ──────────────────────────────────────── */}
      <header className="profile-hero">
        <div className="profile-hero-avatar" aria-hidden>
          <ProfileIcon size={36} />
        </div>
        <div className="profile-hero-info">
          <p className="profile-hero-kicker">ملف المحقق</p>
          <h1 className="profile-hero-name">
            {me?.user?.display_name ?? "محقق مجهول"}
          </h1>
          {rank && (
            <div className="profile-rank">
              <span className="profile-rank-icon" aria-hidden>{rank.icon}</span>
              <span className="profile-rank-ar">{rank.ar}</span>
              <span className="profile-rank-en">{rank.en}</span>
            </div>
          )}
        </div>
        <Link href="/account" className="profile-account-link" aria-label="إعدادات الحساب">
          <ProfileIcon size={18} />
        </Link>
      </header>

      {/* ── Stats strip ──────────────────────────────────────── */}
      {d && (
        <div className="profile-stats-strip">
          <div className="profile-stat">
            <span className="profile-stat-value">{d.submitted_cases}</span>
            <span className="profile-stat-label">قضية منجزة</span>
          </div>
          <div className="profile-stat-divider" />
          <div className="profile-stat">
            <span className="profile-stat-value">{d.skills.length}</span>
            <span className="profile-stat-label">مهارة مرصودة</span>
          </div>
          <div className="profile-stat-divider" />
          <div className="profile-stat">
            <span className="profile-stat-value">
              {d.skills.filter((s: SkillItem) => s.certainty >= 2).length}
            </span>
            <span className="profile-stat-label">مهارة قوية</span>
          </div>
        </div>
      )}

      {/* ── Investigator question ──────────────────────────────── */}
      <aside className="profile-question-card" aria-label="سؤال المحقق">
        <span className="profile-question-mark">
          <SearchIcon size={16} />
          سؤال المحقق
        </span>
        <p className="profile-question-text">أي عادة تفكير تعمل بصمت في كل قضية تحلّها؟</p>
      </aside>

      {/* ── Content ───────────────────────────────────────────── */}
      {failed ? (
        <ErrorState title="تعذّر تحميل مهاراتك" />
      ) : !d ? (
        <LoadingRegion cards={3} />
      ) : d.submitted_cases === 0 ? (
        <EmptyState
          icon={<TargetIcon size={28} />}
          title="لا مهارات بعد"
          body="أكمل قضية لتظهر مهاراتك هنا. لن نعرض شيئاً لم يحدث فعلاً."
          action={<LinkButton variant="primary" href="/cases">اختر قضية</LinkButton>}
        />
      ) : (
        <>
          <Callout tone="info">{DISCLAIMER}</Callout>

          {/* Next step card */}
          {d.next && (
            <div className="profile-next-card">
              <p className="profile-next-label">اقتراح للخطوة التالية</p>
              <h2 className="profile-next-title">{d.next.name_ar}</h2>
              <p className="small dim-2">
                {d.next.kind === "lesson" && d.next.lesson_title_ar
                  ? `درس قصير يقوّي هذه العادة: «${d.next.lesson_title_ar}».`
                  : "جرّب قضية أخرى تستخدم هذه العادة."}
                {" "}هذا اقتراح فقط ولا يقفل شيئاً.
              </p>
              <LinkButton
                variant="outline"
                size="sm"
                href={
                  d.next.kind === "lesson" && d.next.lesson_id
                    ? `/academy/${d.next.lesson_id}`
                    : "/cases"
                }
                style={{ alignSelf: "flex-start" }}
              >
                {d.next.kind === "lesson" ? "افتح الدرس" : "اختر قضية"}
              </LinkButton>
            </div>
          )}

          {/* Skills section */}
          <div className="profile-skills-header">
            <h2 className="profile-skills-title">المهارات</h2>
            <p className="small dim-2">المهارة تحتاج قضيتين على الأقل قبل أن نقول عنها شيئاً.</p>
          </div>

          <ul className="profile-skills-list list">
            {d.skills.map((s: SkillItem) => (
              <li key={s.ko_id} className="profile-skill-item">
                <SkillMeter value={s.certainty} max={2} />
                <SkillCard s={s} />
              </li>
            ))}
          </ul>
        </>
      )}
    </>
  );
}
