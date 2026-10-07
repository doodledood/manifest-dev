// Descriptive measurements. Interpretation belongs to the caller's task.
export const VERSION = "1.0.0";
export const finite = (v, name) => {
  if (typeof v !== "number" || !Number.isFinite(v))
    throw new Error(`${name} must be a finite number`);
  return v;
};
export function object(value, name) {
  if (!value || Array.isArray(value) || typeof value !== "object")
    throw new Error(`${name} must be an object`);
  return value;
}
export function array(value, name) {
  if (!Array.isArray(value)) throw new Error(`${name} must be an array`);
  return value;
}
export function named(items, name) {
  array(items, name);
  const ids = new Set();
  for (const item of items) {
    object(item, `${name} item`);
    if (typeof item.id !== "string" || !item.id || ids.has(item.id))
      throw new Error(`${name} ids must be unique nonempty strings`);
    ids.add(item.id);
  }
  return ids;
}
export const mean = (a) =>
  a.length ? a.reduce((s, v) => s + v, 0) / a.length : null;
export const distance = (a, b) =>
  Math.hypot(
    Math.max(a.x - (b.x + b.width), b.x - (a.x + a.width), 0),
    Math.max(a.y - (b.y + b.height), b.y - (a.y + a.height), 0),
  );
export const centerDistance = (a, b) =>
  Math.hypot(
    a.x + a.width / 2 - b.x - b.width / 2,
    a.y + a.height / 2 - b.y - b.height / 2,
  );
export const intersection = (a, b) =>
  Math.max(0, Math.min(a.x + a.width, b.x + b.width) - Math.max(a.x, b.x)) *
  Math.max(0, Math.min(a.y + a.height, b.y + b.height) - Math.max(a.y, b.y));
export const linear = (c) =>
  c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
export const encoded = (c) =>
  c <= 0.0031308 ? 12.92 * c : 1.055 * c ** (1 / 2.4) - 0.055;
export function rgb(value) {
  const m = value?.match(
    /^rgba?\((\d+(?:\.\d+)?),\s*(\d+(?:\.\d+)?),\s*(\d+(?:\.\d+)?)(?:,\s*([\d.]+))?\)$/,
  );
  if (!m) return null;
  const channels = [+m[1], +m[2], +m[3]],
    alpha = m[4] === undefined ? 1 : +m[4];
  if (channels.some((v) => v > 255) || alpha < 0 || alpha > 1) return null;
  return [...channels.map((v) => v / 255), alpha];
}
export const luminance = (c) =>
  0.2126 * linear(c[0]) + 0.7152 * linear(c[1]) + 0.0722 * linear(c[2]);
export function contrast(a, b) {
  const x = luminance(a),
    y = luminance(b);
  return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05);
}

