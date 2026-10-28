import Link from "next/link";
import { loadAssets } from "@/engine/assets";
import { LinkButton } from "@/components/ui/button";
import { PageHead } from "@/components/ui/card";

export const metadata = { title: "معرض المراجع" };
export const dynamic = "force-dynamic";
const PER = 48;
const COLL_AR: Record<string, string> = {};

export default async function Gallery({ searchParams }: { searchParams: Promise<{ page?: string; c?: string; q?: string }> }) {
  const sp = await searchParams;
  const all = loadAssets().filter((a) => a.kind === "image");
  const colls = [...new Set(all.map((a) => a.collection ?? "other"))].sort();
  const q = (sp.q ?? "").trim().toLowerCase();
  const c = sp.c && colls.includes(sp.c) ? sp.c : "";
  const list = all.filter((a) => (!c || (a.collection ?? "other") === c) && (!q || `${a.title} ${a.creator} ${a.use} ${(a.tags ?? []).join(" ")}`.toLowerCase().includes(q)));
  const pages = Math.max(1, Math.ceil(list.length / PER));
  const page = Math.min(pages, Math.max(1, Number(sp.page) || 1));
  const imgs = list.slice((page - 1) * PER, page * PER);
  const href = (p: number) => `/gallery?${new URLSearchParams({ ...(c ? { c } : {}), ...(q ? { q } : {}), page: String(p) })}`;
  return (
    <>
      <PageHead title="معرض المراجع التاريخية" lead={`لقطات لمخطوطات وأدوات ووثائق وأماكن من مجموعات مفتوحة (${all.length} صورة)، نستلهم منها أجواء القضايا ومشاهدها. هي مراجع بصرية فقط؛ لا تظهر فيها شخصيات القصص ولا تُعدّ دليلاً في أي قضية. حقوق كل صورة مذكورة تحتها.`} />
      <form method="get" action="/gallery" className="row" role="search" aria-label="بحث في المعرض">
        <input className="input" type="search" name="q" defaultValue={sp.q ?? ""} placeholder="ابحث بالعنوان أو الوسم (بالإنجليزية غالباً)" aria-label="بحث" lang="en" dir="ltr" />
        <select className="input" name="c" defaultValue={c} aria-label="المجموعة">
          <option value="">كل المجموعات</option>
          {colls.map((x) => <option key={x} value={x}>{COLL_AR[x] ?? x}</option>)}
        </select>
        <button className="btn btn-outline" type="submit">بحث</button>
      </form>
      <p className="small dim" role="status">{list.length} نتيجة · صفحة {page} من {pages}</p>
      <ul className="gallery">
        {imgs.map((a) => (
          <li key={a.id}><figure>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={a.file} alt={a.title} loading="lazy" width={a.w} height={a.h} />
            <figcaption><b lang="en" dir="ltr">{a.title}</b><br />{a.use.split(";")[0]}<br /><span lang="en" dir="ltr">{a.institution ?? a.creator}</span></figcaption>
          </figure></li>
        ))}
      </ul>
      <nav className="row" aria-label="صفحات المعرض">
        {page > 1 && <Link className="btn btn-outline" href={href(page - 1)}>السابق</Link>}
        {page < pages && <Link className="btn btn-outline" href={href(page + 1)}>التالي</Link>}
      </nav>
      <LinkButton variant="outline" block href="/sounds">مكتبة الأصوات</LinkButton>
      <LinkButton variant="outline" block href="/icons">مكتبة الأيقونات</LinkButton>
      <LinkButton variant="outline" block href="/credits">كل الاعتمادات والتراخيص</LinkButton>
    </>
  );
}
