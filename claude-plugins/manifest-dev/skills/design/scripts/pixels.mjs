import { mean } from "./measurements.mjs";

// Low-level image descriptors, deliberately not labeled saliency or UX quality.
export function describePixels(
  data,
  width,
  height,
  { threshold = 0.08, tileSize = 16 } = {},
) {
  if (
    !Number.isInteger(width) ||
    !Number.isInteger(height) ||
    width < 1 ||
    height < 1 ||
    !data ||
    data.length !== width * height * 4
  )
    throw new Error("pixels need positive dimensions and matching RGBA data");
  if (!Number.isFinite(threshold) || threshold < 0 || threshold > 1)
    throw new Error("edge threshold must be in [0,1]");
  if (!Number.isInteger(tileSize) || tileSize < 1)
    throw new Error("tile size must be a positive integer");
  const gray = new Float64Array(width * height),
    hist = new Array(32).fill(0),
    rg = [],
    yb = [];
  for (let i = 0; i < gray.length; i++) {
    const bytes = Array.from(data.slice(i * 4, i * 4 + 4));
    if (bytes.some((v) => !Number.isInteger(v) || v < 0 || v > 255))
      throw new Error("RGBA channels must be integer bytes in [0,255]");
    const alpha = bytes[3] / 255,
      r = (bytes[0] / 255) * alpha + 1 - alpha,
      g = (bytes[1] / 255) * alpha + 1 - alpha,
      b = (bytes[2] / 255) * alpha + 1 - alpha;
    gray[i] = 0.2126 * r + 0.7152 * g + 0.0722 * b;
    hist[Math.min(31, Math.floor(gray[i] * 32))]++;
    rg.push(r - g);
    yb.push((r + g) / 2 - b);
  }
  const sd = (a) => {
    const m = mean(a);
    return Math.sqrt(mean(a.map((x) => (x - m) ** 2)));
  };
  const gradient = new Float64Array(gray.length);
  let sum = 0,
    edges = 0;
  // Exclude canvas boundary: there is no neighboring pixel to compare there.
  for (let y = 0; y < height - 1; y++)
    for (let x = 0; x < width - 1; x++) {
      const i = y * width + x,
        v = Math.hypot(gray[i + 1] - gray[i], gray[i + width] - gray[i]);
      gradient[i] = v;
      sum += v;
      if (v > threshold) edges++;
    }
  const tiles = [];
  for (let y = 0; y < height; y += tileSize)
    for (let x = 0; x < width; x += tileSize) {
      let count = 0,
        s = 0,
        n = 0;
      for (let yy = y; yy < Math.min(y + tileSize, height); yy++)
        for (let xx = x; xx < Math.min(x + tileSize, width); xx++) {
          const i = yy * width + xx;
          s += gradient[i];
          if (gradient[i] > threshold) n++;
          count++;
        }
      tiles.push({
        x,
        y,
        width: Math.min(tileSize, width - x),
        height: Math.min(tileSize, height - y),
        meanGradient: s / count,
        edgeFraction: n / count,
      });
    }
  const entropy = -hist.reduce((s, c) => {
    const p = c / gray.length;
    return p ? s + p * Math.log2(p) : s;
  }, 0);
  const interior = Math.max(0, (width - 1) * (height - 1));
  return {
    analysisSize: { width, height },
    parameters: { threshold, tileSize, gradient: "forward adjacent pixels" },
    edgeFraction: interior ? edges / interior : 0,
    meanGradient: interior ? sum / interior : 0,
    luminanceHistogramEntropyBits: entropy,
    colorfulnessDescriptor:
      Math.hypot(sd(rg), sd(yb)) + 0.3 * Math.hypot(mean(rg), mean(yb)),
    tiles,
    limits:
      "Downsampled encoded-RGB image descriptors; transparent pixels are composited over white. Tile map colors are normalized within each image and cannot compare absolute strength between maps. Edge density is not feature congestion; gradient energy is not gaze, complexity preference, cognitive load or beauty. Compare matched content, crop and analysis size.",
  };
}
export function heatmapSvg(result) {
  const max = result.tiles.reduce(
    (max, t) => Math.max(max, t.meanGradient),
    0.0001,
  );
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${result.analysisSize.width}" height="${result.analysisSize.height}">${result.tiles.map((t) => `<rect x="${t.x}" y="${t.y}" width="${t.width}" height="${t.height}" fill="rgb(255,${Math.round(255 * (1 - t.meanGradient / max))},0)"/>`).join("")}</svg>`;
}