export function associations(links, entities) {
  return links.map((link) => {
    const a = entities[link.from],
      b = entities[link.to];
    const candidates = (link.competitors || []).map((id) => ({
      id,
      gap: distance(a.box, entities[id].box),
    }));
    candidates.sort((x, y) => x.gap - y.gap);
    const gap = distance(a.box, b.box),
      scale =
        typeof a.fontSize === "number" && a.fontSize > 0 ? a.fontSize : null;
    return {
      id: link.id || `${link.from} → ${link.to}`,
      from: link.from,
      to: link.to,
      endpointVisibility: { from: a.visible, to: b.visible },
      intendedGapPx: gap,
      gapInLabelEm: scale ? gap / scale : null,
      baselineCenterDistancePx: centerDistance(a.box, b.box),
      closestCompetitor: candidates[0] || null,
      competitorMinusIntendedEm:
        candidates.length && scale ? (candidates[0].gap - gap) / scale : null,
      limits:
        "Geometry describes proximity, not whether a relationship is understood. Competing elements must be named by the caller.",
    };
  });
}
export function coVisibility(groups, entities, viewport) {
  return groups.map((g) => {
    const members = g.members.map((id) => ({ id, ...entities[id] }));
    const full = members.filter(
      (e) =>
        e.visible &&
        e.visibleBox &&
        e.box.width > 0 &&
        e.box.height > 0 &&
        intersection(e.visibleBox, viewport) >=
          e.box.width * e.box.height - 0.01,
    );
    const bounds = {
      x: members.reduce((v, e) => Math.min(v, e.box.x), Infinity),
      y: members.reduce((v, e) => Math.min(v, e.box.y), Infinity),
    };
    bounds.width =
      members.reduce((v, e) => Math.max(v, e.box.x + e.box.width), -Infinity) -
      bounds.x;
    bounds.height =
      members.reduce((v, e) => Math.max(v, e.box.y + e.box.height), -Infinity) -
      bounds.y;
    return {
      id: g.id,
      members: g.members,
      fullyVisible: full.map((e) => e.id),
      unmeasuredAncestorClipping: members
        .filter((e) => !e.visibleBox)
        .map((e) => e.id),
      fullyWithinViewport: members
        .filter(
          (e) =>
            e.box.width > 0 &&
            e.box.height > 0 &&
            intersection(e.box, viewport) >= e.box.width * e.box.height - 0.01,
        )
        .map((e) => e.id),
      hidden: members.filter((e) => !e.visible).map((e) => e.id),
      clippedContentCandidates: members
        .filter((e) => e.contentClipCandidate)
        .map((e) => e.id),
      bounds,
      boundsFitViewport:
        bounds.width <= viewport.width && bounds.height <= viewport.height,
      allFullyVisibleNow:
        full.length === members.length
          ? true
          : members.some(
                (e) =>
                  !e.visible ||
                  !e.box.width ||
                  !e.box.height ||
                  intersection(e.visibleBox || e.box, viewport) <
                    e.box.width * e.box.height - 0.01,
              )
            ? false
            : null,
      verticalSpanInViewports: bounds.height / viewport.height,
      limits:
        "Named information, CSS boxes and ancestor clipping. Does not detect every paint occlusion or internal clipped glyph, or establish the usefulness of simultaneous visibility.",
    };
  });
}
export function textSummary(nodes) {
  const counts = new Map();
  const entries = nodes.map((n) => {
    const words = n.text.trim().split(/\s+/u).filter(Boolean).length;
    counts.set(n.text, (counts.get(n.text) || 0) + 1);
    return {
      id: n.id,
      text: n.text,
      words,
      characters: [...n.text].length,
      lines: n.lines,
      meanCharactersPerLineEstimate: n.lines
        ? [...n.text].length / n.lines
        : null,
      fontSizePx: n.fontSize,
      lineHeight: n.lineHeight,
      font: n.font,
      weight: n.weight,
      box: n.box,
      visible: n.visible,
    };
  });
  return {
    entries,
    totalWords: entries.reduce((s, n) => s + n.words, 0),
    repeatedStrings: [...counts]
      .filter(([, n]) => n > 1)
      .map(([text, count]) => ({ text, count })),
    limits:
      "Text-node counts and estimated line measures are not comprehension, redundancy, reading level or a recommended word budget.",
  };
}
export function colorSamples(nodes) {
  const measured = [],
    unmeasured = [];
  for (const n of nodes) {
    const a = rgb(n.color),
      backgrounds = n.backgrounds.map(rgb);
    let b = null,
      reason = null;
    if (n.paintEffects.length) reason = n.paintEffects.join(", ");
    if (!a || a[3] !== 1)
      reason = reason || "unsupported or translucent foreground";
    if (!reason)
      for (const c of backgrounds) {
        if (!c) {
          reason = "unsupported background color";
          break;
        }
        if (c[3] === 0) continue;
        if (c[3] !== 1) {
          reason = "translucent background";
          break;
        }
        b = c;
        break;
      }
    if (!b) reason = reason || "no known opaque background";
    if (reason) unmeasured.push({ id: n.id, reason });
    else
      measured.push({
        id: n.id,
        text: n.text,
        ratio: contrast(a, b),
        fontSizePx: n.fontSize,
        weight: n.weight,
        largeText: !Number.isFinite(n.fontSize)
          ? null
          : n.fontSize >= 24
            ? true
            : n.fontSize < (14 * 96) / 72
              ? false
              : n.weight !== undefined && Number.isFinite(Number(n.weight))
                ? Number(n.weight) >= 700
                : null,
      });
  }
  return {
    measured,
    unmeasured,
    limits:
      "Opaque DOM text samples only. No certification of overlapping paint, pseudo-elements, SVG/canvas, exceptions or unvisited states.",
  };
}
export function journey(graph) {
  object(graph, "journey");
  if (
    !Array.isArray(graph.nodes) ||
    !Array.isArray(graph.edges) ||
    !Array.isArray(graph.tasks)
  )
    throw new Error("journey needs nodes, edges and tasks arrays");
  const ids = named(graph.nodes, "journey nodes");
  for (const e of graph.edges) {
    object(e, "journey edge");
    if (!ids.has(e.from) || !ids.has(e.to))
      throw new Error("journey edge names an unknown node");
    finite(e.cost ?? 1, "edge cost");
    if ((e.cost ?? 1) < 0) throw new Error("edge cost must be nonnegative");
  }
  return graph.tasks.map((t) => {
    object(t, "journey task");
    if (!ids.has(t.from) || !ids.has(t.to))
      throw new Error("journey task names an unknown node");
    const costs = new Map([[t.from, 0]]),
      paths = new Map([[t.from, [t.from]]]),
      todo = new Set(ids);
    while (todo.size) {
      const a = [...todo]
        .filter((x) => costs.has(x))
        .sort((x, y) => costs.get(x) - costs.get(y))[0];
      if (a === undefined) break;
      todo.delete(a);
      for (const e of graph.edges.filter((e) => e.from === a)) {
        const c = costs.get(a) + (e.cost ?? 1);
        if (c < (costs.get(e.to) ?? Infinity)) {
          costs.set(e.to, c);
          paths.set(e.to, [...paths.get(a), e.to]);
        }
      }
    }
    const path = paths.get(t.to) || null;
    return {
      id: t.id || `${t.from} → ${t.to}`,
      reachable: !!path,
      minimumDeclaredCost: costs.get(t.to) ?? null,
      path,
      limits:
        "A caller-declared graph, not observed discoverability, human action time or cognitive effort.",
    };
  });
}
export function fidelity(spec) {
  object(spec, "data");
  named(spec.series, "data series");
  return spec.series.map((s) => {
    if (!Array.isArray(s.source) || !Array.isArray(s.display))
      throw new Error("series needs source and display arrays");
    s.source.forEach((v) => finite(v, "source value"));
    s.display.forEach((v) => finite(v, "display value"));
    const differences = [];
    for (let i = 0; i < Math.max(s.source.length, s.display.length); i++)
      if (s.source[i] !== s.display[i])
        differences.push({
          index: i,
          source: s.source[i] ?? null,
          display: s.display[i] ?? null,
        });
    if (s.axis && (!Array.isArray(s.axis) || s.axis.length !== 2))
      throw new Error("axis needs exactly two values");
    const extent = s.axis
      ? {
          minimum: finite(s.axis[0], "axis minimum"),
          maximum: finite(s.axis[1], "axis maximum"),
        }
      : null;
    if (extent && extent.maximum <= extent.minimum)
      throw new Error("axis maximum must exceed minimum");
    const marks = s.marks
      ? array(s.marks, "marks").map((m) => {
          object(m, "mark");
          if (!extent || !Array.isArray(s.axisPx) || s.axisPx.length !== 2)
            throw new Error("marks need axis and axisPx endpoints");
          const p0 = finite(s.axisPx[0], "axis pixel start"),
            p1 = finite(s.axisPx[1], "axis pixel end");
          const value = finite(m.value, "mark value"),
            position = finite(m.position, "mark position");
          const expected =
            p0 +
            ((value - extent.minimum) / (extent.maximum - extent.minimum)) *
              (p1 - p0);
          return {
            value,
            position,
            expectedPosition: expected,
            positionErrorPx: position - expected,
          };
        })
      : null;
    const proportional = s.proportional
      ? (() => {
          const q = object(s.proportional, "proportional encoding");
          if (!["length", "area", "count"].includes(q.kind))
            throw new Error("proportional kind must be length|area|count");
          const referenceValue = finite(q.referenceValue, "referenceValue"),
            referenceAmount = finite(q.referenceAmount, "referenceAmount");
          if (referenceValue <= 0 || referenceAmount <= 0)
            throw new Error("proportional reference must be positive");
          if (
            q.observedQuantity &&
            !["amount", "radius"].includes(q.observedQuantity)
          )
            throw new Error("observedQuantity must be amount|radius");
          if (q.observedQuantity === "radius" && q.kind !== "area")
            throw new Error("radius observation requires area encoding");
          return {
            kind: q.kind,
            observedQuantity: q.observedQuantity || "amount",
            marks: array(q.marks, "proportional marks").map((m) => {
              object(m, "proportional mark");
              const value = finite(m.value, "mark value"),
                amount = finite(m.amount, "mark amount");
              if (value < 0 || amount < 0)
                throw new Error(
                  "proportional values and amounts must be nonnegative",
                );
              const expectedAmount =
                referenceAmount *
                (q.observedQuantity === "radius"
                  ? Math.sqrt(value / referenceValue)
                  : value / referenceValue);
              return {
                value,
                amount,
                expectedAmount,
                error: amount - expectedAmount,
              };
            }),
          };
        })()
      : null;
    return {
      id: s.id,
      marks,
      proportional,
      differences,
      units: s.units || null,
      sourceReference: s.sourceReference || null,
      axis: extent,
      sourceRange: s.source.length
        ? [
            s.source.reduce((m, v) => Math.min(m, v), Infinity),
            s.source.reduce((m, v) => Math.max(m, v), -Infinity),
          ]
        : null,
      valuesOutsideAxis: extent
        ? s.source.filter((v) => v < extent.minimum || v > extent.maximum)
        : null,
      zeroIncluded: extent ? extent.minimum <= 0 && extent.maximum >= 0 : null,
      limits:
        "Checks declared numbers, declared mark coordinates on a linear scale, not extraction from rendered marks or truth of the supplied source. Zero is contextual to the encoding.",
    };
  });
}
export function timeline(spec) {
  object(spec, "timeline");
  named(spec.events, "timeline events");
  if (spec.links) array(spec.links, "timeline links");
  const events = spec.events.map((e) => {
    const start = finite(e.start, "event start"),
      end = finite(e.end, "event end");
    if (start < 0 || end < start)
      throw new Error("timeline event interval invalid");
    return { ...e, start, end };
  });
  const relations = (spec.links || []).map((l) => {
    object(l, "timeline link");
    const a = events.find((e) => e.id === l.from),
      b = events.find((e) => e.id === l.to);
    if (!a || !b) throw new Error("timeline link names an unknown event");
    return {
      from: l.from,
      to: l.to,
      overlapMs: Math.max(
        0,
        Math.min(a.end, b.end) - Math.max(a.start, b.start),
      ),
      gapMs: Math.max(0, a.start - b.end, b.start - a.end),
    };
  });
  return {
    events: events.map((e) => ({
      ...e,
      durationMs: e.end - e.start,
      wordsPerSecond:
        typeof e.text === "string" && e.text.trim() && e.end > e.start
          ? e.text.trim().split(/\s+/u).length / ((e.end - e.start) / 1000)
          : null,
    })),
    relations,
    limits:
      "Caller-supplied intervals. Timing proximity and exposure do not establish understanding, comfort or an appropriate reading rate.",
  };
}
export function survey(spec) {
  object(spec, "survey");
  const ids = named(spec.items, "survey items");
  array(spec.responses, "survey responses");
  for (const item of spec.items) {
    if (item.axis !== undefined && typeof item.axis !== "string")
      throw new Error("survey axis must be a string");
    if (item.reverse !== undefined && typeof item.reverse !== "boolean")
      throw new Error("survey reverse must be boolean");
  }
  for (const response of spec.responses) object(response, "survey response");
  const lo = finite(spec.minimum, "minimum"),
    hi = finite(spec.maximum, "maximum");
  if (hi <= lo) throw new Error("survey maximum must exceed minimum");
  for (const r of spec.responses)
    for (const [id, v] of Object.entries(r)) {
      if (!ids.has(id)) throw new Error(`unknown survey item ${id}`);
      finite(v, "response");
      if (v < lo || v > hi) throw new Error("response outside declared scale");
    }
  const items = spec.items.map((i) => {
    const v = spec.responses
      .filter((r) => Object.hasOwn(r, i.id))
      .map((r) => (i.reverse ? hi + lo - r[i.id] : r[i.id]));
    return { id: i.id, axis: i.axis || null, n: v.length, mean: mean(v) };
  });
  const axes = [...new Set(items.map((i) => i.axis).filter(Boolean))].map(
    (axis) => {
      const group = items.filter((i) => i.axis === axis);
      const complete = spec.responses.filter((r) =>
        group.every((i) => Object.hasOwn(r, i.id)),
      );
      const values = complete.map((r) =>
        mean(
          group.map((i) => {
            const item = spec.items.find((x) => x.id === i.id);
            return item.reverse ? hi + lo - r[i.id] : r[i.id];
          }),
        ),
      );
      return {
        axis,
        completeResponses: complete.length,
        excludedIncomplete: spec.responses.length - complete.length,
        mean: mean(values),
      };
    },
  );
  return {
    items,
    axes,
    limits:
      "Descriptive aggregation of supplied responses; no invented participants, questionnaire validation, population inference or automatic weighting across axes.",
  };
}

