"""Optional, frozen first-impression estimates from supplied image/features.

Pillow decodes/resamples images; the remaining arithmetic uses the standard
library. No acquisition, rendering, learning or network operations occur here.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any


def features(path: str) -> tuple[dict[str, float], dict[str, Any]]:
    try:
        from PIL import Image, ImageOps
    except ImportError as error:
        raise ValueError(
            "Image input requires Pillow; select DESIGN_TOOLS_PYTHON"
        ) from error
    with Image.open(path) as raw:
        oriented = ImageOps.exif_transpose(raw).convert("RGBA")
        canvas = Image.new("RGBA", oriented.size, "white")
        canvas.alpha_composite(oriented)
        original = canvas.convert("RGB")
    result = {}
    for scale in [128, 256, 512]:
        image = original.copy()
        image.thumbnail((scale, scale), Image.Resampling.LANCZOS)
        width, height = image.size
        rgb = [(r / 255, g / 255, b / 255) for r, g, b in image.getdata()]
        gray = [0.2126 * r + 0.7152 * g + 0.0722 * b for r, g, b in rgb]
        gradient = [
            math.hypot(gray[i + 1] - gray[i], gray[i + width] - gray[i])
            for y in range(height - 1)
            for x in range(width - 1)
            for i in [y * width + x]
        ]
        result[f"gradient_{scale}"] = (
            math.fsum(gradient) / len(gradient) if gradient else 0
        )
        for threshold in [0.02, 0.04, 0.08, 0.12, 0.20]:
            result[f"edge_{scale}_{threshold}"] = (
                sum(v > threshold for v in gradient) / len(gradient) if gradient else 0
            )
        histogram = [0] * 32
        for value in gray:
            histogram[min(31, math.floor(value * 32))] += 1
        result[f"entropy_{scale}"] = -math.fsum(
            (count / len(gray)) * math.log2(count / len(gray))
            for count in histogram
            if count
        )
        rg = [r - g for r, g, b in rgb]
        yb = [(r + g) / 2 - b for r, g, b in rgb]
        rg_mean, yb_mean = math.fsum(rg) / len(rg), math.fsum(yb) / len(yb)
        variance = math.fsum((v - rg_mean) ** 2 for v in rg) / len(rg)
        variance += math.fsum((v - yb_mean) ** 2 for v in yb) / len(yb)
        result[f"colorfulness_{scale}"] = math.sqrt(variance) + 0.3 * math.hypot(
            rg_mean, yb_mean
        )
    return result, {
        "originalSize": list(original.size),
        "decoder": f"Pillow {Image.__version__}",
        "processing": "EXIF transpose; first frame; alpha over white; no ICC conversion; independent LANCZOS maximum-edge128/256/512 views",
    }


def estimate(values: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    axes = {}
    for axis, arm in profile["models"].items():
        model = arm["model"]
        normalized = []
        for name, mean, scale in zip(
            arm["features"], model["means"], model["scales"], strict=True
        ):
            value = values.get(name)
            if (
                isinstance(value, bool)
                or not isinstance(value, (float, int))
                or not math.isfinite(value)
            ):
                raise ValueError(f"Missing/nonfinite feature: {name}")
            normalized.append((value - mean) / scale)
        prediction = model["intercept"] + math.fsum(
            (value - center) * coefficient
            for value, center, coefficient in zip(
                normalized, model["center"], model["coefficients"], strict=True
            )
        )
        axes[axis] = {
            "estimatedMeanRating": prediction,
            "trainingScale": "1-7; output is unbounded and not a personal rating or probability",
            "maxAbsoluteStandardizedFeature": max(abs(v) for v in normalized),
            "distanceLimit": "Feature distance describes departure from training moments; it is not calibrated prediction uncertainty.",
        }
    return {
        "profile": profile["id"],
        "frozenModelSHA256": profile["frozenModelSHA256"],
        "axes": axes,
        "evidence": profile["evidence"],
        "limits": profile["limits"],
        "features": values,
    }


def main() -> None:
    profile = json.loads(
        Path(__file__).with_name("appearance-profile.json").read_text()
    )
    path = sys.argv[1]
    if path == "-" or Path(path).suffix.lower() == ".json":
        supplied = json.loads(
            sys.stdin.read() if path == "-" else Path(path).read_text()
        )
        if not isinstance(supplied, dict) or not isinstance(
            supplied.get("features"), dict
        ):
            raise ValueError(
                "Supplied JSON needs a features object matching the profile recipe"
            )
        values, provenance = supplied["features"], {
            "basis": "caller-supplied features; decoding recipe/provenance caller-owned"
        }
    else:
        values, provenance = features(path)
    print(
        json.dumps(
            {
                "scope": provenance,
                "observations": {"appearance": estimate(values, profile)},
            },
            allow_nan=False,
        )
    )


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        print(f"appearance: {error}", file=sys.stderr)
        sys.exit(1)
