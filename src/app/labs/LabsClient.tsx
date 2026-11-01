"use client";
import { useState } from "react";
import type { LabKind } from "@/engine/labs";
import { KIND_LABEL } from "@/engine/lab-labels";
import { Badge } from "@/components/ui/badge";
import { CardLink } from "@/components/ui/card";
import { ChevronIcon } from "@/components/ui/icons";
import { LabProgressOverlay } from "@/components/labs/LabProgressOverlay";

type Item = {
  id: string;
  title_ar: string;
  skill_ar: string;
  interaction_ar: string;
  difficulty: number;
  minutes: number;
};

type Group = {
  kind: LabKind;
  label: string;
  items: Item[];
};

type DiffFilter = "all" | "1" | "2" | "3";

export function LabsClient({
  groups,
  allIds,
  difficultyLabel,
}: {
  groups: Group[];
  allIds: string[];
  difficultyLabel: Record<number, string>;
}) {
  const [kindFilter, setKindFilter] = useState<"all" | LabKind>("all");
  const [diffFilter, setDiffFilter] = useState<DiffFilter>("all");
  const [doneCount, setDoneCount] = useState<number>(0);

  const kinds = Object.keys(KIND_LABEL) as LabKind[];

  const visibleGroups = groups
    .filter((g) => kindFilter === "all" || g.kind === kindFilter)
    .map((g) => ({
      ...g,
      items: g.items.filter((i) => diffFilter === "all" || String(i.difficulty) === diffFilter),
    }))
    .filter((g) => g.items.length > 0);

  const totalVisible = visibleGroups.reduce((s, g) => s + g.items.length, 0);

  return (
    <>
      {/* Progress overlay — injects CSS for done chips */}
      <LabProgressOverlay
        labIds={allIds}
        onStats={(done) => setDoneCount(done)}
      />

      {/* Progress summary strip — visible once progress is known */}
      {doneCount > 0 && (
        <div className="labs-progress-strip" role="status" aria-label={`أكملت ${doneCount} من ${allIds.length} تمريناً`}>
          <span className="labs-progress-text">
            أكملت <b>{doneCount}</b> من <b>{allIds.length}</b> تمريناً
          </span>
          <div className="labs-progress-bar-wrap" aria-hidden>
            <div
              className="labs-progress-bar-fill"
              style={{ width: `${Math.round((doneCount / allIds.length) * 100)}%` }}
            />
          </div>
          <span className="labs-progress-pct small dim" aria-hidden>
            {Math.round((doneCount / allIds.length) * 100)}٪
          </span>
        </div>
      )}

      {/* Filter controls */}
      <div className="labs-controls" role="toolbar" aria-label="فلاتر المختبرات">
        <div className="labs-filter-row">
          <span className="labs-filter-label">النوع:</span>
          <button
            className={`filter-btn${kindFilter === "all" ? " filter-btn--active" : ""}`}
            onClick={() => setKindFilter("all")}
          >الكل</button>
          {kinds.map((k) => (
            <button
              key={k}
              className={`filter-btn${kindFilter === k ? " filter-btn--active" : ""}`}
              onClick={() => setKindFilter(k)}
            >{KIND_LABEL[k]}</button>
          ))}
        </div>
        <div className="labs-filter-row">
          <span className="labs-filter-label">الصعوبة:</span>
          {(["all", "1", "2", "3"] as DiffFilter[]).map((d) => (
            <button
              key={d}
              className={`filter-btn${diffFilter === d ? " filter-btn--active" : ""}`}
              onClick={() => setDiffFilter(d)}
            >{d === "all" ? "الكل" : difficultyLabel[Number(d)] ?? d}</button>
          ))}
        </div>
        {(kindFilter !== "all" || diffFilter !== "all") && (
          <p className="labs-result-count small dim" role="status" aria-live="polite">
            {totalVisible} تمرين مطابق
          </p>
        )}
      </div>

      {/* Groups */}
      {visibleGroups.map((g) => (
        <section key={g.kind} className="stack" aria-labelledby={`k-${g.kind}`}>
          <h2 id={`k-${g.kind}`} className="text-section-title">
            {g.label} <span className="small dim">({g.items.length})</span>
          </h2>
          <ul className="list">
            {g.items.map((item) => (
              <li key={item.id}>
                <div data-lab-id={item.id}>
                  <CardLink href={`/labs/${item.id}`}>
                    <div className="row" style={{ flexWrap: "nowrap" }}>
                      <b className="grow">{item.title_ar}</b>
                      <span className="lab-done-chip" style={{ display: "none" }}>
                        <Badge tone="positive">✓ مكتمل</Badge>
                      </span>
                      <ChevronIcon className="chev" size={20} />
                    </div>
                    <span className="small dim">المهارة: {item.skill_ar} · {item.interaction_ar}</span>
                    <span className="row small">
                      <Badge outline>{difficultyLabel[item.difficulty]}</Badge>
                      <Badge outline>نحو {item.minutes} د</Badge>
                      <Badge tone="warning">يتطلب مراجعة خبراء</Badge>
                    </span>
                  </CardLink>
                </div>
              </li>
            ))}
          </ul>
        </section>
      ))}

      {visibleGroups.length === 0 && (
        <p className="small dim" style={{ textAlign: "center", padding: "2rem 0" }} role="status">
          لا توجد مختبرات تطابق هذه الفلاتر
        </p>
      )}
    </>
  );
}
