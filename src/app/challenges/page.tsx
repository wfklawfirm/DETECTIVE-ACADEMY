"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { api, deviceSeed } from "@/lib/client";

interface Riddle { id: string; title_ar: string; prompt_ar: string; options: { id: string; text_ar: string }[] }
export default function Challenges() {
  const [r, setR] = useState<Riddle | null>(null);
  const [res, setRes] = useState<{ correct: boolean; answer_id: string; explanation_ar: string } | null>(null);
  const [sel, setSel] = useState<string | null>(null);
  useEffect(() => { void api<{ riddle: Riddle }>(`/api/riddle?seed=${encodeURIComponent(deviceSeed())}`).then((x) => setR(x.riddle)); }, []);
  const pick = async (id: string) => { if (!r || sel) return; setSel(id); setRes(await api("/api/riddle", { riddle_id: r.id, option_id: id })); };
  return (
    <div className="wrap-narrow stack">
      <h1>تحدي اليوم</h1>
      <p className="dim">لغز قصير من تأليفنا، جديد كل يوم. لا نقاط ولا سلاسل؛ فقط متعة التفكير.</p>
      {!r ? <p className="dim">جارٍ التحميل…</p> : (
        <section className="card stack" aria-labelledby="rd">
          <h2 id="rd">{r.title_ar}</h2><p>{r.prompt_ar}</p>
          {r.options.map((o) => <button key={o.id} className="btn" disabled={!!sel} style={{ justifyContent: "flex-start", textAlign: "start", borderColor: res && o.id === res.answer_id ? "var(--green)" : sel === o.id && res && !res.correct ? "var(--rose)" : undefined }} onClick={() => pick(o.id)}>{o.text_ar}</button>)}
          {res && <div role="status"><p className={res.correct ? "ok" : "err"}>{res.correct ? "أحسنت." : "ليست الإجابة الأدق."}</p><p>{res.explanation_ar}</p></div>}
        </section>
      )}
      <p><Link href="/academy">تعلّم المهارة خلف اللغز في الأكاديمية ←</Link></p>
    </div>
  );
}
