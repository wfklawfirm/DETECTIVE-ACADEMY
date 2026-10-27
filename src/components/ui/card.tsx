import Link from "next/link";
import type { ComponentProps, ElementType, HTMLAttributes, ReactNode } from "react";
import { cx } from "./button";
import { ChevronIcon } from "./icons";

export function Card({ as, className, raised, flat, ...rest }: HTMLAttributes<HTMLElement> & { as?: ElementType; raised?: boolean; flat?: boolean }) {
  const Tag = (as ?? "div") as ElementType;
  return <Tag className={cx("card", raised && "raised", flat && "card-flat", className)} {...rest} />;
}
export function CardTitle({ level = 2, className, ...rest }: HTMLAttributes<HTMLHeadingElement> & { level?: 2 | 3 | 4 }) {
  const Tag = (`h${level}`) as ElementType;
  return <Tag className={cx("card-title", className)} {...rest} />;
}
/** Whole-card tap target: a real link. */
export function CardLink({ className, children, ...rest }: ComponentProps<typeof Link>) {
  return <Link className={cx("card", "card-link", className)} {...rest}>{children}</Link>;
}
/** Uniform full-width navigation row. */
export function RowLink({ icon, title, hint, trailing, className, ...rest }: Omit<ComponentProps<typeof Link>, "title"> & { icon?: ReactNode; title: ReactNode; hint?: ReactNode; trailing?: ReactNode }) {
  return (
    <Link className={cx("row-link", className)} {...rest}>
      {icon && <span className="ico">{icon}</span>}
      <span className="grow"><b>{title}</b>{hint && <span className="small dim">{hint}</span>}</span>
      {trailing}
      <ChevronIcon className="chev" size={20} />
    </Link>
  );
}
/** Case-file dossier: a labelled tab sitting on top of a card. */
export function Dossier({ tab, children, className }: { tab: ReactNode; children: ReactNode; className?: string }) {
  return <div className={cx("dossier", className)}><span className="dossier-tab">{tab}</span>{children}</div>;
}
export function SectionTitle({ children, className, as: Tag = "h2" }: { children: ReactNode; className?: string; as?: ElementType }) {
  return <Tag className={cx("text-label section-title", className)}>{children}</Tag>;
}
export function PageHead({ title, lead, kicker }: { title: ReactNode; lead?: ReactNode; kicker?: ReactNode }) {
  return <header className="page-head">{kicker && <p className="kicker">{kicker}</p>}<h1 className="text-page-title">{title}</h1>{lead && <p className="text-supporting dim-2" style={{ fontSize: "0.9375rem" }}>{lead}</p>}</header>;
}
