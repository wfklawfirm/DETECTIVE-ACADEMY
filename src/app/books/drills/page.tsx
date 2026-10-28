import { getActorFromCookies } from "@/server/auth";
import { drillsFor, loadBooks } from "@/engine/books";
import { BooksHead } from "@/components/books/parts";
import { DrillRunner } from "@/components/books/DrillRunner";

export const metadata = { title: "تمارين استدلال المشهد" };
export const dynamic = "force-dynamic";

export default async function Drills() {
  const a = await getActorFromCookies();
  const { drills } = loadBooks();
  const items = drillsFor(drills, a.ageBand).map(({ id, skill, scenario_ar, question_ar, options, answer_id, explanation_ar }) => ({ id, skill, scenario_ar, question_ar, options, answer_id, explanation_ar }));
  return (
    <>
      <BooksHead title="تمارين استدلال المشهد" hook="مشاهد خيالية قصيرة، وجواب واحد هو الأدق: افحص ما تراه قبل أن تحكم." kicker="تمرين" />
      <DrillRunner drills={items} />
    </>
  );
}
