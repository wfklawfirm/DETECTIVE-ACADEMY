import { getActorFromCookies } from "@/server/auth";
import { loadKnowledge, visibleKos } from "@/engine/knowledge";
import { KnowledgeBrowser } from "@/components/KnowledgeBrowser";
import Link from "next/link";

export const metadata = { title: "موسوعة المحقق" };
export const dynamic = "force-dynamic";

export default async function Knowledge() {
  const a = await getActorFromCookies();
  const { kos } = loadKnowledge();
  const items = visibleKos(kos, a.ageBand).map(({ ko_id, type, name_ar, summary_ar, confidence, status, tags }) => ({ ko_id, type, name_ar, summary_ar, confidence, status, tags }));
  return (
    <div className="wrap stack">
      <h1>موسوعة المحقق</h1>
      <p className="dim">مفاهيم من علم الأدلة، ومهارات الاستدلال، وأنماط الألغاز، مأخوذة من مكتبة أثر البحثية. كل مادة تُظهر درجة الثقة وحالتها: «مبني على أدلة» أو «فرضية تصميم» أو «ممارسة مهنية». لم تُراجَع بعدُ من خبراء مستقلين، فاعتبرها مادة تعليمية أولية لا مرجعاً علمياً نهائياً.</p>
      <p className="small"><Link href="/sources">من أين جاءت هذه المعلومات؟ سجل المصادر والحقوق</Link></p>
      <KnowledgeBrowser items={items} />
    </div>
  );
}
