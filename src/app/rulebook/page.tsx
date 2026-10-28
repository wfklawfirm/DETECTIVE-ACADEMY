import { loadRulebook } from "@/engine/reference";
import { Badge } from "@/components/ui/badge";
import { Card, CardTitle } from "@/components/ui/card";
import { Callout } from "@/components/ui/feedback";
import { MoreReference, RefHead, RuleIcon, Section, SourcesBox } from "@/components/reference/parts";

export const metadata = { title: "دستور اللغز العادل" };
export const dynamic = "force-dynamic";

export default function Rulebook() {
  const r = loadRulebook();
  const n = r.sections.reduce((s, x) => s + x.rules.length, 0);
  return (
    <>
      <RefHead title="دستور اللغز العادل" hook={r.hook_ar} />
      <p className="small dim-2">{n} قاعدة في {r.sections.length} أقسام. هي قواعد كتابة نلتزم بها نحن، وتعني لك أن ما تحتاجه للحل موجود أمامك، وأن أحداً لن يُتَّهم بسبب مظهره، وأن العلم يُعرض بحدوده.</p>
      <nav aria-label="أقسام الصفحة" className="row small">
        {r.sections.map((s) => <a key={s.id} className="badge badge-outline" href={`#${s.id}`}>{s.title_ar}</a>)}
        <a className="badge badge-outline" href="#hints">كيف تعمل التلميحات</a>
      </nav>
      {r.sections.map((s) => (
        <Section key={s.id} id={s.id} title={s.title_ar}>
          <div className="row" style={{ flexWrap: "nowrap", alignItems: "center" }}><RuleIcon name={s.icon} /><p className="narrative grow">{s.plain_ar}</p></div>
          <ul className="list">
            {s.rules.map((x) => (
              <li key={x.code}>
                <Card flat as="article">
                  <div className="row" style={{ flexWrap: "nowrap", alignItems: "flex-start" }}>
                    <Badge outline latin dir="ltr" lang="en">{x.code}</Badge>
                    <p className="grow">{x.rule_ar}</p>
                  </div>
                  {x.breakable && <Badge tone="warning">قابلة للكسر بشروط</Badge>}
                  {x.origin_ar && <p className="small dim">أصلها: {x.origin_ar}</p>}
                </Card>
              </li>
            ))}
          </ul>
        </Section>
      ))}
      <Section id="breakable" title="متى تُكسر القاعدة؟" hook="أشهر الروايات خلدت لأنها كسرت قاعدة بوضوح. لكن الكسر هنا مكافأة للمتمرسين لا فخ للمبتدئين.">
        <ul className="stack-sm">{r.breakable_ar.map((x) => <li key={x}>{x}</li>)}</ul>
      </Section>

      <Section id="hints" title={r.hints.title_ar} hook="علقتَ؟ لا بأس. التلميح سؤال قبل أن يكون جواباً، ولكل درجة منه حدّ لا تتجاوزه.">
        <ol className="list" aria-label="درجات التلميح">
          {r.hints.ladder.map((h) => (
            <li key={h.level}>
              <Card flat>
                <div className="row" style={{ flexWrap: "nowrap", alignItems: "baseline" }}><Badge tone={h.level === 0 ? "positive" : h.level >= 4 ? "warning" : "info"}>الدرجة {h.level}</Badge><b className="grow">{h.name_ar}</b></div>
                <p className="small">{h.shows_ar}</p>
              </Card>
            </li>
          ))}
        </ol>
        <h3 className="text-label">قواعد السلّم</h3>
        <ul className="stack-sm">{r.hints.rules_ar.map((x) => <li key={x} className="small">{x}</li>)}</ul>
        <Callout tone="info" title="في أثر">{r.hints.product_note_ar}</Callout>
        <SourcesBox ids={r.hints.src_ids} />
      </Section>
      <MoreReference current="/rulebook" />
    </>
  );
}