export function content(spec) {
  object(spec, "content");
  const ids = named(spec.items, "content items");
  array(spec.order, "content order");
  if (
    new Set(spec.order).size !== spec.order.length ||
    spec.order.some((id) => !ids.has(id))
  )
    throw new Error("content order has duplicate or unknown ids");
  return {
    items: spec.items.map((i) => {
      if (i.prerequisites) array(i.prerequisites, "prerequisites");
      return {
        id: i.id,
        role: i.role || null,
        position: spec.order.indexOf(i.id),
        present: spec.order.includes(i.id),
        prerequisites: (i.prerequisites || []).map((id) => {
          if (!ids.has(id)) throw new Error("unknown content prerequisite");
          return {
            id,
            introducedEarlier:
              spec.order.includes(id) &&
              spec.order.includes(i.id) &&
              spec.order.indexOf(id) < spec.order.indexOf(i.id),
          };
        }),
      };
    }),
    limits:
      "Declared content order and dependencies only. Does not establish prerequisite necessity, truth of claims, comprehension or learning.",
  };
}
export function compare(a, b) {
  const differences = [],
    unmatched = [];
  function walk(x, y, path) {
    if (
      typeof x === "number" &&
      typeof y === "number" &&
      Number.isFinite(x) &&
      Number.isFinite(y)
    ) {
      if (x !== y)
        differences.push({ path, before: x, after: y, delta: y - x });
      return;
    }
    if (Array.isArray(x) && Array.isArray(y)) {
      const keyed = (a) =>
        a.length > 0 &&
        a.every(
          (v) => v && typeof v === "object" && typeof v.id === "string",
        ) &&
        new Set(a.map((v) => v.id)).size === a.length;
      if (keyed(x) && keyed(y)) {
        const right = new Map(y.map((v) => [v.id, v]));
        for (const v of x) {
          if (right.has(v.id)) walk(v, right.get(v.id), `${path}[id=${v.id}]`);
          else unmatched.push(`${path}[id=${v.id}] removed`);
        }
        for (const v of y)
          if (!x.some((z) => z.id === v.id))
            unmatched.push(`${path}[id=${v.id}] added`);
      } else if (
        x.length === y.length &&
        x.every((v) => typeof v === "number") &&
        y.every((v) => typeof v === "number")
      )
        x.forEach((v, i) => walk(v, y[i], `${path}[${i}]`));
      else
        unmatched.push(
          `${path}: array identities unavailable; inspect full reports`,
        );
      return;
    }
    if (x && y && typeof x === "object" && typeof y === "object") {
      for (const key of new Set([...Object.keys(x), ...Object.keys(y)])) {
        if (Object.hasOwn(x, key) && Object.hasOwn(y, key))
          walk(x[key], y[key], path ? `${path}.${key}` : key);
        else unmatched.push(`${path}.${key}: present in one report only`);
      }
    } else if (x !== y) unmatched.push(`${path}: nonnumeric value changed`);
  }
  walk(a.observations || a, b.observations || b, "");
  return {
    numericDeltas: differences,
    unmatched,
    scopeMatched:
      a.scope && b.scope
        ? JSON.stringify(a.scope) === JSON.stringify(b.scope)
        : null,
    limits:
      "Numeric deltas aligned by object keys and unique caller ids, or positional numeric arrays. Automatically assigned DOM ids may change after edits. Nonaligned content stays explicit. No preferred delta direction.",
  };
}

