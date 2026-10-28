import Link from "next/link";
import type { Metadata } from "next";
import { LibraryGate } from "@/components/research/LibraryGate";
import { Markdown } from "@/components/research/Markdown";
import { Badge } from "@/components/ui/badge";
import { LinkButton } from "@/components/ui/button";
import { Callout, EmptyState } from "@/components/ui/feedback";
import { Card } from "@/components/ui/card";
import { STATUS_AR, findEntry, firstJsonRecords, humanSize, parseCsvPage, readDoc, relatedRows } from "@/engine/research";

export const dynamic = "force-dynamic";
export const metadata: Metadata = { title: "وثيقة من المكتبة البحثية", robots: { index: false, follow: false } };
const ROWS = 50; const CELL = 400;
const href = (p: string) => "/studio/library/" + p.split("/").map(encodeURIComponent).join("/");

export default async function Doc({ params, searchParams }: { params: Promise<{ path: string[] }>; searchParams: Promise<{ page?: string }> }) {
  const { path } = await params; const sp = await searchParams;
  const segs = path.map((s) => { try { return decodeURIComponent(s); } catch { return ""; } });
  return (
    <LibraryGate next={"/studio/library/" + path.join("/")}>{(actor) => {
      const e = findEntry(actor, segs);
      if (!e) return <EmptyState title="لا توجد وثيقة بهذا المسار" action={<LinkButton href="/studio/library">العودة للفهرس</LinkButton>} />;
      const related = relatedRows(actor, e).filter((x) => x.path !== e.path || x.pack !== e.pack);
      const head = (
        <>
          <p className="small"><Link href="/studio/library">← المكتبة</Link></p>
          <div className="ref-hero">
            <p className="ref-hero-kicker"><span className="mono">{e.folder}</span></p>
            <h1 className="ref-hero-title" dir="auto">{e.desc && e.type === "md" ? e.desc : e.path.split("/").pop()}</h1>
            <p className="ref-hero-hook">للقراءة فقط · للمدير فقط.</p>
          </div>
          <div className="row"><Badge outline latin>{e.type}</Badge><Badge outline latin>{humanSize(e.size)}</Badge><Badge tone={e.status === "copied" ? "positive" : "warning"}>{STATUS_AR[e.status]}</Badge>{e.sensitive && <Badge tone="negative">داخلي حساس</Badge>}<Badge outline latin>{e.pack}</Badge></div>
          <p className="small dim mono" style={{ overflowWrap: "anywhere" }}>{e.path} · sha256 {e.sha256.slice(0, 16)}…</p>
        </>
      );
      const relatedList = related.length > 0 && (
        <details className="card"><summary>نسخ أخرى مسجلة في الفهرس ({related.length})</summary>
          <ul className="stack-sm small">{related.map((r) => <li key={r.pack + r.source_path} className="mono" style={{ overflowWrap: "anywhere" }}>{r.pack} · {r.status === "duplicate-of" ? "مطابقة" : "تختلف وتم استبدالها"} · {r.source_path}</li>)}</ul></details>
      );
      if (e.status !== "copied") {
        return <div className="stack-lg">{head}<Callout tone="info" title="غير منسوخ">{e.status === "duplicate-of" ? <>هذا الملف مطابق (sha256) لنسخة محفوظة: <Link className="mono" href={href(e.duplicate_of!)}>{e.duplicate_of}</Link></> : e.reason}</Callout>{relatedList}</div>;
      }
      const text = readDoc(actor, e);
      if (text === null) return <div className="stack-lg">{head}<EmptyState title="تعذّر قراءة الملف" /></div>;
      let body: React.ReactNode;
      if (e.type === "md") body = <Card as="article"><Markdown source={text} /></Card>;
      else if (e.type === "txt") body = <pre className="rl-json" tabIndex={0} dir="auto">{text}</pre>;
      else if (e.type === "csv") {
        const page = Math.max(0, Number(sp.page) || 0);
        const { header, rows, total } = parseCsvPage(text, page, ROWS); const pages = Math.max(1, Math.ceil(total / ROWS));
        const q = (n: number) => `${href(e.path)}?page=${n}`;
        body = (
          <div className="stack">
            <p className="small dim">{total} سطراً · {header.length} عموداً · صفحة {page + 1} من {pages}</p>
            <div className="table-wrap" tabIndex={0} role="region" aria-label="جدول البيانات"><table className="simple rl-table"><thead><tr>{header.map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
              <tbody>{rows.map((r, ri) => <tr key={ri}>{r.map((c, ci) => <td key={ci} dir="auto">{c.length > CELL ? c.slice(0, CELL) + "…" : c}</td>)}</tr>)}</tbody></table></div>
            <div className="row">{page > 0 && <LinkButton href={q(page - 1)}>السابق</LinkButton>}{page + 1 < pages && <LinkButton href={q(page + 1)}>التالي</LinkButton>}</div>
          </div>);
      } else {
        let info: ReturnType<typeof firstJsonRecords> | null = null;
        try { info = firstJsonRecords(text, e.type === "jsonl" ? "jsonl" : "json", 8); } catch { info = null; }
        body = info ? (
          <div className="stack">
            <p className="small dim">{info.count} {e.type === "jsonl" ? "سجلاً" : "عنصراً"}{info.keys.length ? ` · الحقول: ${info.keys.join("، ")}` : ""} · أول {info.records.length} فقط</p>
            {info.records.map((r, i) => { const s = JSON.stringify(r, null, 2); return <pre key={i} className="rl-json" tabIndex={0}>{s.length > 3000 ? s.slice(0, 3000) + "\n…" : s}</pre>; })}
          </div>) : <EmptyState title="ملف JSON غير قابل للتحليل" />;
      }
      return <div className="stack-lg">{head}{body}{relatedList}</div>;
    }}</LibraryGate>
  );
}
