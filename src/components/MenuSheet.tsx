"use client";
import Link from "next/link";
import type { Me } from "@/lib/client";
import { NAV } from "./Shell";
import { Sheet } from "./ui/sheet";
import { SegmentedControl, Toggle } from "./ui/form";
import { FlagIcon, FlaskIcon, ImageIcon, LinkIcon, ProfileIcon, ShieldIcon, SparkIcon, StudioIcon, TargetIcon, FileIcon } from "./ui/icons";
import { usePrefs, type ThemePref } from "./ui/prefs";

const MORE = [
  { href: "/challenges", label: "تحدي اليوم", Icon: TargetIcon },
  { href: "/season", label: "الموسم الأول", Icon: TargetIcon },
  { href: "/labs", label: "مختبرات آمنة", Icon: FlaskIcon },
  { href: "/glossary", label: "المسرد الجنائي", Icon: FileIcon },
  { href: "/heritage", label: "تراث الاستدلال", Icon: LinkIcon },
  { href: "/skills", label: "المهارات وأنماط الألغاز", Icon: SparkIcon },
  { href: "/sources", label: "المصادر والحقوق", Icon: LinkIcon },
  { href: "/gallery", label: "معرض المراجع", Icon: ImageIcon },
  { href: "/credits", label: "الاعتمادات", Icon: FileIcon },
];
const THEMES: { value: ThemePref; label: string }[] = [{ value: "dark", label: "داكن" }, { value: "light", label: "فاتح" }, { value: "system", label: "النظام" }];

export function MenuSheet({ open, onClose, path, me, staff }: { open: boolean; onClose: () => void; path: string; me: Me | null; staff: boolean }) {
  const p = usePrefs();
  const cur = (href: string) => (path === href || path.startsWith(href + "/") ? "page" : undefined);
  return (
    <Sheet open={open} onClose={onClose} title="القائمة">
      <nav className="menu-section" aria-label="الأقسام">
        <ul className="menu-nav">
          {NAV.map(({ href, label, Icon }) => <li key={href}><Link href={href} aria-current={cur(href)}><Icon size={22} />{label}</Link></li>)}
        </ul>
      </nav>
      <hr className="divider" />
      <nav className="menu-section" aria-label="المزيد">
        <ul className="menu-nav">
          {MORE.map(({ href, label, Icon }) => <li key={href}><Link href={href} aria-current={cur(href)}><Icon size={22} />{label}</Link></li>)}
          {staff && <li><Link href="/studio" aria-current={cur("/studio")}><StudioIcon size={22} />استوديو المحتوى</Link></li>}
          <li><Link href="/account" aria-current={cur("/account")}><ProfileIcon size={22} />{me?.user ? (me.user.display_name ?? "حسابي") : "الحساب وتسجيل الدخول"}</Link></li>
        </ul>
      </nav>
      <hr className="divider" />
      <section className="menu-section" aria-labelledby="menu-settings">
        <h3 id="menu-settings" className="text-label">المظهر والإعدادات</h3>
        <SegmentedControl label="السمة" name="theme" value={p.theme} onChange={(v) => p.setTheme(v as ThemePref)} options={THEMES} />
        <Toggle label="نص أكبر" hint="يكبّر الخط في كل الشاشات" checked={p.largeText} onChange={p.setLargeText} />
        <Toggle label="تقليل الحركة" hint="يوقف الحركات والتوهج" checked={p.reduceMotion} onChange={p.setReduceMotion} />
        <Toggle label="المؤثرات الصوتية" hint="مطفأة افتراضياً" checked={p.sfx} onChange={p.setSfxOn} />
      </section>
      <hr className="divider" />
      <ul className="menu-nav" aria-label="روابط">
        <li><Link href="/privacy" aria-current={cur("/privacy")}><ShieldIcon size={22} />الخصوصية والسلامة</Link></li>
        <li><Link href="/report" aria-current={cur("/report")}><FlagIcon size={22} />أبلِغ عن مشكلة</Link></li>
      </ul>
      <p className="small dim">Detective Academy · نموذج تجريبي. القصص كلها من تأليفنا وشخصياتها خيالية.</p>
    </Sheet>
  );
}
