"use client";
import type { Lab } from "@/engine/labs";
import { Classify } from "./labs/Classify";
import { Conclude } from "./labs/Conclude";
import { Match } from "./labs/Match";
import { Measure } from "./labs/Measure";
import { Order } from "./labs/Order";
import { Slider } from "./labs/Slider";
import { Spot } from "./labs/Spot";

/** One data-driven runner: the lab's `kind` picks the interaction; content never changes the code path. */
export function LabRunner({ lab }: { lab: Lab }) {
  switch (lab.kind) {
    case "classify": return <Classify lab={lab} />;
    case "order": return <Order lab={lab} />;
    case "match": return <Match lab={lab} />;
    case "slider": return <Slider lab={lab} />;
    case "spot": return <Spot lab={lab} />;
    case "measure": return <Measure lab={lab} />;
    case "conclude": return <Conclude lab={lab} />;
  }
}
