"use client";
import { useEffect, useState } from "react";
import { LinkButton } from "@/components/ui/button";
import { Card, PageHead } from "@/components/ui/card";
import { Callout, ErrorState, LoadingRegion } from "@/components/ui/feedback";
import { ChoiceGroup } from "@/components/ui/form";
import { api, deviceSeed } from "@/lib/client";

interface Riddle { id: string; title_ar: string; prompt_ar: string; options: { id: string; text_ar: string }[] }
export default function Challenges() {
  const [r, setR] = useState<Riddle | null>(null);
  const [failed, setFailed] = useState(false);
  const [res, setRes] = useState<{ correct: boolean; answer_id: string; explanation_ar: string } | null>(null);
  const [sel, setSel] = useState<string | null>(null);
  useEffect(() => { api<{ riddle: Riddle }>(`/api/riddle?seed=${encodeURIComponent(deviceSeed())}`).then((x) => setR(x.riddle)).catch(() => setFailed(true)); }, []);
  const pick = async (id: string) => { if (!r || sel) return; setSel(id); setRes(await api("/api/riddle", { riddle_id: r.id, option_id: id })); };
  const states: Record<string, "correct" | "wrong"> | undefined = res ? { [res.answer_id]: "correct", ...(sel && sel !== res.answer_id ? { [sel]: "wrong" as const } : {}) } : undefined;
  return (
    <>
      <PageHead title="تحدي اليوم" lead="لغز قصير من تأليفنا، جديد كل يوم. لا نقاط ولا سلاسل؛ فقط متعة التفكير." />
      {failed ? <ErrorState title="تعذّر تحميل اللغز" /> : !r ? <LoadingRegion cards={1} /> : (
        <Card as="section" aria-labelledby="rd" className="lantern" raised>
          <h2 id="rd" className="text-section-title">{r.title_ar}</h2><p id="rd-q">{r.prompt_ar}</p>
          <ChoiceGroup labelledBy="rd-q" name="riddle" value={sel} disabled={!!sel} states={states} onChange={pick} options={r.options.map((o) => ({ value: o.id, label: o.text_ar }))} />
          {res && <div role="status" className="stack-sm"><Callout tone={res.correct ? "positive" : "negative"}>{res.correct ? "أحسنت." : "ليست الإجابة الأدق."}</Callout><p>{res.explanation_ar}</p></div>}
        </Card>
      )}
      <LinkButton variant="outline" block href="/academy">تعلّم المهارة خلف اللغز في الأكاديمية</LinkButton>
    </>
  );
}
