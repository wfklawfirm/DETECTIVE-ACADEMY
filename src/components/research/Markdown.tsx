import type { ReactNode } from "react";

/**
 * Small, safe Markdown renderer. It only ever builds React elements from text (React escapes everything);
 * there is no raw-HTML injection API in use and raw HTML in the source is shown as literal text.
 * Links: only http(s) targets become anchors; every other scheme (javascript:, data:, ...) is rendered as plain text.
 */
export function safeHref(u: string): string | null {
  const t = u.trim();
  return /^https?:\/\/[^\s<>"']+$/i.test(t) ? t : null;
}

function inline(src: string, key: string): ReactNode[] {
  const out: ReactNode[] = [];
  const re = /(`[^`]+`)|(\*\*[^*]+\*\*)|(__[^_]+__)|(\[[^\]]+\]\([^)\s]*\))|(\*[^*\s][^*]*\*)|(https?:\/\/[^\s<>)\]"']+)/g;
  let last = 0; let m: RegExpExecArray | null; let i = 0;
  while ((m = re.exec(src))) {
    if (m.index > last) out.push(src.slice(last, m.index));
    const t = m[0]; const k = `${key}-${i++}`;
    if (m[1]) out.push(<code key={k} className="mono">{t.slice(1, -1)}</code>);
    else if (m[2] || m[3]) out.push(<strong key={k}>{inline(t.slice(2, -2), k)}</strong>);
    else if (m[4]) {
      const mm = /^\[([^\]]+)\]\(([^)\s]*)\)$/.exec(t) ?? []; const h = safeHref(mm[2] ?? "");
      out.push(h ? <a key={k} href={h} target="_blank" rel="noopener noreferrer nofollow">{mm[1] ?? ""}</a> : <span key={k}>{mm[1] ?? ""}</span>);
    } else if (m[5]) out.push(<em key={k}>{inline(t.slice(1, -1), k)}</em>);
    else { const h = safeHref(t); out.push(h ? <a key={k} href={h} target="_blank" rel="noopener noreferrer nofollow" className="mono">{t}</a> : t); }
    last = m.index + t.length;
  }
  if (last < src.length) out.push(src.slice(last));
  return out;
}

const isTableSep = (l: string) => /^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$/.test(l);
const cells = (l: string) => l.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((c) => c.trim());

export function Markdown({ source, maxBlocks = 4000 }: { source: string; maxBlocks?: number }) {
  const lines = source.replace(/\r\n?/g, "\n").split("\n");
  // drop YAML front matter
  const at = (k: number) => lines[k] ?? "";
  let i = 0;
  if (at(0).trim() === "---") { const end = lines.indexOf("---", 1); if (end > 0 && end < 60) i = end + 1; }
  const out: ReactNode[] = []; let b = 0;
  const push = (n: ReactNode) => { if (b++ < maxBlocks) out.push(n); };
  while (i < lines.length) {
    const line = at(i);
    if (!line.trim()) { i++; continue; }
    const fence = /^\s*(```|~~~)/.exec(line);
    if (fence) {
      const buf: string[] = []; i++;
      while (i < lines.length && !at(i).trim().startsWith(fence[1] ?? "```")) buf.push(at(i++));
      i++;
      push(<pre key={b} className="md-pre" dir="ltr"><code>{buf.join("\n")}</code></pre>); continue;
    }
    const h = /^(#{1,6})\s+(.*)$/.exec(line);
    if (h) {
      const lvl = Math.min((h[1] ?? "").length + 1, 6) as 2 | 3 | 4 | 5 | 6; const Tag = `h${lvl}` as "h2";
      push(<Tag key={b} dir="auto" className="md-h">{inline(h[2] ?? "", `h${b}`)}</Tag>); i++; continue;
    }
    if (/^\s*([-*_])(\s*\1){2,}\s*$/.test(line)) { push(<hr key={b} />); i++; continue; }
    if (line.includes("|") && i + 1 < lines.length && isTableSep(at(i + 1))) {
      const head = cells(line); i += 2; const body: string[][] = [];
      while (i < lines.length && at(i).includes("|") && at(i).trim()) body.push(cells(at(i++)));
      push(<div key={b} className="table-wrap" tabIndex={0} role="region" aria-label="جدول"><table className="simple"><thead><tr>{head.map((c, j) => <th key={j} dir="auto">{inline(c, `th${b}${j}`)}</th>)}</tr></thead><tbody>{body.map((r, ri) => <tr key={ri}>{r.map((c, j) => <td key={j} dir="auto">{inline(c, `td${b}${ri}${j}`)}</td>)}</tr>)}</tbody></table></div>);
      continue;
    }
    if (/^\s*>/.test(line)) {
      const buf: string[] = [];
      while (i < lines.length && /^\s*>/.test(at(i))) buf.push(at(i++).replace(/^\s*>\s?/, ""));
      push(<blockquote key={b} className="md-quote" dir="auto">{inline(buf.join(" "), `q${b}`)}</blockquote>); continue;
    }
    const li = /^(\s*)([-*+]|\d+[.)])\s+(.*)$/.exec(line);
    if (li) {
      const ordered = /\d/.test(li[2] ?? ""); const items: { depth: number; text: string }[] = [];
      while (i < lines.length) {
        const m = /^(\s*)([-*+]|\d+[.)])\s+(.*)$/.exec(at(i));
        if (m) { items.push({ depth: Math.min(Math.floor((m[1] ?? "").length / 2), 3), text: m[3] ?? "" }); i++; }
        else if (at(i).trim() && /^\s{2,}\S/.test(at(i)) && items.length) { { const last = items[items.length - 1]; if (last) last.text += " " + at(i).trim(); } i++; }
        else break;
      }
      const Tag = ordered ? "ol" : "ul";
      push(<Tag key={b} className="md-list">{items.map((it, j) => <li key={j} dir="auto" style={{ marginInlineStart: `${it.depth * 1.25}rem` }}>{inline(it.text, `li${b}${j}`)}</li>)}</Tag>); continue;
    }
    const buf: string[] = [];
    while (i < lines.length && at(i).trim() && !/^(#{1,6}\s|\s*(```|~~~)|\s*>|\s*([-*+]|\d+[.)])\s)/.test(at(i)) && !(at(i).includes("|") && i + 1 < lines.length && isTableSep(at(i + 1)))) buf.push(at(i++).trim());
    if (!buf.length) { buf.push(at(i++).trim()); }
    push(<p key={b} dir="auto">{inline(buf.join(" "), `p${b}`)}</p>);
  }
  return <div className="md-doc">{out}{b > maxBlocks && <p className="small dim">… تم اقتطاع باقي المستند ({b - maxBlocks} كتلة).</p>}</div>;
}
