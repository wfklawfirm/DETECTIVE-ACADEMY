"use client";
import type { Lab } from "@/engine/labs";
import { Classify } from "./labs/Classify";
import { Conclude } from "./labs/Conclude";
import { Match } from "./labs/Match";
import { Measure } from "./labs/Measure";
import { Order } from "./labs/Order";
import { Slider } from "./labs/Slider";
import { Spot } from "./labs/Spot";

interface FirstLesson { id: string; title_ar: string }

/** One data-driven runner: the lab's `kind` picks the interaction; content never changes the code path. */
export function LabRunner({ lab, firstLesson }: { lab: Lab; firstLesson?: FirstLesson | null }) {
  switch (lab.kind) {
    case "classify": return <Classify lab={lab} firstLesson={firstLesson} />;
    case "order": return <Order lab={lab} firstLesson={firstLesson} />;
    case "match": return <Match lab={lab} firstLesson={firstLesson} />;
    case "slider": return <Slider lab={lab} firstLesson={firstLesson} />;
    case "spot": return <Spot lab={lab} firstLesson={firstLesson} />;
    case "measure": return <Measure lab={lab} firstLesson={firstLesson} />;
    case "conclude": return <Conclude lab={lab} firstLesson={firstLesson} />;
  }
}
