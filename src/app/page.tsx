import Link from "next/link";
import { EntryHook } from "@/components/EntryHook";

export default function Landing() {
  return (
    <div className="wrap">
      <EntryHook surface="landing" />
      <section className="hero">
        <p className="kicker">تحقيقات عربية · أدلة حقيقية الطابع · قصص من تأليفنا</p>
        <h1>الحقيقة لا تُخمَّن. <span style={{ color: "var(--amber)" }}>تُثبَت.</span></h1>
        <p className="lead">افتح ملفاً غامضاً، اقرأ سجلاته، استجوب شهوده، وتعلّم كيف تفرّق بين ما تثبته الأدلة وما يبدو مقنعاً فقط.</p>
        <div className="row" style={{ marginBlockStart: 24 }}>
          <Link className="btn primary" href="/start">افتح أول ملف — ١٢ دقيقة</Link>
          <Link className="btn" href="/cases">تصفّح القضايا</Link>
        </div>
      </section>
      <section className="grid cols-2" style={{ marginBlockStart: 40 }} aria-label="كيف تعمل أثر">
        <div className="card"><h3>أدلة لا حدس</h3><p className="dim">كل استنتاج تربطه بدليل، وكل دليل تصنّف مصدره وحدوده. لا مكافأة على التخمين ولا على البلاغة.</p></div>
        <div className="card"><h3>حقيقة ثابتة سلفاً</h3><p className="dim">حقيقة كل قضية مكتوبة ومراجَعة قبل أن تبدأ. الشخصيات لا تقول إلا ما تعرفه، ولا يخترع النظام أدلة أثناء اللعب.</p></div>
        <div className="card"><h3>أخطئ وراجع</h3><p className="dim">فرضياتك تُسجَّل بتاريخ تعديلها. تغيير الرأي أمام دليل جديد يُحسب لك لا عليك.</p></div>
        <div className="card"><h3>مهارات تنتقل معك</h3><p className="dim">بعد كل قضية تجربة قصيرة على سياق جديد: هل انتقلت المهارة فعلاً؟ والنتائج «مبدئية» ونقولها بصراحة.</p></div>
      </section>
    </div>
  );
}
