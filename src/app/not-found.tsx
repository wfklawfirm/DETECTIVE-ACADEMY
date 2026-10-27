import { AtharMark } from "@/components/ui/brand";
import { LinkButton } from "@/components/ui/button";

export default function NotFound() {
  return (
    <section className="lantern hero" aria-labelledby="nf-h" style={{ alignItems: "flex-start" }}>
      <AtharMark size={48} />
      <span className="stamp">ملف غير موجود</span>
      <h1 id="nf-h" className="hero-title" style={{ fontSize: "1.9rem" }}>لا أثر لهذه الصفحة</h1>
      <p className="hero-lead">الرابط الذي فتحته لا يقود إلى شيء هنا. ربما نُقل أو لم يوجد أصلاً.</p>
      <LinkButton variant="primary" size="lg" block href="/home">العودة إلى ملفاتي</LinkButton>
      <LinkButton variant="ghost" block href="/cases">تصفّح القضايا</LinkButton>
    </section>
  );
}
