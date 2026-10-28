/** Tiny safe arithmetic evaluator for slider-model labs. No eval, no property access: numbers, variables, + - * / ^, parentheses and a few named functions. */
type Tok = { t: "num"; v: number } | { t: "id"; v: string } | { t: "op"; v: string };
const FN: Record<string, (...a: number[]) => number> = {
  sqrt: Math.sqrt, abs: Math.abs, min: Math.min, max: Math.max, ln: Math.log, exp: Math.exp, round: Math.round, floor: Math.floor, ceil: Math.ceil,
  pow: Math.pow, tan: Math.tan, atan: Math.atan, deg: (r) => (r * 180) / Math.PI, rad: (d) => (d * Math.PI) / 180, clamp: (x, lo, hi) => Math.min(hi, Math.max(lo, x)),
};
function lex(s: string): Tok[] {
  const out: Tok[] = []; let i = 0;
  while (i < s.length) {
    const c = s[i]!;
    if (/\s/.test(c)) { i++; continue; }
    const n = /^\d+(\.\d+)?/.exec(s.slice(i));
    if (n) { out.push({ t: "num", v: Number(n[0]) }); i += n[0].length; continue; }
    const id = /^[A-Za-z_][A-Za-z0-9_]*/.exec(s.slice(i));
    if (id) { out.push({ t: "id", v: id[0] }); i += id[0].length; continue; }
    if ("+-*/^(),".includes(c)) { out.push({ t: "op", v: c }); i++; continue; }
    throw new Error(`bad character '${c}' in expression`);
  }
  return out;
}
/** Names used by an expression (variables and functions) for validation at load time. */
export function exprNames(src: string): { vars: string[]; fns: string[] } {
  const toks = lex(src); const vars = new Set<string>(), fns = new Set<string>();
  toks.forEach((t, i) => { if (t.t === "id") (toks[i + 1]?.t === "op" && toks[i + 1]!.v === "(" ? fns : vars).add(t.v); });
  return { vars: [...vars], fns: [...fns] };
}
export function evalExpr(src: string, env: Record<string, number>): number {
  const toks = lex(src); let p = 0;
  const peek = () => toks[p]; const isOp = (v: string) => { const t = peek(); return t?.t === "op" && t.v === v; };
  function primary(): number {
    const t = toks[p++];
    if (!t) throw new Error("unexpected end");
    if (t.t === "num") return t.v;
    if (t.t === "op" && t.v === "(") { const v = add(); if (!isOp(")")) throw new Error("missing )"); p++; return v; }
    if (t.t === "op" && t.v === "-") return -unary();
    if (t.t === "id") {
      if (isOp("(")) {
        p++; const args: number[] = [];
        if (!isOp(")")) { do { args.push(add()); } while (isOp(",") && p++ >= 0); }
        if (!isOp(")")) throw new Error("missing )"); p++;
        const f = Object.prototype.hasOwnProperty.call(FN, t.v) ? FN[t.v] : undefined;
        if (!f) throw new Error(`unknown function ${t.v}`);
        return f(...args);
      }
      if (!Object.prototype.hasOwnProperty.call(env, t.v)) throw new Error(`unknown variable ${t.v}`);
      return env[t.v]!;
    }
    throw new Error("unexpected token");
  }
  function unary(): number { if (isOp("-")) { p++; return -unary(); } return power(); }
  function power(): number { const b = primary(); if (isOp("^")) { p++; return Math.pow(b, unary()); } return b; }
  function mul(): number { let v = unary(); while (isOp("*") || isOp("/")) { const o = toks[p++] as { v: string }; const r = unary(); v = o.v === "*" ? v * r : v / r; } return v; }
  function add(): number { let v = mul(); while (isOp("+") || isOp("-")) { const o = toks[p++] as { v: string }; const r = mul(); v = o.v === "+" ? v + r : v - r; } return v; }
  const v = add();
  if (p !== toks.length) throw new Error("trailing tokens");
  return v;
}
