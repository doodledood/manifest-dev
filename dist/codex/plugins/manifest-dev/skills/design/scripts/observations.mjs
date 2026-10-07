import {
  object,
  array,
  finite,
  associations,
  coVisibility,
  textSummary,
  colorSamples,
} from "./measurements.mjs";

export const instruments = {
  geometry: "Supplied boxes, relationships and alignments",
  visibility: "Supplied viewport, boxes and clipping observations",
  typography: "Supplied rendered text lines, fonts and glyph widths",
  copy: "Supplied text, headings, actions and repeated strings",
  color: "Supplied opaque text paint samples and exclusions",
  access: "Supplied semantics, labels, language and form attributes",
  targets: "Supplied control boxes and optional pointer samples",
  media: "Supplied assets, alternatives and dimensions",
  motion: "Supplied animation timing observations",
  image: "Supplied image pixels and local variation descriptors",
};

function box(value, name, positive = false) {
  object(value, name);
  for (const k of ["x", "y", "width", "height"])
    finite(value[k], `${name}.${k}`);
  if (
    value.width < 0 ||
    value.height < 0 ||
    (positive && (!value.width || !value.height))
  )
    throw new Error(
      `${name} needs ${positive ? "positive" : "nonnegative"} dimensions`,
    );
}
function records(s, key) {
  if (!Object.hasOwn(s, key))
    throw new Error(`Supply ${key} observations for this instrument`);
  array(s[key], key);
  for (const record of s[key]) object(record, `${key} record`);
  return s[key];
}
function validateGeometry(s, plan, visibility) {
  object(s.entities, "entities");
  for (const [id, e] of Object.entries(s.entities)) {
    object(e, `entity ${id}`);
    box(e.box, `entity ${id}.box`);
    if (e.visibleBox) {
      box(e.visibleBox, `entity ${id}.visibleBox`);
      const b = e.box,
        c = e.visibleBox;
      if (
        c.width > 0 &&
        c.height > 0 &&
        (c.x < b.x - 0.01 ||
          c.y < b.y - 0.01 ||
          c.x + c.width > b.x + b.width + 0.01 ||
          c.y + c.height > b.y + b.height + 0.01)
      )
        throw new Error(
          `entity ${id}.visibleBox must be within its original box`,
        );
    }
    if (e.fontSize !== undefined && finite(e.fontSize, "fontSize") <= 0)
      throw new Error("fontSize must be positive when supplied");
    if (visibility && typeof e.visible !== "boolean")
      throw new Error(`Supply observed visibility for entity ${id}`);
  }
  for (const key of ["links", "groups", "alignments"]) {
    if (plan[key] !== undefined) array(plan[key], key);
    for (const item of plan[key] || []) {
      object(item, key);
      const ids =
        key === "links"
          ? [item.from, item.to, ...(item.competitors || [])]
          : item.members;
      if (key === "links" && item.competitors !== undefined)
        array(item.competitors, "competitors");
      array(ids, `${key} members`);
      if (!ids.length) throw new Error(`${key} needs nonempty members`);
      for (const id of ids)
        if (!Object.hasOwn(s.entities, id))
          throw new Error(`Unknown named entity: ${id}`);
    }
  }
  if (visibility) box(s.viewport, "viewport", true);
}
function alignments(groups, entities) {
  return groups.map((g) => {
    const axis = g.axis || "left";
    if (!["left", "right", "top", "bottom", "width", "height"].includes(axis))
      throw new Error("Unknown alignment axis");
    const values = g.members.map((id) => {
      const b = entities[id].box;
      return {
        id,
        value:
          axis === "left"
            ? b.x
            : axis === "right"
              ? b.x + b.width
              : axis === "top"
                ? b.y
                : axis === "bottom"
                  ? b.y + b.height
                  : b[axis],
      };
    });
    return {
      id: g.id,
      axis,
      values,
      rangePx:
        values.reduce((m, v) => Math.max(m, v.value), -Infinity) -
        values.reduce((m, v) => Math.min(m, v.value), Infinity),
    };
  });
}

