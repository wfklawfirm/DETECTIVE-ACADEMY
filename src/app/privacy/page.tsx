import { Callout } from "@/components/ui/feedback";
import { LinkButton } from "@/components/ui/button";
import { PageHead } from "@/components/ui/card";

export const metadata = { title: "الخصوصية والسلامة" };
export default function Privacy() {
  return (
    <>
      <PageHead title="الخصوصية والسلامة" />
      <Callout tone="info">نص تشغيلي مختصر للنموذج التجريبي، وليس مراجعة قانونية نهائية.</Callout>
      <section className="stack"><h2 className="text-section-title">ما نجمعه</h2>
        <ul>
          <li>بلا حساب: فئتك العمرية العامة (كعكة صغيرة) ورمز تقدّم موقَّع على جهازك. لا نخزّن اسماً ولا بريداً ولا تاريخ ميلاد.</li>
          <li>مع حساب (١٨+ فقط حالياً): بريدك، كلمة مرور مشفّرة بدالة قوية، وتقدّمك في القضايا.</li>
          <li>سجل تدقيق للعمليات الإدارية يحتوي بصمة عنوان شبكة مملّحة لا العنوان نفسه.</li>
        </ul></section>
      <section className="stack"><h2 className="text-section-title">ما لا نفعله</h2>
        <ul><li>لا إعلانات ولا بيع بيانات، ولا تتبّع عبر مواقع أخرى.</li><li>لا نرسل نصوصك إلى خدمات ذكاء اصطناعي خارجية. الحوارات في هذه النسخة مكتوبة سلفاً ومضبوطة، وليست مولَّدة.</li><li>لا نستخدم عدّادات خسارة أو تشهيراً بالغياب. يمكنك تفعيل «الوضع الهادئ» من حسابك أو جهازك.</li></ul></section>
      <section className="stack"><h2 className="text-section-title">حقوقك</h2>
        <p>يمكنك حذف حسابك وكل تقدّمك من صفحة الحساب. بيانات الجهاز تُمسح بمسح بيانات الموقع من المتصفح.</p></section>
      <section className="stack"><h2 className="text-section-title">حدود هذه النسخة</h2>
        <ul><li>بوابة العمر ذاتية الإفصاح، وليست تحققاً من الهوية.</li><li>القضايا المعلَّمة «تجريبية» لم تكتمل مراجعتها العلمية والثقافية والقانونية بعد.</li><li>الدرجات «مبدئية» وليست قياساً نفسياً مقنّناً.</li></ul></section>
      <p>للإبلاغ عن محتوى غير مناسب أو خطأ علمي:</p>
      <LinkButton variant="outline" block href="/report">نموذج الإبلاغ</LinkButton>
    </>
  );
}
