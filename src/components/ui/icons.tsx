import type { ReactNode, SVGProps } from "react";

/** One icon family: hand-rolled line icons, 24 viewBox, stroke 1.75, round caps/joins. Decorative by default. */
type P = Omit<SVGProps<SVGSVGElement>, "children"> & { size?: number; title?: string };
function Svg({ size = 24, title, children, ...rest }: P & { children: ReactNode }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.75} strokeLinecap="round" strokeLinejoin="round" aria-hidden={title ? undefined : true} role={title ? "img" : undefined} focusable="false" {...rest}>
      {title ? <title>{title}</title> : null}
      {children}
    </svg>
  );
}
export const HomeIcon = (p: P) => <Svg {...p}><path d="M4 11l8-7 8 7" /><path d="M6 10v9h12v-9" /><path d="M10 19v-5h4v5" /></Svg>;
export const FolderIcon = (p: P) => <Svg {...p}><path d="M3 7a2 2 0 012-2h4l2 2.5h8a2 2 0 012 2V17a2 2 0 01-2 2H5a2 2 0 01-2-2z" /></Svg>;
export const BookIcon = (p: P) => <Svg {...p}><path d="M5 4.5A1.5 1.5 0 016.5 3H19v15H6.5A1.5 1.5 0 005 19.5z" /><path d="M5 19.5A1.5 1.5 0 006.5 21H19v-3" /><path d="M9 8h6" /></Svg>;
export const LibraryIcon = (p: P) => <Svg {...p}><path d="M4 4v16" /><path d="M9 4v16" /><path d="M14.5 5.5l3.2-1 3.3 14.3-3.2 1z" /></Svg>;
export const ProfileIcon = (p: P) => <Svg {...p}><circle cx="12" cy="8.5" r="3.5" /><path d="M5 20c.7-3.6 3.5-5.5 7-5.5s6.3 1.9 7 5.5" /></Svg>;
export const MenuIcon = (p: P) => <Svg {...p}><path d="M4 7h16" /><path d="M4 12h16" /><path d="M4 17h16" /></Svg>;
export const XIcon = (p: P) => <Svg {...p}><path d="M6 6l12 12" /><path d="M18 6L6 18" /></Svg>;
export const CheckIcon = (p: P) => <Svg {...p}><path d="M5 12.5l4.5 4.5L19 7.5" /></Svg>;
/** Drawn pointing to inline-end in LTR; mirrors automatically under RTL via .flip-rtl. */
export const ChevronIcon = ({ className = "", ...p }: P) => <Svg className={`flip-rtl ${className}`} {...p}><path d="M9 5l7 7-7 7" /></Svg>;
/** Back arrow: points to inline-start (LTR: left); mirrors under RTL so it points right, toward where you came from. */
export const BackIcon = ({ className = "", ...p }: P) => <Svg className={`flip-rtl ${className}`} {...p}><path d="M19 12H5" /><path d="M11 6l-6 6 6 6" /></Svg>;
export const ArrowIcon = ({ className = "", ...p }: P) => <Svg className={`flip-rtl ${className}`} {...p}><path d="M5 12h14" /><path d="M13 6l6 6-6 6" /></Svg>;
export const LockIcon = (p: P) => <Svg {...p}><rect x="5" y="10.5" width="14" height="9.5" rx="2" /><path d="M8 10.5V8a4 4 0 018 0v2.5" /></Svg>;
export const AlertIcon = (p: P) => <Svg {...p}><path d="M12 4l9 15.5H3z" /><path d="M12 10v4" /><path d="M12 17h.01" /></Svg>;
export const InfoIcon = (p: P) => <Svg {...p}><circle cx="12" cy="12" r="9" /><path d="M12 11v5" /><path d="M12 7.8h.01" /></Svg>;
export const SearchIcon = (p: P) => <Svg {...p}><circle cx="10.5" cy="10.5" r="6" /><path d="M15 15l5 5" /></Svg>;
export const ClockIcon = (p: P) => <Svg {...p}><circle cx="12" cy="12" r="9" /><path d="M12 7v5l3.2 2" /></Svg>;
export const ScaleIcon = (p: P) => <Svg {...p}><path d="M12 4v16" /><path d="M7 20h10" /><path d="M5 7h14" /><path d="M5 7l-2.5 6a3 3 0 005 0z" /><path d="M19 7l-2.5 6a3 3 0 005 0z" /></Svg>;
export const PenIcon = (p: P) => <Svg {...p}><path d="M4 20l1-4L16.5 4.5a2 2 0 013 3L8 19z" /><path d="M14.5 6.5l3 3" /></Svg>;
export const UsersIcon = (p: P) => <Svg {...p}><circle cx="9" cy="8.5" r="3.2" /><path d="M3 19.5c.6-3.2 3-4.8 6-4.8s5.4 1.6 6 4.8" /><path d="M16 5.6a3.2 3.2 0 010 5.8" /><path d="M18 14.9c1.8.5 3 1.9 3.4 4.1" /></Svg>;
export const BoardIcon = (p: P) => <Svg {...p}><rect x="3.5" y="4" width="17" height="14" rx="2" /><circle cx="8.5" cy="9" r="1.2" /><circle cx="15.5" cy="13" r="1.2" /><path d="M9.2 9.7l5.1 2.6" /><path d="M9 21l1-3" /><path d="M15 21l-1-3" /></Svg>;
export const FileIcon = (p: P) => <Svg {...p}><path d="M6 3h8l4 4v14H6z" /><path d="M14 3v4h4" /><path d="M9 12h6" /><path d="M9 16h6" /></Svg>;
export const EvidenceIcon = (p: P) => <Svg {...p}><rect x="4" y="7" width="16" height="13" rx="2" /><path d="M8 7V5a1 1 0 011-1h6a1 1 0 011 1v2" /><path d="M4 12h16" /></Svg>;
export const FlaskIcon = (p: P) => <Svg {...p}><path d="M9.5 3h5" /><path d="M10.5 3v6L5 18.5A1.8 1.8 0 006.6 21h10.8a1.8 1.8 0 001.6-2.5L13.5 9V3" /><path d="M8 15h8" /></Svg>;
export const SparkIcon = (p: P) => <Svg {...p}><path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z" /></Svg>;
export const ImageIcon = (p: P) => <Svg {...p}><rect x="3.5" y="4.5" width="17" height="15" rx="2" /><circle cx="9" cy="10" r="1.6" /><path d="M20 16l-5-5-8 8" /></Svg>;
export const ShieldIcon = (p: P) => <Svg {...p}><path d="M12 3l7 3v5.5c0 4.3-2.9 7.7-7 9.5-4.1-1.8-7-5.2-7-9.5V6z" /><path d="M9.2 12l2 2 3.6-4" /></Svg>;
export const FlagIcon = (p: P) => <Svg {...p}><path d="M6 21V4" /><path d="M6 5h11l-2 4 2 4H6" /></Svg>;
export const SoundIcon = (p: P) => <Svg {...p}><path d="M4 10v4h3.5l4.5 3.5v-11L7.5 10z" /><path d="M15.5 9a4 4 0 010 6" /><path d="M18 6.5a7.5 7.5 0 010 11" /></Svg>;
export const LinkIcon = (p: P) => <Svg {...p}><path d="M10 14a4 4 0 005.7 0l3-3a4 4 0 00-5.7-5.7l-1 1" /><path d="M14 10a4 4 0 00-5.7 0l-3 3a4 4 0 005.7 5.7l1-1" /></Svg>;
export const SettingsIcon = (p: P) => <Svg {...p}><path d="M5 7h9" /><path d="M18 7h1" /><circle cx="16" cy="7" r="2" /><path d="M5 17h1" /><path d="M10 17h9" /><circle cx="8" cy="17" r="2" /></Svg>;
export const LogoutIcon = (p: P) => <Svg {...p}><path d="M14 4h4a2 2 0 012 2v12a2 2 0 01-2 2h-4" /><path d="M10 8l-4 4 4 4" /><path d="M6 12h10" /></Svg>;
export const StudioIcon = (p: P) => <Svg {...p}><path d="M4 20h4L19 9a2.8 2.8 0 00-4-4L4 16z" /><path d="M13 7l4 4" /></Svg>;
export const SunIcon = (p: P) => <Svg {...p}><circle cx="12" cy="12" r="4" /><path d="M12 3v2M12 19v2M3 12h2M19 12h2M5.6 5.6L7 7M17 17l1.4 1.4M5.6 18.4L7 17M17 7l1.4-1.4" /></Svg>;
export const RefreshIcon = (p: P) => <Svg {...p}><path d="M20 11a8 8 0 00-14-4.5L4 9" /><path d="M4 4v5h5" /><path d="M4 13a8 8 0 0014 4.5L20 15" /><path d="M20 20v-5h-5" /></Svg>;
export const TargetIcon = (p: P) => <Svg {...p}><circle cx="12" cy="12" r="8.5" /><circle cx="12" cy="12" r="4.5" /><circle cx="12" cy="12" r="0.8" /></Svg>;
