#!/usr/bin/env python3
"""Offline real-homepage calibration. Acquisition remains outside the instruments.

Commands separate extraction, development fitting, and one final label evaluation.
Data/images stay in a caller-owned directory; this file ships no website assets.
Requires Pillow, NumPy, SciPy, scikit-learn; AIM comparison also needs OpenCV,
pydantic and an explicit local AIM checkout. No network access occurs here.
"""

import argparse
import base64
import csv
import hashlib
import importlib
import importlib.metadata
import io
import json
import platform
import subprocess
import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps
from scipy.fft import dctn
from scipy.stats import spearmanr
from sklearn.preprocessing import PolynomialFeatures

AXES = ["complexity", "aesthetics", "craftsmanship", "novelty", "technical-condition"]
SOURCES = {
    "AVI_14": "train",
    "CHI_13": "train",
    "CHI_15": "train",
    "IJHCS_12": "development",
    "CHI_20": "test",
    "ICWE_19": "test",
}
PRIORITY = {"train": 0, "development": 1, "test": 2}
AIM_MODULES = {
    "aim_contour_density": "m4.m4_contour_density",
    "aim_figure_ground": "m5.m5_figure_ground_contrast",
    "aim_luminance_sd": "m13.m13_luminance_std",
    "aim_colorfulness": "m15.m15_colorfulness_hassler_susstrunk",
    "aim_distinct_rgb": "m3.m3_distinct_rgb_values",
}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    path = Path(path)
    if path.exists():
        raise FileExistsError(f"Preserve the earlier evidence; output exists: {path}")
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def load(path):
    return json.loads(Path(path).read_text())


def correlation(x, y):
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):
        raise ValueError("Correlation input must be finite")
    if len(x) < 3 or np.ptp(x) == 0 or np.ptp(y) == 0:
        return None
    result = float(spearmanr(x, y).statistic)
    return result if np.isfinite(result) else None


def image_features(args):
    path, aim = args
    path = Path(path)
    with Image.open(path) as raw:
        image = ImageOps.exif_transpose(raw).convert("RGBA")
        canvas = Image.new("RGBA", image.size, "white")
        canvas.alpha_composite(image)
        image = canvas.convert("RGB")
    full = hashlib.sha256(image.tobytes() + str(image.size).encode()).hexdigest()
    tiny = np.asarray(image.resize((9, 8)).convert("L"))
    dhash = int(
        "".join("1" if x else "0" for x in (tiny[:, 1:] > tiny[:, :-1]).flat), 2
    )
    similarity = np.asarray(image.resize((64, 40)), dtype=np.uint8)
    frequency = dctn(
        np.asarray(image.resize((32, 32)).convert("L"), dtype=float),
        type=2,
        norm="ortho",
    )[:8, :8].ravel()[1:]
    phash = int("".join("1" if x else "0" for x in frequency > np.median(frequency)), 2)
    features = {}
    for scale in [128, 256, 512]:
        view = image.copy()
        view.thumbnail((scale, scale), Image.Resampling.LANCZOS)
        rgb = np.asarray(view, dtype=float) / 255
        gray = rgb @ np.array([0.2126, 0.7152, 0.0722])
        gradient = np.hypot(
            gray[:-1, 1:] - gray[:-1, :-1], gray[1:, :-1] - gray[:-1, :-1]
        )
        features[f"gradient_{scale}"] = (
            float(np.mean(gradient)) if gradient.size else 0.0
        )
        for threshold in [0.02, 0.04, 0.08, 0.12, 0.20]:
            features[f"edge_{scale}_{threshold}"] = (
                float(np.mean(gradient > threshold)) if gradient.size else 0.0
            )
        hist = np.bincount(
            np.minimum(31, np.floor(gray * 32).astype(int)).ravel(), minlength=32
        )
        probabilities = hist[hist > 0] / gray.size
        features[f"entropy_{scale}"] = float(
            -np.sum(probabilities * np.log2(probabilities))
        )
        rg = rgb[:, :, 0] - rgb[:, :, 1]
        yb = (rgb[:, :, 0] + rgb[:, :, 1]) / 2 - rgb[:, :, 2]
        features[f"colorfulness_{scale}"] = float(
            np.hypot(np.std(rg), np.std(yb)) + 0.3 * np.hypot(np.mean(rg), np.mean(yb))
        )
    if aim:
        sys.path.insert(0, str(Path(aim) / "backend"))
        buf = io.BytesIO()
        view.save(buf, format="PNG")
        encoded = base64.b64encode(buf.getvalue()).decode()
        for name, module in AIM_MODULES.items():
            metric = importlib.import_module(f"aim.metrics.{module}").Metric
            features[name] = float(metric.execute_metric(encoded)[0])
        jpeg = io.BytesIO()
        view.save(jpeg, format="JPEG", quality=70)
        features["jpeg70_bytes_per_pixel"] = len(jpeg.getvalue()) / (
            view.width * view.height
        )
    name = path.name
    source = next((x for x in SOURCES if name.startswith(x + "_")), None)
    return {
        "id": name,
        "source": source,
        "split": SOURCES.get(source),
        "originalSize": list(image.size),
        "sha256": digest(path),
        "pixelHash": full,
        "differenceHash": f"{dhash:016x}",
        "perceptualHash": f"{phash:016x}",
        "similarityThumbnail": base64.b64encode(similarity.tobytes()).decode(),
        "features": features,
    }