export function viewing(spec) {
  object(spec, "viewing");
  array(spec.elements, "viewing elements");
  const distanceMm = finite(spec.distanceMm, "distanceMm");
  if (distanceMm <= 0) throw new Error("viewing distance must be positive");
  return {
    distanceMm,
    elements: spec.elements.map((e) => {
      object(e, "viewing element");
      const sizeMm = finite(e.sizeMm, "sizeMm");
      if (sizeMm < 0) throw new Error("sizeMm must be nonnegative");
      return {
        id: e.id,
        sizeMm,
        angleArcMinutes:
          ((2 * Math.atan(sizeMm / (2 * distanceMm)) * 180) / Math.PI) * 60,
      };
    }),
    limits:
      "Geometric angular size from supplied physical size and viewing distance. Does not measure readability, lighting, projection, visual acuity or a recommended threshold.",
  };
}

// Oklab equations, public-domain implementation by Bjorn Ottosson:
// https://bottosson.github.io/posts/oklab/
export function oklab(rgbColor) {
  const [r, g, b] = rgbColor.map(linear);
  const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b);
  const m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b);
  const s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
  return [
    0.2104542553 * l + 0.793617785 * m - 0.0040720468 * s,
    1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s,
    0.0259040371 * l + 0.7827717662 * m - 0.808675766 * s,
  ];
}
export function palette(spec) {
  object(spec, "palette");
  const ids = named(spec.colors, "palette colors");
  const colors = spec.colors.map((c) => {
    if (typeof c.hex !== "string" || !/^#[0-9a-f]{6}$/i.test(c.hex))
      throw new Error("palette colors need opaque six-digit sRGB hex");
    const rgbColor = [1, 3, 5].map(
        (i) => parseInt(c.hex.slice(i, i + 2), 16) / 255,
      ),
      lab = oklab(rgbColor);
    return {
      id: c.id,
      hex: c.hex,
      rgb: rgbColor,
      oklab: lab,
      oklch: [
        lab[0],
        Math.hypot(lab[1], lab[2]),
        ((Math.atan2(lab[2], lab[1]) * 180) / Math.PI + 360) % 360,
      ],
    };
  });
  const pairs = spec.pairs
    ? array(spec.pairs, "palette pairs")
    : colors.flatMap((a, i) => colors.slice(i + 1).map((b) => [a.id, b.id]));
  const comparisons = pairs.map((pair) => {
    if (
      !Array.isArray(pair) ||
      pair.length !== 2 ||
      pair.some((id) => !ids.has(id))
    )
      throw new Error("palette pair needs two known ids");
    const [a, b] = pair.map((id) => colors.find((c) => c.id === id));
    return {
      id: pair.join(" / "),
      pair,
      deltaEOK: Math.hypot(...a.oklab.map((v, i) => v - b.oklab[i])),
      contrastRatio: contrast(a.rgb, b.rgb),
    };
  });
  const ramp = spec.order
    ? array(spec.order, "palette order").map((id) => {
        if (!ids.has(id)) throw new Error("palette order has unknown id");
        return colors.find((c) => c.id === id);
      })
    : [];
  return {
    colors: colors.map(({ rgb, ...c }) => c),
    comparisons,
    orderedLightness: ramp.map((c, i) => ({
      id: c.id,
      L: c.oklab[0],
      deltaFromPrevious: i ? c.oklab[0] - ramp[i - 1].oklab[0] : null,
    })),
    limits:
      "Declared opaque sRGB colors; Oklab distance in 0–1 coordinate units is not a universal distinguishability threshold, color-vision simulation, categorical meaning or safe-palette verdict. Declare relevant pair topology rather than assuming only adjacent colors can touch.",
  };
}
