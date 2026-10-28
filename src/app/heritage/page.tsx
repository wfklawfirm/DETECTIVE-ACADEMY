import Link from "next/link";
import type { Metadata } from "next";
import { Badge } from "@/components/ui/badge";
import { Callout } from "@/components/ui/feedback";
import { Card, PageHead } from "@/components/ui/card";
import { LANG_NAME, LANG_ORDER, RIGHTS_LABEL, loadHeritage } from "@/engine/heritage";

export const metadata: Metadata = { title: "مكتبة التراث", description: "فهرس لنصوص التحري والاستدلال في الملك العام، مع مقاطع قصيرة منسوبة لأصحابها." };

export default function Heritage() {
  const { texts, excerpts } = loadHeritage();
  const withEx = texts.filter((t) => t.excerpt_count > 0);
  const refOnly = texts.filter((t) => t.excerpt_count === 0);
  const words = Math.round(excerpts.reduce((s, e) => s + e.words, 0));
  return (
    <div className="stack-lg">
      <PageHead kicker="مكتبة التراث" title="قبل أن يكون هناك محققون في الشاشات" lead="هل سبق أحدٌ هولمز إلى فكرة «لا تثق بما ترى حتى تلاحظ»؟ اقرأ مقاطع قصيرة من نصوص قديمة، وانتبه إلى ما تلاحظه أنت." />
      <Callout tone="info" title="كيف نتعامل مع الحقوق؟">
        نقتبس مقاطع قصيرة (أقل من ١٢٠ كلمة) من نصوص ثبت أنها في الملك العام أو CC0، وننسبها لأصحابها ولمصدرها. أما النصوص ذات الترخيص غير التجاري (مثل مدونة OpenITI) فنذكر بياناتها فقط ولا نقتبس منها.
        المقاطع بلغتها الأصلية مع شرح عربي قصير؛ والشرح العربي من إعدادنا ولم يراجعه مختص بعد.
      </Callout>
      <p className="small dim">{texts.length} نصاً في الفهرس · {withEx.length} منها بمقاطع ({excerpts.length} مقطعاً، نحو {words.toLocaleString("ar")} كلمة) · {refOnly.length} للمرجع فقط</p>
      <nav aria-label="اللغات" className="row">
        {LANG_ORDER.filter((l) => withEx.some((t) => t.lang === l)).map((l) => <a key={l} className="badge badge-outline" href={`#lang-${l}`}>{LANG_NAME[l]} ({withEx.filter((t) => t.lang === l).length})</a>)}
        <a className="badge badge-outline" href="#ref-only">للمرجع فقط ({refOnly.length})</a>
      </nav>
      {LANG_ORDER.map((l) => {
        const items = withEx.filter((t) => t.lang === l);
        if (!items.length) return null;
        return (
          <section key={l} id={`lang-${l}`} className="stack" aria-labelledby={`h-${l}`}>
            <h2 id={`h-${l}`} className="text-label section-title">نصوص {LANG_NAME[l]}</h2>
            <ul className="list">{items.map((t) => (
              <li key={t.id}>
                <Card as="article">
                  <div className="row row-between">
                    <h3 className="card-title"><Link href={`/heritage/${t.id}`}>{t.title_ar}</Link></h3>
                    <Badge tone="positive">{t.excerpt_count} مقاطع</Badge>
                  </div>
                  <p className="small dim" lang="en" dir="ltr" style={{ textAlign: "start" }}>{t.title}</p>
                  <p className="small">{t.author_ar} · {t.era_ar} · {t.lang_ar}</p>
                  <div className="row"><Badge outline>{RIGHTS_LABEL[t.rights]}</Badge></div>
                </Card>
              </li>))}</ul>
          </section>);
      })}
      <section id="ref-only" className="stack" aria-labelledby="h-ref">
        <h2 id="h-ref" className="text-label section-title">للمرجع فقط (بلا اقتباس)</h2>
        <p className="small dim">هذه النصوص مسجلة بعنوانها ومؤلفها وترخيصها ورابطها، دون أي مقطع منها.</p>
        <ul className="list">{refOnly.map((t) => (
          <li key={t.id}>
            <Card as="article" flat>
              <div className="row row-between">
                <h3 className="card-title"><Link href={`/heritage/${t.id}`}>{t.title_ar}</Link></h3>
                <Badge tone={t.rights === "cc_by_nc_ref" ? "warning" : "neutral"}>{t.rights === "cc_by_nc_ref" ? "ترخيص غير تجاري" : "بلا مقاطع"}</Badge>
              </div>
              <p className="small">{t.author_ar} · {t.era_ar} · {t.lang_ar}</p>
            </Card>
          </li>))}</ul>
      </section>
    </div>
  );
}
