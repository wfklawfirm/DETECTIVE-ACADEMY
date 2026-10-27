"use client";
import { useEffect, useId, useRef, useState, type ReactNode } from "react";
import { createPortal } from "react-dom";
import { IconButton } from "./button";
import { XIcon } from "./icons";

/**
 * Bottom sheet on a phone, centred dialog from 640px. Modal: focus trap, Escape, scroll lock, aria-modal,
 * focus restore, and every other body child is made inert while open (so background content is hidden from AT too).
 */
export function Sheet({ open, onClose, title, closeLabel = "إغلاق", children, footer, dismissible = true }: { open: boolean; onClose: () => void; title: string; closeLabel?: string; children: ReactNode; footer?: ReactNode; dismissible?: boolean }) {
  const panel = useRef<HTMLDivElement>(null);
  const titleId = useId();
  const [node, setNode] = useState<HTMLDivElement | null>(null);
  useEffect(() => {
    const n = document.createElement("div");
    n.setAttribute("data-sheet-portal", "");
    document.body.appendChild(n);
    setNode(n);
    return () => { document.body.removeChild(n); };
  }, []);
  useEffect(() => {
    if (!open || !node) return;
    const sibs = Array.from(document.body.children).filter((el): el is HTMLElement => el instanceof HTMLElement && el !== node);
    const prev = sibs.map((el) => el.inert);
    sibs.forEach((el) => { el.inert = true; });
    return () => { sibs.forEach((el, i) => { el.inert = prev[i]!; }); };
  }, [open, node]);
  useEffect(() => {
    if (!open || !node) return;
    const before = document.activeElement as HTMLElement | null;
    const p = panel.current;
    p?.focus();
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape" && dismissible) { e.preventDefault(); onClose(); return; }
      if (e.key !== "Tab" || !p) return;
      const f = Array.from(p.querySelectorAll<HTMLElement>('a[href], button:not([disabled]), textarea, input:not([disabled]), select, [tabindex]:not([tabindex="-1"])')).filter((x) => x.offsetParent !== null || x === document.activeElement);
      if (!f.length) { e.preventDefault(); return; }
      const first = f[0]!, last = f[f.length - 1]!;
      if (e.shiftKey && (document.activeElement === first || document.activeElement === p)) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    };
    document.addEventListener("keydown", onKey);
    const ov = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => { document.removeEventListener("keydown", onKey); document.body.style.overflow = ov; before?.focus?.(); };
  }, [open, node, onClose, dismissible]);
  if (!open || !node) return null;
  return createPortal(
    <div className="sheet-root">
      <div className="sheet-scrim" onClick={dismissible ? onClose : undefined} aria-hidden />
      <div ref={panel} role="dialog" aria-modal="true" aria-labelledby={titleId} tabIndex={-1} className="sheet animate-rise">
        <span className="sheet-grip" aria-hidden />
        <div className="sheet-head">
          <h2 id={titleId} className="text-section-title">{title}</h2>
          {dismissible && <IconButton label={closeLabel} onClick={onClose}><XIcon /></IconButton>}
        </div>
        <div className="sheet-body">{children}</div>
        {footer && <div className="sheet-foot">{footer}</div>}
      </div>
    </div>,
    node,
  );
}
