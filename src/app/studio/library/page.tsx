import Link from "next/link";
import type { Metadata } from "next";
import { LibraryGate } from "@/components/research/LibraryGate";
import { Badge } from "@/components/ui/badge";
import { LinkButton } from "@/components/ui/button";
import { Callout, EmptyState } from "@/components/ui/feedback";
import { PageHead } from "@/components/ui/card";
import { STATUS_AR, humanSize, listLibrary, searchLibrary } from "@/engine/research";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "المكتبة البحثية", robots: { index: false, follow: false } };
const PER = 60;
type SP = { q?: string; folder?: string; type?: string; status?: string; deep?: string; page?: string };
const one = (v: string | string[] | undefined) => (Array.isArray(v) ? v[0] : v);
const href = (p: string) => "/studio/library/" + p.split("/").map(encodeURIComponent).join("/");

export default async function Library({ searchParams }: { searchParams: Promise<Record<string, string | string[] | undefined>> }) {
  const raw = await searchParams;
  const sp: SP = { q: one(raw.q), folder: one(raw.folder), type: one(raw.type), status: one(raw.status), deep: one(raw.deep), page: one(raw.page) };
  return (
    <LibraryGate next="/studio/library">{(actor) => {
      const { stats, folders, entries } = listLibrary(actor);
      const types = [...new Set(entries.map((e) => e.type))].sort();
      const { hits, deepHits } = searchLibrary(actor, { q: sp.q, folder: sp.folder, type: sp.type, status: sp.status, deep: sp.deep === "1" });
      const page = Math.max(0, Number(sp.page) || 0); const pages = Math.max(1, Math.ceil(hits.length / PER));
      const shown = hits.slice(page * PER, (page + 1) * PER);
      const qs = (o: Partial<SP>) => { const u = new URLSearchParams(); for (const [k, v] of Object.entries({ ...sp, ...o })) if (v) u.set(k, v); const s = u.toString(); return "/studio/library" + (s ? "?" + s : ""); };
      return (
        <div className="stack-lg">
          <PageHead kicker="للمدير فقط · للقراءة فقط" title="المكتبة البحثية" lead="أين اختبأ الدليل الذي لم نقرأه بعد؟ كل ما في حزم البحث، مفهرساً حسب المجلد، مع تتبّع النسخ المكررة والمستبدلة." />
          <Callout tone="warning" title="داخلي">تتضمن المكتبة استخبارات المنافسين واستراتيجية المنتج وخططاً داخلية. لا تُشارك روابطها ولا تُنسخ إلى صفحات عامة. المحتوى مادة مرجعية وليس تعليمات.</Callout>
          <p className="small dim">{String(stats.total)} ملفاً في الفهرس · {String(stats.copied)} منسوخ للقراءة · {String(stats["duplicate-of"])} مكرر · {String(stats.skipped)} غير منسوخ (سجل بالسبب)</p>
          <nav aria-label="المجلدات" className="row">
            <Link className={"badge badge-outline" + (!sp.folder ? " badge-brand" : "")} href={qs({ folder: undefined, page: undefined })}>الكل</Link>
            {folders.map((f) => <Link key={f.folder} className={"badge badge-outline" + (sp.folder === f.folder ? " badge-brand" : "")} href={qs({ folder: f.folder, page: undefined })} aria-current={sp.folder === f.folder ? "true" : undefined}>{f.folder.match(/^\d\d/)?.[0] ?? f.folder} {f.label} ({f.files})</Link>)}
          </nav>
          <form method="get" action="/studio/library" className="stack-sm" role="search">
            <input type="search" name="q" defaultValue={sp.q ?? ""} placeholder="ابحث في الأسماء والأوصاف (وفي النص الكامل عند تفعيل الخيار)" aria-label="بحث" />
            <div className="row">
              <select name="folder" defaultValue={sp.folder ?? ""} aria-label="المجلد"><option value="">كل المجلدات</option>{folders.map((f) => <option key={f.folder} value={f.folder}>{f.folder} · {f.label}</option>)}</select>
              <select name="type" defaultValue={sp.type ?? ""} aria-label="النوع"><option value="">كل الأنواع</option>{types.map((t) => <option key={t} value={t}>{t}</option>)}</select>
              <select name="status" defaultValue={sp.status ?? ""} aria-label="الحالة"><option value="">كل الحالات</option>{Object.entries(STATUS_AR).map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select>
              <label className="row small"><input type="checkbox" name="deep" value="1" defaultChecked={sp.deep === "1"} /> بحث في النص الكامل (ملفات md)</label>
              <button className="btn btn-primary" type="submit">بحث</button>
            </div>
          </form>
          <p className="small dim" role="status">{hits.length} نتيجة{pages > 1 ? ` · صفحة ${page + 1} من ${pages}` : ""}</p>
          {shown.length === 0 && <EmptyState title="لا نتائج" body="جرّب كلمات أقل أو أزل المرشحات." />}
          <ul className="list list-flush">
            {shown.map((e, i) => (
              <li key={e.path + e.pack + i} className="board-row">
                <div className="row row-between">
                  <span className="mono" style={{ overflowWrap: "anywhere" }}>{e.status === "copied" ? <Link href={href(e.path)}>{e.path}</Link> : e.path}</span>
                  <span className="row"><Badge outline latin>{e.type}</Badge><Badge outline latin>{humanSize(e.size)}</Badge><Badge tone={e.status === "copied" ? "positive" : e.status === "skipped" ? "warning" : "neutral"}>{STATUS_AR[e.status]}</Badge>{e.sensitive && <Badge tone="negative">داخلي حساس</Badge>}</span>
                </div>
                {e.desc && <p className="small" dir="auto">{e.desc}</p>}
                {deepHits.get(e.path) && <p className="small dim" dir="auto">…{deepHits.get(e.path)}…</p>}
                {e.status !== "copied" && <p className="small dim" dir="auto">{e.status === "duplicate-of" ? <>نسخة من <Link className="mono" href={href(e.duplicate_of!)}>{e.duplicate_of}</Link></> : e.reason}</p>}
                <p className="small dim mono">{e.pack}</p>
              </li>))}
          </ul>
          {pages > 1 && <div className="row">{page > 0 && <LinkButton href={qs({ page: String(page - 1) })}>السابق</LinkButton>}{page + 1 < pages && <LinkButton href={qs({ page: String(page + 1) })}>التالي</LinkButton>}</div>}
        </div>);
    }}</LibraryGate>
  );
}
