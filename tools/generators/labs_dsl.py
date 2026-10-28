"""Tiny constructors for the lab content files. Each lab ends with a boundary ('what this cannot prove') and a transfer question; each has a hook."""
def I(id, text, answer, why): return {"id": id, "text_ar": text, "answer": answer, "why_ar": why}   # classify item / match pair
def S(id, text, why): return {"id": id, "text_ar": text, "why_ar": why}                              # order step
def C(id, label): return {"id": id, "label_ar": label}                                                 # category / option
def L(id, text, flaw=None, why=None, ok=None):                                                         # spot line
    return {"id": id, "text_ar": text, "flaw": ({"label_ar": flaw, "why_ar": why} if flaw else None), **({"ok_ar": ok} if ok else {})}
def O(id, text, verdict, why): return {"id": id, "text_ar": text, "verdict": verdict, "why_ar": why}  # conclude option
def SC(id, facts, q, opts): return {"id": id, "facts_ar": facts, "question_ar": q, "options": opts}
def T(id, prompt, unit, answer, tol, why, traps=None): return {"id": id, "prompt_ar": prompt, "unit_ar": unit, "answer": answer, "tolerance": tol, "why_ar": why, "traps": traps or []}
def X(id, label, mn, mx, step, value, unit=None):                                                       # slider control
    d = {"id": id, "label_ar": label, "min": mn, "max": mx, "step": step, "value": value}
    if unit: d["unit_ar"] = unit
    return d
def OUT(id, label, expr, decimals=1, unit=None, read=None):
    d = {"id": id, "label_ar": label, "expr": expr, "decimals": decimals}
    if unit: d["unit_ar"] = unit
    if read: d["read_ar"] = [{"max": m, "text_ar": t} for m, t in read]
    return d

def lab(kind, id, title, skill, interaction, hook, intro, transfer, boundary, d, m, ko=(), origin="", illustrative=None, **body):
    x = {"id": id, "kind": kind, "title_ar": title, "skill_ar": skill, "intro_ar": intro, "hook_ar": hook, "transfer_ar": transfer, "boundary_ar": boundary,
         "difficulty": d, "minutes": m, "ko_ids": list(ko), **body}
    if illustrative: x["illustrative_ar"] = illustrative
    x["_cat"] = {"interaction_ar": interaction, "origin_ar": origin}
    return x
