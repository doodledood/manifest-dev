// Expected facts are fixture-side; these experiments do not measure human UX.
import {
  associations,
  coVisibility,
  centerDistance,
  distance,
} from "../../claude-plugins/manifest-dev/skills/design/scripts/measurements.mjs";
import { describePixels } from "../../claude-plugins/manifest-dev/skills/design/scripts/pixels.mjs";
const entity = (x, y, w, h, font = 16, visible = true) => ({
  box: { x, y, width: w, height: h },
  fontSize: font,
  visible,
});
export function calibration() {
  // Caller owns the labelled relationship; cases deliberately vary target size.
  const associationsCases = [
    {
      id: "field-help",
      split: "train",
      label: entity(0, 0, 80, 20),
      owner: entity(0, 28, 180, 32),
      other: entity(240, 0, 100, 20),
      expectedOwner: true,
    },
    {
      id: "wide-return-path",
      split: "train",
      label: entity(0, 0, 80, 20),
      owner: entity(0, 24, 720, 44),
      other: entity(110, 0, 80, 20),
      expectedOwner: true,
    },
    {
      id: "distant-caption",
      split: "train",
      label: entity(0, 0, 70, 20),
      owner: entity(0, 220, 100, 40),
      other: entity(0, 28, 100, 40),
      expectedOwner: false,
    },
    {
      id: "compact-table",
      split: "train",
      label: entity(0, 0, 100, 18, 12),
      owner: entity(104, 0, 100, 18, 12),
      other: entity(280, 0, 120, 18, 12),
      expectedOwner: true,
    },
    {
      id: "slide-wide-evidence",
      split: "challenge",
      label: entity(0, 0, 120, 32, 28),
      owner: entity(0, 42, 820, 140),
      other: entity(200, 0, 80, 32),
      expectedOwner: true,
    },
    {
      id: "poster-far-source",
      split: "challenge",
      label: entity(0, 0, 150, 30, 24),
      owner: entity(0, 460, 300, 50),
      other: entity(0, 40, 150, 50),
      expectedOwner: false,
    },
    {
      id: "rtl-referent",
      split: "challenge",
      label: entity(700, 0, 90, 20),
      owner: entity(20, 26, 770, 44),
      other: entity(600, 0, 80, 20),
      expectedOwner: true,
    },
    {
      id: "connected-far-referent",
      split: "challenge",
      label: entity(0, 0, 60, 20),
      owner: entity(260, 0, 100, 40),
      other: entity(80, 0, 100, 40),
      expectedOwner: true,
      cue: "explicit connector; proximity is inapplicable",
    },
    {
      id: "diagram-container",
      split: "challenge",
      label: entity(0, 0, 50, 20),
      owner: entity(0, 24, 1000, 20),
      other: entity(75, 0, 30, 20),
      expectedOwner: true,
    },
  ];
  const scored = associationsCases.map((c) => {
    const e = { label: c.label, owner: c.owner, other: c.other };
    const r = associations(
      [{ from: "label", to: "owner", competitors: ["other"] }],
      e,
    )[0];
    return {
      id: c.id,
      split: c.split,
      expectedOwner: c.expectedOwner,
      baseline:
        centerDistance(c.label.box, c.owner.box) <
        centerDistance(c.label.box, c.other.box),
      refined: r.competitorMinusIntendedEm > 0,
      gapEm: r.gapInLabelEm,
      marginEm: r.competitorMinusIntendedEm,
    };
  });
  const score = (cases, key) => ({
    correct: cases.filter((c) => c[key] === c.expectedOwner).length,
    total: cases.length,
  });
  // Search interpretation thresholds on train only; preserve challenge failures.
  const train = scored.filter((c) => c.split === "train"),
    hold = scored.filter((c) => c.split === "challenge");
  const search = [0, 0.25, 0.5, 1, 2, 3, 4, 8].map((cutoff) => ({
    cutoff,
    correct: train.filter((c) => c.gapEm <= cutoff === c.expectedOwner).length,
    total: train.length,
  }));
  const selected = [...search].sort(
    (a, b) => b.correct - a.correct || a.cutoff - b.cutoff,
  )[0];
  const thresholdChallenge = hold.map((c) => ({
    id: c.id,
    predicted: c.gapEm <= selected.cutoff,
    expected: c.expectedOwner,
  }));
  const viewport = { x: 0, y: 0, width: 300, height: 200 };
  const visibilityCases = [
    {
      id: "normal",
      split: "train",
      item: entity(20, 20, 80, 30),
      expected: true,
    },
    {
      id: "page-overflow",
      split: "train",
      item: entity(20, 220, 80, 30),
      expected: false,
    },
    {
      id: "hidden",
      split: "train",
      item: entity(20, 20, 80, 30, 16, false),
      expected: false,
    },
    {
      id: "ancestor-clipped",
      split: "challenge",
      item: {
        ...entity(20, 100, 80, 30),
        visibleBox: { x: 20, y: 100, width: 80, height: 0 },
      },
      expected: false,
    },
    {
      id: "partially-clipped",
      split: "challenge",
      item: {
        ...entity(20, 20, 80, 30),
        visibleBox: { x: 20, y: 20, width: 40, height: 30 },
      },
      expected: false,
    },
    {
      id: "shifted-group",
      split: "challenge",
      item: entity(280, 20, 80, 30),
      expected: false,
    },
  ].map((c) => ({
    id: c.id,
    split: c.split,
    expected: c.expected,
    baseline:
      c.item.visible &&
      c.item.box.width <= viewport.width &&
      c.item.box.height <= viewport.height,
    refined: coVisibility(
      [{ id: "fact", members: ["item"] }],
      { item: c.item },
      viewport,
    )[0].allFullyVisibleNow,
  }));
  const visibilityScore = (cases, key) => ({
    correct: cases.filter((c) => c[key] === c.expected).length,
    total: cases.length,
  });
  const pixels = [];
  for (const split of ["train", "challenge"])
    for (const kind of split === "train"
      ? ["uniform", "vertical-lines", "horizontal-lines"]
      : ["checkerboard", "low-contrast-checkerboard", "uniform"]) {
      const data = [];
      for (let y = 0; y < 16; y++)
        for (let x = 0; x < 16; x++) {
          const on =
            kind === "uniform"
              ? false
              : kind === "vertical-lines"
                ? x % 4 < 2
                : kind === "horizontal-lines"
                  ? y % 4 < 2
                  : (x + y) % 2 === 0;
          const v = on
            ? kind === "low-contrast-checkerboard"
              ? 136
              : 255
            : 128;
          data.push(v, v, v, 255);
        }
      let baseline = 0;
      for (let y = 1; y < 15; y++)
        for (let x = 1; x < 15; x++) {
          const at = (x, y) => data[(y * 16 + x) * 4] / 255;
          baseline += Math.hypot(
            (at(x + 1, y) - at(x - 1, y)) / 2,
            (at(x, y + 1) - at(x, y - 1)) / 2,
          );
        }
      const refined = describePixels(data, 16, 16, { threshold: 0.01 });
      pixels.push({
        id: `${split}-${kind}`,
        split,
        expectedVariation: kind !== "uniform",
        baselineVariation: baseline > 0,
        refinedVariation: refined.meanGradient > 0,
        meanGradient: refined.meanGradient,
      });
    }
  return {
    evidence:
      "Constructed known-relation observations. No participants, measured task speed, preference or general UX-quality validation.",
    association: {
      target:
        "Caller-labelled relationships in curated proximity examples and a connector exception. Independent semantic ownership comes from the fixture, not from the distance calculation; no human comprehension is measured.",
      baseline: "Center distance",
      refinement:
        "Boundary gap relative to named competitors in label em; endpoint visibility is exposed separately.",
      cases: scored,
      train: {
        baseline: score(train, "baseline"),
        refined: score(train, "refined"),
      },
      challenge: {
        baseline: score(hold, "baseline"),
        refined: score(hold, "refined"),
      },
      thresholdSearch: {
        search,
        selected,
        challenge: thresholdChallenge,
        disposition:
          "WITHHELD as a general grouping threshold: fitted to constructed training layouts; enclosure, optical ink, connectors, scale and genre can change interpretation.",
      },
    },
    visibility: {
      target:
        "Named box fully in viewport and not clipped by a declared ancestor.",
      baseline: "Dimension/visibility flags only",
      refinement:
        "Viewport intersection plus ancestor clip intersection, separate dimensional fit and observed visibility.",
      cases: visibilityCases,
      train: {
        baseline: visibilityScore(
          visibilityCases.filter((c) => c.split === "train"),
          "baseline",
        ),
        refined: visibilityScore(
          visibilityCases.filter((c) => c.split === "train"),
          "refined",
        ),
      },
      challenge: {
        baseline: visibilityScore(
          visibilityCases.filter((c) => c.split === "challenge"),
          "baseline",
        ),
        refined: visibilityScore(
          visibilityCases.filter((c) => c.split === "challenge"),
          "refined",
        ),
      },
      disposition:
        "Descriptive box observation retained; internal glyph clipping and paint occlusion need independent inspection.",
    },
    image: {
      target: "Detect adjacent-pixel variation in constructed patterns.",
      baseline: "Centered derivative",
      refinement:
        "Forward adjacent differences, bounded downsampling and explicit local normalization.",
      cases: pixels,
      disposition:
        "Pixel descriptor retained. Complexity, gaze and beauty predictors withheld; tuning the edge threshold does not establish UX quality.",
    },
    unfit: [
      "Global word-count minimization",
      "Global edge-density minimization",
      "Global animation-count minimization",
      "Shortest declared path as service quality",
      "Flat text contrast as categorical discriminability",
      "Training-fit spacing threshold as universal grouping",
    ],
  };
}
export const attacks = [
  {
    id: "clipped-facts",
    family: "dashboard",
    metric: "Document overflow/visible count",
    temptingEdit: "Use overflow:hidden to eliminate page overflow.",
    independentFact: "Required exception text must remain available.",
    outcome: "harmful",
    correction:
      "Inspect named clipping and actual content, not page overflow alone.",
  },
  {
    id: "tiny-type",
    family: "deck",
    metric: "Co-visibility",
    temptingEdit: "Shrink all type until everything fits.",
    independentFact:
      "The declared viewing context still requires legible content; no automatic font floor is inferred.",
    outcome: "context-dependent",
    correction:
      "Keep physical size/angle and actual render beside co-visibility.",
  },
  {
    id: "missing-qualification",
    family: "article",
    metric: "Word count",
    temptingEdit: "Delete the study limitation.",
    independentFact: "The adoption decision depends on the trial limitation.",
    outcome: "harmful",
    correction:
      "Reject the lower-count candidate; preserve semantic requirements.",
  },
  {
    id: "plot-width-drift",
    family: "chart",
    metric: "Declared source/display equality",
    temptingEdit: "Leave each row with a different plot width.",
    independentFact:
      "Equal values must map to equal lengths under the declared common scale.",
    outcome: "harmful",
    correction:
      "Measure common plot geometry and independently obtained mark positions.",
  },
  {
    id: "fake-route",
    family: "form",
    metric: "Shortest declared path",
    temptingEdit: "Add a direct saved edge to the supplied graph.",
    independentFact:
      "The actual failed save must preserve input and support recovery.",
    outcome: "harmful",
    correction:
      "Use an executed scenario; declaration is not observed behavior.",
  },
  {
    id: "one-tap-only",
    family: "game",
    metric: "First action succeeds",
    temptingEdit: "Ignore repeated actions.",
    independentFact: "Every repeated tap must update the count.",
    outcome: "harmful",
    correction: "Probe second and third use, not only first-frame feedback.",
  },
  {
    id: "monochrome-series",
    family: "chart",
    metric: "Text contrast",
    temptingEdit: "Give all category lines one high-contrast color.",
    independentFact:
      "The relevant categories must remain distinguishable through available channels.",
    outcome: "context-dependent",
    correction:
      "Use relevant pair topology and labels/shapes, not a contrast total.",
  },
  {
    id: "image-only-cta",
    family: "email",
    metric: "Low DOM word count",
    temptingEdit: "Put the action label only in an image.",
    independentFact:
      "The action must remain available with media hidden in the declared stress condition.",
    outcome: "harmful",
    correction:
      "Inspect images-off and candidate names/actual pointer reception.",
  },
  {
    id: "premature-rounding",
    family: "explorable",
    metric: "Short clean output",
    temptingEdit:
      "Round the input before computing and leave the basis unchanged.",
    independentFact:
      "At 333 L/min, result and displayed flow must derive from the same full-precision state.",
    outcome: "harmful",
    correction:
      "Check independent formula values and invalid-input preservation.",
  },
  {
    id: "hidden-print-text",
    family: "report",
    metric: "Good screen layout",
    temptingEdit: "Clip sections in print CSS.",
    independentFact: "The exported PDF must preserve the report sections.",
    outcome: "harmful",
    correction:
      "Inspect actual print output; screen observations do not clear pagination.",
  },
  {
    id: "fine-pattern",
    family: "poster",
    metric: "Centered edge energy",
    temptingEdit: "Use alternating one-pixel patterns.",
    independentFact:
      "A patterned image contains variation even if centered differences cancel.",
    outcome: "harmful",
    correction: "Change derivative; inspect aliasing at the analysis size.",
  },
  {
    id: "instant-text",
    family: "explainer",
    metric: "Reading rate",
    temptingEdit: "Set a nonempty text event duration to zero.",
    independentFact:
      "The essential qualification has zero exposure, not a favorable reading rate.",
    outcome: "harmful",
    correction: "Return undefined rate for zero exposure.",
  },
  {
    id: "hidden-hit-box",
    family: "rtl",
    metric: "Control box area",
    temptingEdit: "Expand an invisible box while keeping the affordance tiny.",
    independentFact:
      "The control must be locatable and operable through the supplied paths.",
    outcome: "context-dependent",
    correction:
      "Keep visible affordance, pointer samples and keyboard behavior separate.",
  },
  {
    id: "fabricated-survey",
    family: "poster",
    metric: "High satisfaction mean",
    temptingEdit: "Substitute model guesses for audience responses.",
    independentFact: "No participants were recruited in this run.",
    outcome: "invalid-evidence",
    correction:
      "Label constructed/model evidence; do not claim human outcomes.",
  },
];
