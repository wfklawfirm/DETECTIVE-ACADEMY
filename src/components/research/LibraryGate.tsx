import type { ReactNode } from "react";
import { getActorFromCookies, type Actor } from "@/server/auth";
import { libraryAccess } from "@/engine/research";
import { LinkButton } from "@/components/ui/button";
import { PageHead } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/feedback";
import { StudioIcon } from "@/components/ui/icons";

/** Server-side admin gate for the research library: renders nothing from the library unless the viewer is an admin. */
export async function LibraryGate({ next, children }: { next: string; children: (actor: Actor) => ReactNode | Promise<ReactNode> }) {
  const actor = await getActorFromCookies();
  const a = libraryAccess(actor);
  if (a === "ok") return <>{await children(actor)}</>;
  return (
    <>
      <PageHead title="المكتبة البحثية" />
      <EmptyState icon={<StudioIcon size={28} />} title={a === "login" ? "للمدير فقط: سجّل الدخول" : "هذه المكتبة للمدير فقط"} body="تضم المكتبة وثائق داخلية (منافسون، استراتيجية، تخطيط) ولا تُعرض للعموم."
        action={a === "login" ? <LinkButton variant="primary" href={`/account?next=${encodeURIComponent(next)}`}>سجّل الدخول</LinkButton> : undefined} />
    </>
  );
}
