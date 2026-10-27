import { loadAssets } from "@/engine/assets";

export const metadata = { title: "معرض المراجع" };
export const dynamic = "force-dynamic";

export default function Gallery() {
  const imgs = loadAssets().filter((a) => a.kind === "image");
  return (
    <div className="wrap stack">
      <h1>معرض المراجع التاريخية</h1>
      <p className="dim">صور لمخطوطات وأدوات ووثائق قديمة من مجموعات مفتوحة، نستلهم منها أجواء القضايا ومشاهدها. هي مراجع بصرية فقط؛ لا تظهر فيها شخصيات القصص ولا تُعدّ دليلاً في أي قضية. حقوق كل صورة مذكورة تحتها.</p>
      <ul className="gallery">
        {imgs.map((a) => (
          <li key={a.id}><figure>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={a.file} alt={a.title} loading="lazy" width={a.w} height={a.h} />
            <figcaption><b lang="en" dir="ltr">{a.title}</b><br />{a.use.split(";")[0]}<br /><span lang="en" dir="ltr">{a.institution ?? a.creator}</span></figcaption>
          </figure></li>
        ))}
      </ul>
      <p className="small"><a href="/credits">كل الاعتمادات والتراخيص</a></p>
    </div>
  );
}
