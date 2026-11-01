"use client";
import { useEffect, useState } from "react";
import { useMe } from "@/components/Shell";
import { LinkButton } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { EmptyState, LoadingRegion } from "@/components/ui/feedback";
import { StudioIcon } from "@/components/ui/icons";
import { api } from "@/lib/client";

interface Stats {
  users: { total: number; today: number };
  cases: { total: number; published: number; in_review: number; draft: number };
  plays: { total: number; completed: number };
  lessons_done: number;
}

function Stat({ value, label, sub }: { value: number | string; label: string; sub?: string }) {
  return (
    <div className="studio-stat">
      <span className="studio-stat-value">{value}</span>
      <span className="studio-stat-label">{label}</span>
      {sub && <span className="studio-stat-sub">{sub}</span>}
    </div>
  );
}

export default function StudioStats() {
  const { me } = useMe();
  const [s, setS] = useState<Stats | null>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    if (me?.user?.role !== "admin") return;
    api<Stats>("/api/studio/stats")
      .then(setS)
      .catch(() => setErr("تعذّر تحميل الإحصاءات"));
  }, [me]);

  if (!me?.user || me.user.role !== "admin") {
    return (
      <>
        <div className="ref-hero"><p className="ref-hero-kicker">الاستوديو</p><h1 className="ref-hero-title">إحصاءات الاستوديو</h1></div>
        <EmptyState icon={<StudioIcon size={28} />} title="للمدير فقط" action={<LinkButton variant="primary" href="/studio">عودة للاستوديو</LinkButton>} />
      </>
    );
  }

  return (
    <>
      <div className="ref-hero">
        <p className="ref-hero-kicker">الاستوديو · المدير</p>
        <h1 className="ref-hero-title">إحصاءات المنصة</h1>
        <div className="ref-hero-actions"><LinkButton variant="ghost" href="/studio">← الاستوديو</LinkButton></div>
      </div>

      {err && <p className="callout" data-tone="negative">{err}</p>}
      {!s && !err && <LoadingRegion cards={4} />}

      {s && (
        <div className="stack">
          {/* Users */}
          <Card as="section">
            <h2 className="card-title">المستخدمون</h2>
            <div className="studio-stats-strip">
              <Stat value={s.users.total} label="إجمالي الحسابات" />
              <Stat value={s.users.today} label="مسجّل اليوم" />
            </div>
          </Card>

          {/* Cases */}
          <Card as="section">
            <h2 className="card-title">القضايا</h2>
            <div className="studio-stats-strip">
              <Stat value={s.cases.total} label="إجمالي النسخ" />
              <Stat value={s.cases.published} label="منشورة" sub="✓" />
              <Stat value={s.cases.in_review} label="قيد المراجعة" />
              <Stat value={s.cases.draft} label="مسودة" />
            </div>
          </Card>

          {/* Engagement */}
          <Card as="section">
            <h2 className="card-title">الاستخدام</h2>
            <div className="studio-stats-strip">
              <Stat value={s.plays.total} label="جلسة لعب" />
              <Stat
                value={s.plays.total > 0 ? `${Math.round((s.plays.completed / s.plays.total) * 100)}%` : "—"}
                label="معدل الإكمال"
              />
              <Stat value={s.lessons_done} label="درس مكتمل" />
            </div>
          </Card>
        </div>
      )}
    </>
  );
}
