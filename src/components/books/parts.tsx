import { PageHead } from "../ui/card";
import { Callout } from "../ui/feedback";
import { SearchIcon } from "../ui/icons";

export const BOOKS_NOTE = "هذه ملاحظات مفاهيم بصياغتنا عن كتب محمية بحقوق النشر؛ لا ننقل نصوصها. لم تُراجَع بعدُ من خبراء ولا من مدقق لغوي ناطق بالعربية، فاعتبرها مادة تعليمية أولية.";

/** Every books page opens with the same shape: title, a one-line mystery hook, then the provenance note. */
export function BooksHead({ title, hook, kicker = "مكتبة الكتب", note = true }: { title: string; hook: string; kicker?: string; note?: boolean }) {
  return (
    <>
      <PageHead title={title} kicker={kicker} />
      <aside className="lead-card animate-rise" aria-label="خيط الصفحة">
        <span className="mark"><SearchIcon size={18} />خيط</span>
        <p>{hook}</p>
      </aside>
      {note && <Callout tone="warning" title="مادة أولية">{BOOKS_NOTE}</Callout>}
    </>
  );
}
