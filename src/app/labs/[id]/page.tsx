import Link from "next/link";
import { notFound } from "next/navigation";
import { loadLabs } from "@/engine/labs";
import { LabRunner } from "@/components/LabRunner";

export const dynamic = "force-dynamic";

export default async function LabPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const lab = loadLabs().playable.find((l) => l.id === id);
  if (!lab) notFound();
  return (
    <div className="wrap-narrow stack">
      <p className="kicker"><Link href="/labs">المختبرات</Link> · {lab.skill_ar}</p>
      <h1>{lab.title_ar}</h1>
      <p>{lab.intro_ar}</p>
      <LabRunner lab={lab} />
    </div>
  );
}
