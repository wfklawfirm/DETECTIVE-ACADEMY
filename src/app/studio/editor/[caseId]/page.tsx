"use client";
import { useCallback, useEffect, useRef, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { useMe } from "@/components/Shell";
import { Button, LinkButton } from "@/components/ui/button";
import { Callout, EmptyState, LoadingRegion } from "@/components/ui/feedback";
import { StudioIcon } from "@/components/ui/icons";
import { api, ApiError } from "@/lib/client";

interface DraftCover {
  title_ar: string;
  subtitle_ar: string;
  hook_ar: string;
  difficulty: string;
  setting_ar: string;
}

const DIFFICULTY_OPTIONS = [
  { value: "easy",   label: "سهلة" },
  { value: "medium", label: "متوسطة" },
  { value: "hard",   label: "صعبة" },
];

function EditableField({
  label, value, field, caseId, onSave,
}: {
  label: string; value: string; field: string; caseId: string; onSave: (field: string, val: string) => void;
}) {
  const [editing, setEditing] = useState(false);
  const [draft, setDraft]     = useState(value);
  const [saving, setSaving]   = useState(false);
  const [saved,  setSaved]    = useState(false);
  const ref = useRef<HTMLInputElement | HTMLSelectElement | null>(null);

  useEffect(() => { setDraft(value); }, [value]);
  useEffect(() => { if (editing && ref.current) ref.current.focus(); }, [editing]);

  const save = async () => {
    if (draft === value) { setEditing(false); return; }
    setSaving(true);
    try {
      await api("/api/studio/draft", { case_id: caseId, field, value: draft });
      onSave(field, draft);
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    } catch { /* ignore */ }
    setSaving(false);
    setEditing(false);
  };

  const isSelect = field === "cover.difficulty";
  return (
    <div className="editor-field">
      <label className="editor-field-label">{label}</label>
      <div className={`editor-field-row${editing ? " editing" : ""}`}>
        {editing ? (
          isSelect ? (
            <select ref={ref as React.Ref<HTMLSelectElement>} className="input" value={draft}
              onChange={(e) => setDraft(e.target.value)}
              onBlur={save}>
              {DIFFICULTY_OPTIONS.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
            </select>
          ) : (
            <input ref={ref as React.Ref<HTMLInputElement>} className="input" value={draft}
              onChange={(e) => setDraft(e.target.value)}
              onBlur={save}
              onKeyDown={(e) => { if (e.key === "Enter") { e.preventDefault(); void save(); } if (e.key === "Escape") setEditing(false); }} />
          )
        ) : (
          <span className="editor-field-value">{draft}</span>
        )}
        <button className="editor-pencil" onClick={() => setEditing(true)} aria-label="تعديل" type="button">✏️</button>
        {saving && <span className="editor-status dim-2">…</span>}
        {saved  && <span className="editor-status ok">✓ حُفظ</span>}
      </div>
    </div>
  );
}

export default function CaseEditor() {
  const { caseId } = useParams<{ caseId: string }>();
  const { me } = useMe();
  const [cover, setCover] = useState<DraftCover | null>(null);
  const [err,   setErr]   = useState<string | null>(null);
  const [loaded, setLoaded] = useState(false);

  const load = useCallback(async () => {
    try {
      const d = await api<{ cover: DraftCover }>(`/api/studio/draft?case_id=${caseId}`);
      setCover(d.cover);
    } catch (e) { setErr(e instanceof ApiError ? e.message : "خطأ في التحميل"); }
    setLoaded(true);
  }, [caseId]);

  useEffect(() => { if (me?.user) void load(); }, [me, load]);

  const handleSave = (field: string, val: string) => {
    const key = field.replace("cover.", "") as keyof DraftCover;
    setCover((c) => c ? { ...c, [key]: val } : c);
  };

  if (!me?.user || !["editor", "admin"].includes(me.user.role))
    return (
      <>
        <div className="ref-hero"><p className="ref-hero-kicker">استوديو</p><h1 className="ref-hero-title">محرر القضية</h1></div>
        <EmptyState icon={<StudioIcon size={28} />} title="للمحررين والمدراء فقط" action={<LinkButton variant="primary" href="/account?next=/studio">سجّل الدخول</LinkButton>} />
      </>
    );

  return (
    <>
      <div className="ref-hero">
        <p className="ref-hero-kicker">استوديو · محرر القضايا</p>
        <h1 className="ref-hero-title">تعديل: <code className="mono">{caseId}</code></h1>
        <p className="ref-hero-hook">انقر ✏️ بجانب أي حقل لتعديله — يُحفظ تلقائياً عند الخروج.</p>
      </div>

      <div className="row"><LinkButton href="/studio" variant="secondary">← العودة إلى الاستوديو</LinkButton></div>

      {err && <Callout tone="negative">{err}</Callout>}
      {!loaded && <LoadingRegion cards={1} />}

      {cover && (
        <div className="editor-card">
          <EditableField label="العنوان"          field="cover.title_ar"    caseId={caseId} value={cover.title_ar}    onSave={handleSave} />
          <EditableField label="العنوان الفرعي"  field="cover.subtitle_ar" caseId={caseId} value={cover.subtitle_ar} onSave={handleSave} />
          <EditableField label="الخطاف"           field="cover.hook_ar"     caseId={caseId} value={cover.hook_ar}     onSave={handleSave} />
          <EditableField label="الصعوبة"          field="cover.difficulty"  caseId={caseId} value={cover.difficulty}  onSave={handleSave} />
          <EditableField label="البيئة"            field="cover.setting_ar"  caseId={caseId} value={cover.setting_ar}  onSave={handleSave} />
        </div>
      )}
    </>
  );
}