// Acquisition is outside this module. The caller supplies observations from any host.
export function analyzeObservations(s, tools, plan = {}) {
  object(s, "observations");
  object(plan, "plan");
  const result = {};
  for (const tool of tools) {
    if (!Object.hasOwn(instruments, tool) || tool === "image")
      throw new Error(`Unknown observation instrument: ${tool}`);
    if (["geometry", "visibility"].includes(tool)) {
      validateGeometry(s, plan, tool === "visibility");
      result[tool] =
        tool === "geometry"
          ? {
              entities: s.entities,
              associations: associations(plan.links || [], s.entities),
              alignments: alignments(plan.alignments || [], s.entities),
              limits:
                "Supplied geometry, not optical boundaries or understood relationships. Em distances are unmeasured without a supplied font size.",
            }
          : {
              groups: coVisibility(plan.groups || [], s.entities, s.viewport),
              documentSize: s.documentSize,
              limits:
                "Supplied viewport/clip evidence only. Missing paint or internal text clipping is not inferred.",
            };
    } else if (tool === "copy" || tool === "typography") {
      const nodes = records(s, "nodes");
      for (const n of nodes) {
        if (typeof n.text !== "string")
          throw new Error("nodes need text strings");
        if (
          tool === "typography" &&
          (!Number.isInteger(n.lines) ||
            n.lines < 0 ||
            typeof n.fontSize !== "number" ||
            !Number.isFinite(n.fontSize) ||
            n.fontSize <= 0)
        )
          throw new Error(
            "typography needs supplied rendered line counts and positive font sizes; HTML source cannot establish them",
          );
      }
      result[tool] = {
        ...textSummary(nodes),
        ...(tool === "copy"
          ? { headings: s.headings, actions: s.controls }
          : { glyphWidths: s.glyphWidths }),
        limits:
          "Supplied text/property inventory, not reading load, legibility or comprehension. Missing rendered properties remain unmeasured.",
      };
    } else if (tool === "color") {
      const nodes = records(s, "nodes");
      for (const n of nodes) {
        if (
          typeof n.color !== "string" ||
          !Array.isArray(n.backgrounds) ||
          !Array.isArray(n.paintEffects)
        )
          throw new Error(
            "color needs supplied foreground, ancestor backgrounds and paintEffects coverage; HTML source cannot establish paint",
          );
      }
      result.color = colorSamples(nodes);
    } else if (tool === "access") {
      result.access = {
        controls: records(s, "controls"),
        headings: s.headings,
        media: s.media,
        languages: s.languages,
        limits:
          "Supplied/source semantics and name candidates, not an accessibility-tree or assistive-technology certification.",
      };
    } else if (tool === "targets") {
      const controls = records(s, "controls");
      for (const c of controls) {
        box(c.box, "control.box");
        if (c.points !== undefined) {
          array(c.points, "pointer samples");
          for (const point of c.points) {
            object(point, "pointer sample");
            finite(point.x, "pointer sample x");
            finite(point.y, "pointer sample y");
            if (typeof point.receivesPointer !== "boolean")
              throw new Error(
                "pointer samples need observed receivesPointer booleans",
              );
          }
        }
      }
      result.targets = {
        controls,
        unmeasuredPointerSamples: controls
          .filter((c) => !Array.isArray(c.points) || !c.points.length)
          .map((c) => c.id),
        limits:
          "Supplied boxes; pointer reception is known only for supplied hit samples. Geometry alone does not establish behavior or ergonomics.",
      };
    } else if (tool === "media") {
      result.media = {
        assets: records(s, "media"),
        limits:
          "Supplied/source asset inventory. Declared dimensions do not establish rendered crop, relevance or equivalent meaning.",
      };
    } else if (tool === "motion") {
      result.motion = {
        animations: records(s, "animations"),
        limits:
          "Supplied timing observations; no discovery of future triggers, frame-time or comfort.",
      };
    }
  }
  return result;
}
