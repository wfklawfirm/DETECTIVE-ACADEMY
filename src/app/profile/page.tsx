"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { allTokens, api } from "@/lib/client";

interface Row { ko_id: string; name_ar: string; level: number; cases: string[]; track: string | null }
const LV = ["لم يظهر بعد", "بداية", "ناشئ", "متمكّن", "متقدّم"];
export default function Profile() {
  const [d, setD] = useState<{ skills: Row[]; disclaimer_ar: string; submitted_cases: number } | null>(null);
  useEffect(() => { void api<typeof d>("/api/profile", { tokens: allTokens() }).then(setD); }, []);
  return (
    <div className="wrap-narrow stack">
      <h1>مهاراتي</h1>
      {!d ? <p className="dim">جارٍ التحميل…</p> : d.submitted_cases === 0 ? <><p>أكمل قضية لتظهر مهاراتك هنا.</p><Link className="btn primary" href="/cases">اختر قضية</Link></> : (
        <>
          <p className="card small">{d.disclaimer_ar}</p>
          {d.skills.map((s) => (
            <div key={s.ko_id} className="card"><div className="row" style={{ justifyContent: "space-between" }}><b>{s.name_ar}</b><span className="chip">{s.track ? `مسار ${s.track}` : ""}</span></div>
              <div className="meter" role="img" aria-label={`${LV[s.level]}`}><i style={{ inlineSize: `${(s.level / 4) * 100}%` }} /></div>
              <p className="small dim" style={{ margin: "6px 0 0" }}>{LV[s.level]} · من: {s.cases.join("، ")}</p></div>
          ))}
        </>
      )}
    </div>
  );
}
