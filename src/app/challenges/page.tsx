"use client";
import { useEffect, useState } from "react";
import { LinkButton } from "@/components/ui/button";
import { ErrorState, LoadingRegion } from "@/components/ui/feedback";
import { ChoiceGroup } from "@/components/ui/form";
import { api, deviceSeed } from "@/lib/client";

interface Riddle {
  id: string;
  title_ar: string;
  prompt_ar: string;
  options: { id: string; text_ar: string }[];
}

export default function Challenges() {
  const [r, setR]         = useState<Riddle | null>(null);
  const [failed, setFailed] = useState(false);
  const [res, setRes]     = useState<{ correct: boolean; answer_id: string; explanation_ar: string } | null>(null);
  const [sel, setSel]     = useState<string | null>(null);

  useEffect(() => {
    api<{ riddle: Riddle }>(`/api/riddle?seed=${encodeURIComponent(deviceSeed())}`)
      .then((x) => setR(x.riddle))
      .catch(() => setFailed(true));
  }, []);

  const pick = async (id: string) => {
    if (!r || sel) return;
    setSel(id);
    setRes(await api("/api/riddle", { riddle_id: r.id, option_id: id }));
  };

  const states: Record<string, "correct" | "wrong"> | undefined = res
    ? { [res.answer_id]: "correct", ...(sel && sel !== res.answer_id ? { [sel]: "wrong" as const } : {}) }
    : undefined;

  return (
    <>
      {/* ── Cinematic hero ─────────────────────────────────────── */}
      <header className="challenges-hero">
        <div className="challenges-hero-inner">
          <div className="challenges-hero-text">
            <p className="challenges-hero-kicker">تحدي يومي · لغز من تأليفنا</p>
            <h1 className="challenges-hero-title">تحدي اليوم</h1>
            <p className="challenges-hero-sub">
              لا نقاط ولا سلاسل؛ فقط متعة التفكير.
            </p>
          </div>
          <div className="challenges-hero-badge" aria-hidden>
            <span className="challenges-hero-glyph">🧩</span>
          </div>
        </div>
      </header>

      {/* ── States ─────────────────────────────────────────────── */}
      {failed && <ErrorState title="تعذّر تحميل اللغز" />}
      {!failed && !r && <LoadingRegion cards={1} />}

      {/* ── Riddle card ─────────────────────────────────────────── */}
      {!failed && r && (
        <section className="riddle-card" aria-labelledby="rd-title">
          <div className="riddle-card-header">
            <span className="riddle-card-num" aria-hidden>؟</span>
            <h2 id="rd-title" className="riddle-card-title">{r.title_ar}</h2>
          </div>
          <p id="rd-prompt" className="riddle-card-prompt">{r.prompt_ar}</p>

          <ChoiceGroup
            labelledBy="rd-prompt"
            name="riddle"
            value={sel}
            disabled={!!sel}
            states={states}
            onChange={pick}
            options={r.options.map((o) => ({ value: o.id, label: o.text_ar }))}
          />

          {res && (
            <div role="status" className="riddle-result">
              <div className={`riddle-result-verdict riddle-result-verdict--${res.correct ? "correct" : "wrong"}`}>
                {res.correct ? "✓ أحسنت — إجابة دقيقة" : "✗ ليست الإجابة الأدق"}
              </div>
              <p className="riddle-result-explanation">{res.explanation_ar}</p>
            </div>
          )}
        </section>
      )}

      {/* ── Academy link ────────────────────────────────────────── */}
      <div className="challenges-footer">
        <p className="challenges-footer-text">هل أثار اللغز فضولك؟</p>
        <LinkButton variant="outline" href="/academy">
          تعلّم المهارة خلف اللغز في الأكاديمية ←
        </LinkButton>
      </div>
    </>
  );
}
