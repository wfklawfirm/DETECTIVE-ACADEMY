import Link from "next/link";
import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { Badge } from "@/components/ui/badge";
import { Callout } from "@/components/ui/feedback";
import { Card, PageHead } from "@/components/ui/card";
import { RIGHTS_LABEL, dirFor, excerptsFor, loadHeritage, safeUrl, showable } from "@/engine/heritage";

export const dynamicParams = false;
export function generateStaticParams() { return loadHeritage().texts.map((t) => ({ id: t.id })); }
export async function generateMetadata({ params }: { params: Promise<{ id: string }> }): Promise<Metadata> {
  const { id } = await params; const t = loadHeritage().texts.find((x) => x.id === id);
  return { title: t ? `${t.title_ar} · مكتبة التراث` : "مكتبة التراث" };
}

export default async function HeritageText({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const { texts, excerpts } = loadHeritage();
  const t = texts.find((x) => x.id === id);
  if (!t) notFound();
  const ex = showable(t, excerptsFor(excerpts, t.id));
  const url = safeUrl(t.source_url);
  return (
    <article className="stack-lg">
      <p className="small"><Link href="/heritage">← مكتبة التراث</Link></p>
      <PageHead kicker={t.lang_ar} title={t.title_ar} lead={ex.length ? "اقرأ المقطع أولاً، ثم اسأل نفسك السؤال الموجّه قبل أن تقرأ الشرح." : "نص مسجّل للمرجع فقط، بلا مقاطع."} />
      <p className="small dim" lang={t.lang === "ar" ? "ar" : "en"} dir={t.lang === "ar" ? "rtl" : "ltr"} style={{ textAlign: "start" }}>{t.title} — {t.author}</p>
      <div className="row"><Badge tone={t.rights === "cc_by_nc_ref" ? "warning" : "positive"}>{RIGHTS_LABEL[t.rights]}</Badge><Badge outline>{t.era_ar}</Badge><Badge outline>{t.author_ar}</Badge></div>

      <Card as="section"><h2 className="card-title">البيانات والحقوق</h2>
        <dl className="stack-sm small">
          <div><dt className="dim">الترخيص</dt><dd>{t.licence}</dd></div>
          <div><dt className="dim">الحكم الحقوقي</dt><dd>{t.rights_ar}</dd></div>
          <div><dt className="dim">المصدر الرقمي</dt><dd lang="en" dir="ltr" style={{ textAlign: "start" }}>{t.digitization}</dd></div>
          <div><dt className="dim">الرابط</dt><dd>{url ? <a href={url} target="_blank" rel="noopener noreferrer nofollow" className="mono" style={{ overflowWrap: "anywhere" }}>{url}</a> : <span className="mono">{t.source_url}</span>}</dd></div>
          <div><dt className="dim">معرّف في فهرسنا</dt><dd className="mono">{t.source_id ?? "—"} · {t.asset_id}</dd></div>
        </dl>
      </Card>

      {t.excerpt_count === 0 && (
        <Callout tone="warning" title={t.rights === "cc_by_nc_ref" ? "مرجع فقط: لا اقتباس" : "بلا مقاطع"}>{t.reference_reason_ar}</Callout>
      )}

      {ex.length > 0 && (
        <section className="stack" aria-label="المقاطع">
          <h2 className="text-label section-title">مقاطع قصيرة ({ex.length})</h2>
          {t.edit_note_ar && <p className="small dim">{t.edit_note_ar}</p>}
          <ol className="list">
            {ex.map((e) => (
              <li key={e.id}>
                <Card as="section" id={e.id}>
                  <p className="kicker">{e.skill_ar} · المقطع {e.n}</p>
                  <p><strong>{e.hook_ar}</strong></p>
                  <blockquote className="excerpt" lang={e.lang} dir={dirFor(e.lang)} style={{ whiteSpace: "pre-line" }}>{e.text}</blockquote>
                  <p className="small"><strong>الشرح بالعربية: </strong>{e.gloss_ar}</p>
                  <p className="small dim">من «{t.title_ar}»، {t.author_ar}. {e.locator}. <span lang="en" dir="ltr">{e.attribution}</span></p>
                </Card>
              </li>))}
          </ol>
        </section>
      )}
    </article>
  );
}
