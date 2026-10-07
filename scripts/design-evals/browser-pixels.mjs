export async function decodePixels(page, buffer, mime, maxEdge = 512) {
  return page.evaluate(
    async ({ data, mime, maxEdge }) => {
      const img = new Image();
      img.src = `data:${mime};base64,${data}`;
      await img.decode();
      const scale = Math.min(
        1,
        maxEdge / Math.max(img.naturalWidth, img.naturalHeight),
      );
      const width = Math.max(1, Math.round(img.naturalWidth * scale)),
        height = Math.max(1, Math.round(img.naturalHeight * scale));
      const canvas = document.createElement("canvas");
      canvas.width = width;
      canvas.height = height;
      const c = canvas.getContext("2d");
      c.fillStyle = "white";
      c.fillRect(0, 0, width, height);
      c.drawImage(img, 0, 0, width, height);
      return {
        data: Array.from(c.getImageData(0, 0, width, height).data),
        width,
        height,
        originalSize: { width: img.naturalWidth, height: img.naturalHeight },
      };
    },
    { data: buffer.toString("base64"), mime, maxEdge },
  );
}
export async function inspectionViews(page, buffer) {
  return page.evaluate(async (data) => {
    const img = new Image();
    img.src = `data:image/png;base64,${data}`;
    await img.decode();
    const views = {};
    for (const [name, filter, scale] of [
      ["grayscale", "grayscale(1)", 1],
      ["blur", "blur(8px)", 1],
      ["thumbnail", "none", Math.min(1, 240 / img.naturalWidth)],
    ]) {
      const c = document.createElement("canvas");
      c.width = Math.max(1, Math.round(img.naturalWidth * scale));
      c.height = Math.max(1, Math.round(img.naturalHeight * scale));
      const ctx = c.getContext("2d");
      ctx.fillStyle = "white";
      ctx.fillRect(0, 0, c.width, c.height);
      ctx.filter = filter;
      ctx.drawImage(img, 0, 0, c.width, c.height);
      views[name] = c.toDataURL("image/png").split(",")[1];
    }
    return views;
  }, buffer.toString("base64"));
}
