import { loadIcons } from "@/engine/icons";
import { Badge } from "@/components/ui/badge";
import { Card, PageHead } from "@/components/ui/card";

export const metadata = { title: "مكتبة الأيقونات" };
export const dynamic = "force-dynamic";

export default function Icons() {
  const { sets, icons } = loadIcons();
  return (
    <>
      <PageHead title="مكتبة الأيقونات" lead={`${icons.length} أيقونة خطية من ست مكتبات مفتوحة المصدر، محفوظة هنا مع نص ترخيص كل مكتبة. واجهة أثر نفسها تستعمل عائلة أيقونات واحدة؛ هذه المكتبة مرجع لمن يصمّم قضايا وأدوات جديدة.`} />
      {sets.map((s) => (
        <section key={s.key} className="stack" aria-label={s.name}>
          <h2 className="text-label section-title" lang="en" dir="ltr">{s.name} · <Badge latin>{s.license}</Badge> · {s.count} · <a href={s.license_file}>license</a></h2>
          <ul className="icon-grid">
            {icons.filter((i) => i.set === s.key).map((i) => (
              <li key={i.file}><figure>
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={i.file} alt="" width={28} height={28} loading="lazy" />
                <figcaption lang="en" dir="ltr">{i.name}</figcaption>
              </figure></li>
            ))}
          </ul>
        </section>
      ))}
      <Card flat className="small">الأيقونات تحتفظ بإشعار حقوق مؤلفيها كما اشترطت تراخيصها (MIT / ISC / Apache-2.0). لا ندّعي أنها من تصميمنا.</Card>
    </>
  );
}
