import { getActorFromCookies } from "@/server/auth";
import { loadKnowledge, visibleKos } from "@/engine/knowledge";
import { KnowledgeBrowser } from "@/components/KnowledgeBrowser";
import { REFERENCE_PAGES } from "@/engine/reference-labels";
import { PageHead, RowLink } from "@/components/ui/card";
import { Callout } from "@/components/ui/feedback";
import { FlaskIcon, ImageIcon, LinkIcon, SparkIcon } from "@/components/ui/icons";

export const metadata = { title: "موسوعة المحقق" };
export const dynamic = "force-dynamic";

export default async function Knowledge() {
  const a = await getActorFromCookies();
  const { kos } = loadKnowledge();
  const items = visibleKos(kos, a.ageBand).map(({ ko_id, type, name_ar, summary_ar, confidence, status, tags }) => ({ ko_id, type, name_ar, summary_ar, confidence, status, tags }));
  return (
    <>
      <PageHead title="موسوعة المحقق" lead="مفاهيم من علم الأدلة، ومهارات الاستدلال، وأنماط الألغاز، مأخوذة من مكتبة أثر البحثية." />
      <Callout tone="warning" title="مادة أولية">كل مادة تُظهر درجة الثقة وحالتها: «مبني على أدلة» أو «فرضية تصميم» أو «ممارسة مهنية». لم تُراجَع بعدُ من خبراء مستقلين، فاعتبرها مادة تعليمية أولية لا مرجعاً علمياً نهائياً.</Callout>
      <ul className="list" aria-label="روابط الموسوعة">
        <li><RowLink href="/labs" icon={<FlaskIcon size={22} />} title="مختبرات آمنة" hint="تمارين قصيرة بسجلات خيالية" /></li>
        <li><RowLink href="/skills" icon={<SparkIcon size={22} />} title="المهارات وأنماط الألغاز" hint="الإطار الذي نبني عليه القضايا" /></li>
        <li><RowLink href="/sources" icon={<LinkIcon size={22} />} title="من أين جاءت هذه المعلومات؟" hint="سجل المصادر والحقوق" /></li>
        {REFERENCE_PAGES.map((r) => <li key={r.href}><RowLink href={r.href} icon={<SparkIcon size={22} />} title={r.title} hint={r.hint} /></li>)}
        <li><RowLink href="/books" icon={<FlaskIcon size={22} />} title="مفاهيم من كتب الطب الشرعي" hint="ملاحظات أصلية مع تدريبات قصيرة" /></li>
        <li><RowLink href="/heritage" icon={<LinkIcon size={22} />} title="تراث الاستدلال" hint="نصوص من الملك العام ومراجع الأدب البوليسي" /></li>
        <li><RowLink href="/gallery" icon={<ImageIcon size={22} />} title="معرض المراجع" hint="صور مرجعية من مجموعات مفتوحة" /></li>
      </ul>
      <KnowledgeBrowser items={items} />
    </>
  );
}
