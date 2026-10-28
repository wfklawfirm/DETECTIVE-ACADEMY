import { EntryHook } from "@/components/EntryHook";
import { AtharMark } from "@/components/ui/brand";
import { LinkButton } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Callout } from "@/components/ui/feedback";
import { EvidenceIcon, ScaleIcon, RefreshIcon, SparkIcon } from "@/components/ui/icons";

const POINTS = [
  { Icon: EvidenceIcon, t: "أدلة لا حدس", d: "كل استنتاج تربطه بدليل، وكل دليل تصنّف مصدره وحدوده. لا مكافأة على التخمين ولا على البلاغة." },
  { Icon: ScaleIcon, t: "حقيقة ثابتة سلفاً", d: "حقيقة كل قضية مكتوبة ومراجَعة قبل أن تبدأ. الشخصيات لا تقول إلا ما تعرفه، ولا يخترع النظام أدلة أثناء اللعب." },
  { Icon: RefreshIcon, t: "أخطئ وراجع", d: "فرضياتك تُسجَّل بتاريخ تعديلها. تغيير الرأي أمام دليل جديد يُحسب لك لا عليك." },
  { Icon: SparkIcon, t: "مهارات تنتقل معك", d: "بعد كل قضية تجربة قصيرة على سياق جديد: هل انتقلت المهارة فعلاً؟ والنتائج «مبدئية» ونقولها بصراحة." },
];

export default function Landing() {
  return (
    <>
      <EntryHook surface="landing" />
      <section className="lantern hero" aria-labelledby="hero-h">
        <div className="row" style={{ justifyContent: "space-between" }}>
          <span className="stamp">سرّي · قيد التحقيق</span>
          <AtharMark size={44} />
        </div>
        <p className="kicker">تحقيقات عربية · أدلة حقيقية الطابع · قصص من تأليفنا</p>
        <h1 id="hero-h" className="hero-title">الحقيقة لا تُخمَّن. <em>تُثبَت.</em></h1>
        <p className="hero-lead">افتح ملفاً غامضاً، اقرأ سجلاته، استجوب شهوده، وتعلّم كيف تفرّق بين ما تثبته الأدلة وما يبدو مقنعاً فقط.</p>
        <LinkButton variant="primary" size="lg" block href="/start">افتح أول ملف — ١٢ دقيقة</LinkButton>
        <LinkButton variant="ghost" block href="/cases">تصفّح القضايا</LinkButton>
      </section>
      <section className="stack" aria-labelledby="how-h">
        <h2 id="how-h" className="text-label section-title">كيف تعمل Detective Academy</h2>
        <ul className="list">
          {POINTS.map(({ Icon, t, d }) => (
            <li key={t}><Card as="div" flat><div className="row" style={{ flexWrap: "nowrap", alignItems: "flex-start" }}><span className="ico" style={{ color: "var(--foreground-secondary)", marginBlockStart: "0.2rem" }}><Icon size={24} /></span><div className="stack-sm grow"><h3 className="card-title">{t}</h3><p className="small dim-2">{d}</p></div></div></Card></li>
          ))}
        </ul>
      </section>
      <Callout tone="info" title="نموذج تجريبي">بعض القضايا ما زالت قيد المراجعة الخبيرة وهي معلَّمة بذلك. لا نسأل عن هويتك، وتقدّمك يُحفظ على جهازك.</Callout>
    </>
  );
}
