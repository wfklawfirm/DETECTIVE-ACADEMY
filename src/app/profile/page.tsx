"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { useMe } from "@/components/Shell";
import { SkillCard, type SkillItem } from "@/components/home/SkillCard";
import { LinkButton } from "@/components/ui/button";
import { EmptyState, ErrorState, LoadingRegion } from "@/components/ui/feedback";
import { ProfileIcon, SearchIcon, TargetIcon } from "@/components/ui/icons";
import { allTokens, api } from "@/lib/client";

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
  "هذا تقدير تعليمي مبدئي مبني على قضاياك المنجزة وقواعد معلنة. ليس اختباراً مقنَّناً، ولا يصلح للمفاضلة، ولا يغلق عليك شيئاً.";

/* ── Rank ────────────────────────────────────────────────────── */
function rankFor(n: number) {
  if (n >= 8) return { ar: "محقق أول",    en: "Lead Detective",      icon: "🏆", level: 5 };
  if (n >= 5) return { ar: "محقق متقدم", en: "Senior Investigator",  icon: "🔎", level: 4 };
  if (n >= 3) return { ar: "محقق",        en: "Investigator",         icon: "🔍", level: 3 };
  if (n >= 1) return { ar: "متدرب",       en: "Trainee",              icon: "📋", level: 2 };
  return         { ar: "مجنّد جديد",   en: "Recruit",              icon: "🪪", level: 1 };
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

/* ── Rank bar (5 pips) ───────────────────────────────────────── */
function RankPips({ level }: { level: number }) {
  return (
    <div className="rank-pips" aria-hidden>
      {Array.from({ length: 5 }, (_, i) => (
        <span key={i} className={`rank-pip${i < level ? " rank-pip--active" : ""}`} />
      ))}
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
      {/* ── Cinematic hero ───────────────────────────────────── */}
      <header className="profile-hero">
        <div className="profile-hero-inner">
          <div className="profile-hero-avatar" aria-hidden>
            <ProfileIcon size={32} />
          </div>
          <div className="profile-hero-info">
            <p className="profile-hero-kicker">ملف المحقق</p>
            <h1 className="profile-hero-name">
              {me?.user?.display_name ?? "محقق مجهول"}
            </h1>
            {rank && (
              <div className="profile-rank-row">
                <span className="profile-rank-icon" aria-hidden>{rank.icon}</span>
                <span className="profile-rank-ar">{rank.ar}</span>
                <span className="profile-rank-en">{rank.en}</span>
                <RankPips level={rank.level} />
              </div>
            )}
          </div>
          <Link href="/account" className="profile-account-btn" aria-label="إعدادات الحساب">
            <ProfileIcon size={16} />
          </Link>
        </div>

        {/* Stats strip */}
        {d && (
          <div className="profile-stats-strip">
            <div className="profile-stat">
              <span className="profile-stat-value">{d.submitted_cases}</span>
              <span className="profile-stat-label">قضية منجزة</span>
            </div>
            <div className="profile-stat-sep" />
            <div className="profile-stat">
              <span className="profile-stat-value">{d.skills.length}</span>
              <span className="profile-stat-label">مهارة مرصودة</span>
            </div>
            <div className="profile-stat-sep" />
            <div className="profile-stat">
              <span className="profile-stat-value profile-stat-value--strong">
                {d.skills.filter((s: SkillItem) => s.certainty >= 2).length}
              </span>
              <span className="profile-stat-label">مهارة قوية</span>
            </div>
          </div>
        )}
      </header>

      {/* ── Investigator question ─────────────────────────────── */}
      <aside className="profile-question-card" aria-label="سؤال المحقق">
        <span className="profile-question-mark">
          <SearchIcon size={14} />
          سؤال المحقق
        </span>
        <p className="profile-question-text">
          أي عادة تفكير تعمل بصمت في كل قضية تحلّها؟
        </p>
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
          body="أكمل قضية لتظهر مهاراتك هنا."
          action={<LinkButton variant="primary" href="/cases">اختر قضية</LinkButton>}
        />
      ) : (
        <>
          {/* Disclaimer strip */}
          <div className="profile-disclaimer">
            <span className="profile-disclaimer-icon" aria-hidden>ℹ️</span>
            <p>{DISCLAIMER}</p>
          </div>

          {/* Next step card */}
          {d.next && (
            <div className="profile-next-card">
              <p className="profile-next-kicker">اقتراح · الخطوة التالية</p>
              <h2 className="profile-next-title">{d.next.name_ar}</h2>
              <p className="profile-next-body">
                {d.next.kind === "lesson" && d.next.lesson_title_ar
                  ? `درس قصير يقوّي هذه العادة: «${d.next.lesson_title_ar}».`
                  : "جرّب قضية أخرى تستخدم هذه العادة."}
                {" "}هذا اقتراح فقط ولا يقفل شيئاً.
              </p>
              <LinkButton
                variant="primary"
                size="sm"
                href={
                  d.next.kind === "lesson" && d.next.lesson_id
                    ? `/academy/${d.next.lesson_id}`
                    : "/cases"
                }
              >
                {d.next.kind === "lesson" ? "افتح الدرس ←" : "اختر قضية ←"}
              </LinkButton>
            </div>
          )}

          {/* Skills section */}
          <section aria-labelledby="skills-h">
            <div className="profile-skills-header">
              <h2 id="skills-h" className="profile-skills-title">خريطة المهارات</h2>
              <p className="profile-skills-note">المهارة تحتاج قضيتين على الأقل قبل أن نقول عنها شيئاً.</p>
            </div>
            <ul className="profile-skills-list list">
              {d.skills.map((s: SkillItem) => (
                <li key={s.ko_id} className="profile-skill-item">
                  <SkillMeter value={s.certainty} max={2} />
                  <SkillCard s={s} />
                </li>
              ))}
            </ul>
          </section>
        </>
      )}
    </>
  );
}