def extract(args):
    initial_code_hash = digest(__file__)
    paths = sorted(Path(args.images).rglob("*.png"))
    if len({p.name for p in paths}) != len(paths):
        raise ValueError("Duplicate image basename IDs; label joins must be one to one")
    if any(not any(p.name.startswith(s + "_") for s in SOURCES) for p in paths):
        raise ValueError(
            "Unknown image provenance; source assignment must precede extraction"
        )
    if len(paths) != 1506:
        raise ValueError(f"Expected1506 source images, found{len(paths)}")
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        rows = []
        for i, row in enumerate(
            pool.map(image_features, [(str(p), args.aim) for p in paths])
        ):
            rows.append(row)
            if (i + 1) % 100 == 0:
                print(f"Extracted{i + 1}/{len(paths)}", flush=True)
    parent = list(range(len(rows)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    near = []
    for i, a in enumerate(rows):
        for j in range(i):
            b = rows[j]
            distance = (
                int(a["differenceHash"], 16) ^ int(b["differenceHash"], 16)
            ).bit_count()
            exact = a["pixelHash"] == b["pixelHash"]
            verified = exact
            if distance <= 5 and not exact:
                p_distance = (
                    int(a["perceptualHash"], 16) ^ int(b["perceptualHash"], 16)
                ).bit_count()
                a_thumb = np.frombuffer(
                    base64.b64decode(a["similarityThumbnail"]), dtype=np.uint8
                ).astype(float)
                b_thumb = np.frombuffer(
                    base64.b64decode(b["similarityThumbnail"]), dtype=np.uint8
                ).astype(float)
                pixel_distance = float(np.mean(np.abs(a_thumb - b_thumb)) / 255)
                ratios = [r["originalSize"][0] / r["originalSize"][1] for r in [a, b]]
                verified = (
                    p_distance <= 8
                    and pixel_distance <= 0.06
                    and abs(np.log(ratios[0] / ratios[1])) <= 0.1
                    and min(
                        np.mean(np.std(a_thumb.reshape(64 * 40, 3), axis=0)),
                        np.mean(np.std(b_thumb.reshape(64 * 40, 3), axis=0)),
                    )
                    >= 2.55
                )
                if a["split"] != b["split"]:
                    near.append(
                        {
                            "a": a["id"],
                            "b": b["id"],
                            "differenceHashDistance": distance,
                            "perceptualHashDistance": p_distance,
                            "normalizedPixelDistance": pixel_distance,
                            "grouped": verified,
                        }
                    )
            if verified:
                parent[find(i)] = find(j)
                if exact and a["split"] != b["split"]:
                    near.append(
                        {"a": a["id"], "b": b["id"], "exact": True, "grouped": True}
                    )
    groups = {}
    for i, row in enumerate(rows):
        groups.setdefault(find(i), []).append(row)
    excluded = []
    for members in groups.values():
        group = min(row["id"] for row in members)
        latest = max(PRIORITY[row["split"]] for row in members)
        seen = set()
        for row in members:
            row["group"] = group
            reason = None
            if PRIORITY[row["split"]] < latest:
                reason = "Near duplicate/template in a later split"
            elif row["pixelHash"] in seen:
                reason = "Exact duplicate within split"
            seen.add(row["pixelHash"])
            row["excluded"] = reason
            if reason:
                excluded.append({"id": row["id"], "reason": reason})
    aim_provenance = None
    if args.aim:
        aim_root = Path(args.aim)
        modules = [
            aim_root / "backend/aim/metrics" / (module.replace(".", "/") + ".py")
            for module in AIM_MODULES.values()
        ]
        modules += [
            aim_root / "LICENSE.txt",
            aim_root / "backend/aim/common/constants.py",
            aim_root / "backend/aim/metrics/interfaces.py",
        ]
        aim_provenance = {
            "commit": subprocess.check_output(
                ["git", "-C", str(aim_root), "rev-parse", "HEAD"], text=True
            ).strip(),
            "fileHashes": {str(p.relative_to(aim_root)): digest(p) for p in modules},
        }
    if digest(__file__) != initial_code_hash:
        raise ValueError(
            "Extractor changed during the run; preserve output and rerun with stable code"
        )
    save(
        Path(args.out) / "features.json",
        {
            "rows": rows,
            "decoder": {
                "python": platform.python_version(),
                "pillow": Image.__version__,
                "numpy": np.__version__,
                "orientation": "EXIF",
                "alpha": "white",
                "resize": "LANCZOS max edge, no upscale",
                "aimCheckout": args.aim,
                "aimProvenance": aim_provenance,
                "opencvImplementation": (
                    __import__("cv2").__version__ if args.aim else None
                ),
                "aimVariant": "Desktop defaults, EXIF/white composite,512px maximum edge. Scale-adapted candidate, not replication at original study resolution.",
                "dependencies": {
                    name: importlib.metadata.version(name)
                    for name in [
                        "numpy",
                        "pillow",
                        "scipy",
                        "scikit-learn",
                        "opencv-python-headless",
                        "pydantic",
                    ]
                    if args.aim or name not in ["opencv-python-headless", "pydantic"]
                },
                "scriptSHA256": digest(__file__),
                "protocolSHA256": digest(Path(args.out) / "calibration-plan.json"),
            },
            "crossSplitNearMatches": near,
            "excluded": excluded,
            "counts": dict(Counter(r["split"] for r in rows if not r["excluded"])),
        },
    )
    for split in PRIORITY:
        ids = {r["id"] for r in rows if r["split"] == split and not r["excluded"]}
        labels = {}
        for axis in AXES:
            ratings = {}
            with (Path(args.ratings) / f"{axis}.tsv").open() as source:
                for row in csv.reader(source, delimiter="\t"):
                    if row[0] not in ids:
                        continue
                    values = [float(v) for v in row[1:] if v != "NA"]
                    ratings[row[0]] = {
                        "mean": float(np.mean(values)),
                        "count": len(values),
                        "sd": float(np.std(values, ddof=1)),
                        "sem": float(np.std(values, ddof=1) / np.sqrt(len(values))),
                        "values": values,
                    }
            if set(ratings) != ids:
                raise ValueError(f"Missing labels for {split}/{axis}")
            labels[axis] = ratings
        save(Path(args.out) / f"labels-{split}.json", labels)
    print(
        "Source-separated features and labels frozen; final test labels remain separate."
    )


def matrix(rows, names):
    return np.array([[r["features"][name] for name in names] for r in rows])


def fit(x, y, alpha, quadratic):
    means = x.mean(axis=0)
    scales = x.std(axis=0)
    scales[scales == 0] = 1
    normalized = (x - means) / scales
    powers = None
    if quadratic:
        poly = PolynomialFeatures(2, include_bias=False)
        normalized = poly.fit_transform(normalized)
        powers = poly.powers_.tolist()
    center = normalized.mean(axis=0)
    normalized -= center
    intercept = float(np.mean(y))
    coefficients = np.linalg.solve(
        normalized.T @ normalized + alpha * np.eye(normalized.shape[1]),
        normalized.T @ (y - intercept),
    )
    return {
        "means": means.tolist(),
        "scales": scales.tolist(),
        "powers": powers,
        "center": center.tolist(),
        "intercept": intercept,
        "coefficients": coefficients.tolist(),
    }


def predict(x, model):
    values = (x - model["means"]) / model["scales"]
    if model["powers"] is not None:
        values = np.prod(
            values[:, None, :] ** np.array(model["powers"])[None, :, :], axis=2
        )
    return (values - model["center"]) @ np.array(model["coefficients"]) + model[
        "intercept"
    ]


def tune(args):
    data = load(Path(args.out) / "features.json")
    if data["decoder"]["scriptSHA256"] != digest(__file__) or data["decoder"][
        "protocolSHA256"
    ] != digest(Path(args.out) / "calibration-plan.json"):
        raise ValueError(
            "Extractor or protocol changed; use a fresh extraction before fitting"
        )
    train = [r for r in data["rows"] if r["split"] == "train" and not r["excluded"]]
    dev = [r for r in data["rows"] if r["split"] == "development" and not r["excluded"]]
    training = load(Path(args.out) / "labels-train.json")
    development = load(Path(args.out) / "labels-development.json")
    all_names = sorted(train[0]["features"])
    combined_names = [n for n in all_names if n != "aim_colorfulness"]
    native_names = [n for n in all_names if not n.startswith(("aim_", "jpeg70"))]
    base_names = ["gradient_512", "edge_512_0.08", "entropy_512", "colorfulness_512"]
    aim_names = [n for n in all_names if n.startswith("aim_") or n.startswith("jpeg70")]
    frozen = {
        "featureSHA256": digest(Path(args.out) / "features.json"),
        "scriptSHA256": digest(__file__),
        "protocolSHA256": digest(Path(args.out) / "calibration-plan.json"),
        "trainingLabelSHA256": digest(Path(args.out) / "labels-train.json"),
        "developmentLabelSHA256": digest(Path(args.out) / "labels-development.json"),
        "testLabelSHA256": digest(Path(args.out) / "labels-test.json"),
        "models": {},
        "baselines": {},
        "gradientBaselines": {},
        "nativeModels": {},
        "search": {},
        "evidence": "Fit only train labels; select only development labels. Final labels not read by tune.",
    }
    for axis in AXES:
        y = np.array([training[axis][r["id"]]["mean"] for r in train])
        target = np.array([development[axis][r["id"]]["mean"] for r in dev])
        candidates = []
        sets = [(name, [name]) for name in all_names] + [
            ("current_four", base_names),
            ("all_linear", combined_names),
            ("all_native_linear", native_names),
            ("current_quadratic", base_names),
        ]
        if aim_names:
            sets.append(("aim_linear", aim_names))
        for name, names in sets:
            quadratic = name == "current_quadratic"
            for alpha in (
                [1.0] if len(names) == 1 else [0.1, 1.0, 10.0, 100.0, 1000.0]
            ):
                model = fit(matrix(train, names), y, alpha, quadratic)
                estimates = predict(matrix(dev, names), model)
                rho = correlation(estimates, target)
                candidates.append(
                    {
                        "name": name,
                        "features": names,
                        "alpha": alpha,
                        "quadratic": quadratic,
                        "developmentSpearman": rho,
                        "developmentMAE": float(np.mean(np.abs(estimates - target))),
                        "model": model,
                    }
                )
        candidates.sort(
            key=lambda c: (
                -(
                    c["developmentSpearman"]
                    if c["developmentSpearman"] is not None
                    else -2
                ),
                c["developmentMAE"],
            )
        )
        winner = candidates[0]
        # Do not refit with development labels: keep the original fitted model.
        frozen["models"][axis] = winner
        frozen["baselines"][axis] = next(
            c for c in candidates if c["name"] == "current_four"
        )
        frozen["nativeModels"][axis] = next(
            c for c in candidates if c["name"] == "all_native_linear"
        )
        frozen["gradientBaselines"][axis] = next(
            c for c in candidates if c["name"] == "gradient_512"
        )
        frozen["search"][axis] = [
            {k: v for k, v in c.items() if k != "model"} for c in candidates
        ]
    save(Path(args.out) / "frozen-models.json", frozen)
    print(
        json.dumps(
            {
                axis: {
                    k: v
                    for k, v in frozen["models"][axis].items()
                    if k not in ["model", "features"]
                }
                for axis in AXES
            },
            indent=2,
        )
    )


def stats(rows, truth, predicted, baseline):
    groups = sorted({r["group"] for r in rows})
    by_group = {g: [i for i, r in enumerate(rows) if r["group"] == g] for g in groups}
    rng = np.random.default_rng(20261007)
    correlations, deltas, errors = [], [], []
    for _ in range(1000):
        indices = np.concatenate(
            [by_group[g] for g in rng.choice(groups, size=len(groups), replace=True)]
        )
        rho = correlation(predicted[indices], truth[indices])
        base = correlation(baseline[indices], truth[indices])
        if rho is not None:
            correlations.append(rho)
        if rho is not None and base is not None:
            deltas.append(rho - base)
        errors.append(
            float(
                np.mean(np.abs(predicted[indices] - truth[indices]))
                - np.mean(np.abs(baseline[indices] - truth[indices]))
            )
        )
    difference = truth[:, None] - truth[None, :]
    eligible = np.triu(np.abs(difference) >= 1, k=1)
    agreement = np.sign(predicted[:, None] - predicted[None, :]) * np.sign(difference)
    pair_count = int(np.sum(eligible))
    return {
        "nImages": len(rows),
        "nDuplicateGroups": len(groups),
        "spearman": correlation(predicted, truth),
        "spearman95CI": (
            np.quantile(correlations, [0.025, 0.975]).tolist() if correlations else None
        ),
        "baselineSpearman": correlation(baseline, truth),
        "deltaSpearman95CI": (
            np.quantile(deltas, [0.025, 0.975]).tolist() if deltas else None
        ),
        "mae": float(np.mean(np.abs(predicted - truth))),
        "baselineMAE": float(np.mean(np.abs(baseline - truth))),
        "deltaMAE95CI": np.quantile(errors, [0.025, 0.975]).tolist(),
        "separatedPairAccuracy": (
            float(
                np.mean(
                    np.where(agreement[eligible] == 0, 0.5, agreement[eligible] > 0)
                )
            )
            if pair_count
            else None
        ),
        "separatedPairCount": pair_count,
        "pairLimits": "Pairs share images; pair count is not an independent sample size. Eligibility uses>=1 point difference in human means.",
    }


def evaluate(args):
    out = Path(args.out)
    if (out / "test-evaluation-started.json").exists():
        raise FileExistsError(
            "Final labels were already evaluated; this split is now regression evidence."
        )
    data = load(out / "features.json")
    frozen = load(out / "frozen-models.json")
    if digest(out / "features.json") != frozen["featureSHA256"]:
        raise ValueError("Features changed after model freeze")
    for path, key in [
        (Path(__file__), "scriptSHA256"),
        (out / "calibration-plan.json", "protocolSHA256"),
        (out / "labels-train.json", "trainingLabelSHA256"),
        (out / "labels-development.json", "developmentLabelSHA256"),
        (out / "labels-test.json", "testLabelSHA256"),
    ]:
        if digest(path) != frozen[key]:
            raise ValueError(f"Frozen evaluation input changed: {path.name}")
    test = [r for r in data["rows"] if r["split"] == "test" and not r["excluded"]]
    with (out / "test-evaluation-started.json").open("x") as marker:
        json.dump(
            {
                "modelsSHA256": digest(out / "frozen-models.json"),
                "featureSHA256": digest(out / "features.json"),
                "note": "Final labels consumed once this marker is created. A failed or repeated evaluation is no longer a virgin holdout.",
            },
            marker,
            indent=2,
        )
    labels = load(out / "labels-test.json")
    training = load(out / "labels-train.json")
    report = {
        "modelsSHA256": digest(out / "frozen-models.json"),
        "featureSHA256": digest(out / "features.json"),
        "testLabelSHA256": digest(out / "labels-test.json"),
        "axes": {},
        "limits": "One new rating study across six image source collections. Bootstrap samples duplicate groups, not raters; confidence intervals omit systematic rater variation. Screenshot judgments are first impressions, not task performance. Artificial IDs cannot guarantee independent domains/templates.",
    }
    predictions = {}
    for axis in AXES:
        chosen = frozen["models"][axis]
        y = np.array([labels[axis][r["id"]]["mean"] for r in test])
        estimated = predict(matrix(test, chosen["features"]), chosen["model"])
        base_model = frozen["baselines"][axis]
        baseline = predict(matrix(test, base_model["features"]), base_model["model"])
        primitive = frozen["gradientBaselines"][axis]
        gradient_baseline = predict(
            matrix(test, primitive["features"]), primitive["model"]
        )
        result = stats(test, y, estimated, baseline)
        result["baselineIdentity"] = (
            "Development-selected ridge on existing four512px descriptors, fit with train labels only"
        )
        result["baselineMAE"] = float(np.mean(np.abs(baseline - y)))
        result["adjacentGradientSpearman"] = correlation(gradient_baseline, y)
        native = frozen["nativeModels"][axis]
        native_predicted = predict(matrix(test, native["features"]), native["model"])
        result["nativeOnlyRefinement"] = stats(test, y, native_predicted, baseline)
        constant = np.mean([x["mean"] for x in training[axis].values()])
        result["constantTrainMeanMAE"] = float(np.mean(np.abs(y - constant)))
        result["ratingCountRange"] = [
            min(x["count"] for x in labels[axis].values()),
            max(x["count"] for x in labels[axis].values()),
        ]
        result["medianRatingSEM"] = float(
            np.median([x["sem"] for x in labels[axis].values()])
        )
        result["bySource"] = {}
        for source in sorted({r["source"] for r in test}):
            indices = [i for i, r in enumerate(test) if r["source"] == source]
            result["bySource"][source] = stats(
                [test[i] for i in indices],
                y[indices],
                estimated[indices],
                baseline[indices],
            )
            result["nativeOnlyRefinement"].setdefault("bySource", {})[source] = stats(
                [test[i] for i in indices],
                y[indices],
                native_predicted[indices],
                baseline[indices],
            )
        rng = np.random.default_rng(20261007)
        half_agreement = []
        for _ in range(100):
            halves = [rng.permutation(labels[axis][r["id"]]["values"]) for r in test]
            first = [np.mean(v[: len(v) // 2]) for v in halves]
            second = [np.mean(v[len(v) // 2 :]) for v in halves]
            half_agreement.append(correlation(first, second))
        result["randomObservationHalfAgreement"] = {
            "medianSpearman": float(np.median(half_agreement)),
            "range95": np.quantile(half_agreement, [0.025, 0.975]).tolist(),
            "limits": "Random halves of observed per-image ratings, not participant-blocked reliability or a latent predictive ceiling.",
        }
        report["axes"][axis] = result
        predictions[axis] = [
            {
                "id": r["id"],
                "source": r["source"],
                "humanMean": float(y[i]),
                "ratingCount": labels[axis][r["id"]]["count"],
                "sem": labels[axis][r["id"]]["sem"],
                "predicted": float(estimated[i]),
                "baseline": float(baseline[i]),
            }
            for i, r in enumerate(test)
        ]
    save(out / "test-report.json", report)
    save(out / "test-predictions.json", predictions)
    print(
        json.dumps(
            {
                axis: {
                    k: v
                    for k, v in report["axes"][axis].items()
                    if k
                    in [
                        "nImages",
                        "spearman",
                        "spearman95CI",
                        "baselineSpearman",
                        "mae",
                        "constantTrainMeanMAE",
                        "separatedPairAccuracy",
                    ]
                }
                for axis in AXES
            },
            indent=2,
        )
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["extract", "tune", "evaluate"])
    parser.add_argument("--out", required=True)
    parser.add_argument("--images")
    parser.add_argument("--ratings")
    parser.add_argument("--aim")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    if args.command == "extract" and (not args.images or not args.ratings):
        parser.error("extract requires --images and --ratings")
    {"extract": extract, "tune": tune, "evaluate": evaluate}[args.command](args)


if __name__ == "__main__":
    main()
