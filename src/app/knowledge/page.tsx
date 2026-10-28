import { getActorFromCookies } from "@/server/auth";
import { loadKnowledge, visibleKos } from "@/engine/knowledge";
import { KnowledgeBrowser } from "@/components/KnowledgeBrowser";
import { REFERENCE_PAGES } from "@/engine/reference-labels";
import { RowLink } from "@/components/ui/card";
import { FlaskIcon, ImageIcon, LinkIcon, SparkIcon } from "@/components/ui/icons";

export const metadata = { title: "موسوعة المحقق" };
export const dynamic = "force-dynamic";

export default async function Knowledge() {
  const a = await getActorFromCookies();
  const { kos } = loadKnowledge();
  const items = visibleKos(kos, a.ageBand).map(
    ({ ko_id, type, name_ar, summary_ar, confidence, status, tags }) => ({
      ko_id, type, name_ar, summary_ar, confidence, status, tags,
    })
  );

  return (
    <>
      {/* ── Cinematic hero ──────────────────────────────────────── */}
      <header className="knowledge-hero">
        <div className="knowledge-hero-inner">
          <div className="knowledge-hero-text">
            <p className="knowledge-hero-kicker">موسوعة المحقق · مكتبة الاستدلال</p>
            <h1 className="knowledge-hero-title">موسوعة المحقق</h1>
            <p className="knowledge-hero-sub">
              مفاهيم من علم الأدلة ومهارات الاستدلال وأنماط الألغاز —
              مستخرجة من مكتبة Detective Academy البحثية.
            </p>
          </div>
          <div className="knowledge-hero-badge" aria-hidden>
            <span className="knowledge-hero-glyph">📚</span>
          </div>
        </div>

        {/* Warning strip */}
        <div className="knowledge-hero-warning">
          <span className="knowledge-warning-icon" aria-hidden>⚠️</span>
          <p className="small">
            <strong>مادة أولية:</strong> كل مادة تُظهر درجة الثقة وحالتها —
            «مبني على أدلة» أو «فرضية تصميم» أو «ممارسة مهنية». لم تُراجَع بعدُ
            من خبراء مستقلين، فاعتبرها مادة تعليمية أولية لا مرجعاً علمياً نهائياً.
          </p>
        </div>
      </header>

      {/* ── Quick links grid ───────────────────────────────────── */}
      <section className="knowledge-links-section" aria-label="روابط الموسوعة السريعة">
        <p className="knowledge-links-kicker">استكشف</p>
        <div className="knowledge-links-grid">
          <a href="/labs" className="knowledge-link-card">
            <span className="knowledge-link-icon" aria-hidden><FlaskIcon size={22} /></span>
            <div>
              <p className="knowledge-link-title">مختبرات آمنة</p>
              <p className="knowledge-link-hint">تمارين قصيرة بسجلات خيالية</p>
            </div>
          </a>
          <a href="/skills" className="knowledge-link-card">
            <span className="knowledge-link-icon" aria-hidden><SparkIcon size={22} /></span>
            <div>
              <p className="knowledge-link-title">المهارات وأنماط الألغاز</p>
              <p className="knowledge-link-hint">الإطار الذي نبني عليه القضايا</p>
            </div>
          </a>
          <a href="/sources" className="knowledge-link-card">
            <span className="knowledge-link-icon" aria-hidden><LinkIcon size={22} /></span>
            <div>
              <p className="knowledge-link-title">المصادر والحقوق</p>
              <p className="knowledge-link-hint">سجل المصادر والحقوق</p>
            </div>
          </a>
          <a href="/books" className="knowledge-link-card">
            <span className="knowledge-link-icon" aria-hidden><FlaskIcon size={22} /></span>
            <div>
              <p className="knowledge-link-title">مفاهيم الطب الشرعي</p>
              <p className="knowledge-link-hint">ملاحظات أصلية مع تدريبات قصيرة</p>
            </div>
          </a>
          <a href="/heritage" className="knowledge-link-card">
            <span className="knowledge-link-icon" aria-hidden><LinkIcon size={22} /></span>
            <div>
              <p className="knowledge-link-title">تراث الاستدلال</p>
              <p className="knowledge-link-hint">نصوص من الملك العام ومراجع الأدب البوليسي</p>
            </div>
          </a>
          <a href="/gallery" className="knowledge-link-card">
            <span className="knowledge-link-icon" aria-hidden><ImageIcon size={22} /></span>
            <div>
              <p className="knowledge-link-title">معرض المراجع</p>
              <p className="knowledge-link-hint">صور مرجعية من مجموعات مفتوحة</p>
            </div>
          </a>
          {REFERENCE_PAGES.map((r) => (
            <a key={r.href} href={r.href} className="knowledge-link-card">
              <span className="knowledge-link-icon" aria-hidden><SparkIcon size={22} /></span>
              <div>
                <p className="knowledge-link-title">{r.title}</p>
                <p className="knowledge-link-hint">{r.hint}</p>
              </div>
            </a>
          ))}
        </div>
      </section>

      {/* ── Knowledge browser ──────────────────────────────────── */}
      <KnowledgeBrowser items={items} />
    </>
  );
}
