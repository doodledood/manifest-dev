#!/usr/bin/env python3
"""External full-page check of frozen homepage models; no fitting or acquisition.

Uses a caller-owned sample and participant-standardized appearance ratings from
the three Dataverse collections named in external-plan.json. Dependencies are
the same as site-calibration.py. Both full-page and top900 variants are reported.
"""

import argparse
import csv
import importlib.util
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

SPEC = importlib.util.spec_from_file_location(
    "calibration", Path(__file__).with_name("site-calibration.py")
)
core = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(core)


def feature_pair(args):
    row, root, aim = args
    root = Path(root)
    path = root / "images" / row["filename"]
    full = core.image_features((path, aim))
    crop = root / "top900" / (path.stem + ".png")
    with Image.open(path) as image:
        image = ImageOps.exif_transpose(image)
        image.crop((0, 0, image.width, min(900, image.height))).save(crop)
    top = core.image_features((crop, aim))
    return {**row, "full": full, "top900": top}


def extract(args):
    root = Path(args.root)
    sample = core.load(root / "sample-freeze.json")
    if len(sample["rows"]) != 420:
        raise ValueError("Expected the preselected420 screens")
    paths = [
        Path(__file__),
        Path(core.__file__),
        root / "external-plan.json",
        root / "sample-freeze.json",
        Path(args.models),
    ] + sorted(root.glob("ratings.avg.*.txt"))
    hashes = {str(p.resolve()): core.digest(p) for p in paths}
    (root / "top900").mkdir(exist_ok=True)
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        rows = []
        for i, row in enumerate(
            pool.map(feature_pair, [(r, str(root), args.aim) for r in sample["rows"]])
        ):
            rows.append(row)
            if (i + 1) % 50 == 0:
                print(f"Extracted{i + 1}/420 full-page/crop pairs", flush=True)
    corpus = core.load(Path(args.models).with_name("features.json"))["rows"]
    exact = {r["pixelHash"] for r in corpus}
    overlaps = []
    for row in rows:
        for variant in ["full", "top900"]:
            view = row[variant]
            row[variant]["exactPriorCorpusOverlap"] = view["pixelHash"] in exact
            near = []
            for prior in corpus:
                dh = (
                    int(view["differenceHash"], 16) ^ int(prior["differenceHash"], 16)
                ).bit_count()
                ph = (
                    int(view["perceptualHash"], 16) ^ int(prior["perceptualHash"], 16)
                ).bit_count()
                if dh <= 5 and ph <= 8:
                    near.append({"id": prior["id"], "dHash": dh, "pHash": ph})
            if near or view["pixelHash"] in exact:
                overlaps.append(
                    {
                        "id": row["filename"],
                        "variant": variant,
                        "exact": view["pixelHash"] in exact,
                        "nearCandidates": near,
                    }
                )
    if any(core.digest(p) != expected for p, expected in hashes.items()):
        raise ValueError("Source, protocol or frozen model changed during extraction")
    core.save(
        root / "external-features.json",
        {
            "frozenHashes": hashes,
            "models": str(Path(args.models).resolve()),
            "rows": rows,
            "priorCorpusOverlapCandidates": overlaps,
            "limits": "Near candidates are screening flags, not confirmed domains/templates. Unknown brand overlap remains. Full-page512max-edge scaling can erase text; top900 is a distinct predeclared input condition.",
        },
    )


def rank_report(rows, truth, predicted, baseline):
    # Exact duplicates share a bootstrap group. Brand/template IDs unavailable.
    groups = sorted({r["group"] for r in rows})
    indices = {g: [i for i, r in enumerate(rows) if r["group"] == g] for g in groups}
    rng = np.random.default_rng(20261007)
    rho, delta = [], []
    for _ in range(1000):
        sample = np.concatenate(
            [indices[g] for g in rng.choice(groups, len(groups), replace=True)]
        )
        a = core.correlation(truth[sample], predicted[sample])
        b = core.correlation(truth[sample], baseline[sample])
        if a is not None and np.isfinite(a):
            rho.append(a)
        if a is not None and b is not None and np.isfinite(a + b):
            delta.append(a - b)
    return {
        "nImages": len(rows),
        "nExactPixelGroups": len(groups),
        "spearman": core.correlation(truth, predicted),
        "spearman95CI": np.quantile(rho, [0.025, 0.975]).tolist() if rho else None,
        "baselineSpearman": core.correlation(truth, baseline),
        "deltaSpearman95CI": (
            np.quantile(delta, [0.025, 0.975]).tolist() if delta else None
        ),
    }


def evaluate(args):
    root = Path(args.root)
    data = core.load(root / "external-features.json")
    for path, expected in data["frozenHashes"].items():
        if core.digest(path) != expected:
            raise ValueError(f"Frozen input changed: {Path(path).name}")
    with (root / "external-test-started.json").open("x") as marker:
        json.dump(
            {
                "featuresSHA256": core.digest(root / "external-features.json"),
                "note": "Labels consumed; all later uses are regression evidence.",
            },
            marker,
        )
    labels = {}
    selected = {r["filename"] for r in data["rows"]}
    for path in sorted(root.glob("ratings.avg.*.txt")):
        with path.open() as stream:
            for row in csv.DictReader(stream, delimiter="\t"):
                if row["stimulusId"] not in selected:
                    continue
                values = {k: float(row[k]) for k in ["AE", "US", "TRU"]}
                if row["stimulusId"] in labels:
                    if labels[row["stimulusId"]] != values:
                        raise ValueError("Conflicting duplicate rating ID")
                    continue
                labels[row["stimulusId"]] = values
    frozen = core.load(data["models"])
    report = {
        "modelsSHA256": core.digest(data["models"]),
        "featuresSHA256": core.digest(root / "external-features.json"),
        "variants": {},
        "overlapCandidates": data["priorCorpusOverlapCandidates"],
        "limits": "Published2024 independent rating study;420 filename-hash-selected full-page homepages. AE appearance, US perceived ease, TRU perceived trust; no task success or actual trust. CIs cluster exact pixels, not raters/brands/templates. Scores trained on1-7 first impressions are assessed by ranks against participant-standardized ratings, without refitting or MAE comparison across incompatible scales. Exploratory US/TRU correlations are associations, not predicted task behavior.",
    }
    predictions = {}
    for variant in ["full", "top900"]:
        rows = [r for r in data["rows"] if not r[variant]["exactPriorCorpusOverlap"]]
        views = [{**r[variant], "group": r[variant]["pixelHash"]} for r in rows]
        base = frozen["baselines"]["aesthetics"]
        baseline = core.predict(core.matrix(views, base["features"]), base["model"])
        models = {
            "aesthetics_selected": frozen["models"]["aesthetics"],
            "aesthetics_native": frozen["nativeModels"]["aesthetics"],
            "complexity_selected": frozen["models"]["complexity"],
            "craftsmanship_selected": frozen["models"]["craftsmanship"],
        }
        report["variants"][variant] = {}
        predictions[variant] = []
        for name, model in models.items():
            predicted = core.predict(
                core.matrix(views, model["features"]), model["model"]
            )
            axis_reports = {}
            for axis in (
                ["AE", "US", "TRU"] if name != "aesthetics_native" else ["AE"]
            ):
                truth = np.array([labels[r["filename"]][axis] for r in rows])
                result = rank_report(views, truth, predicted, baseline)
                result["byGenre"] = {}
                for genre in sorted({r["genre"] for r in rows}):
                    idx = [i for i, r in enumerate(rows) if r["genre"] == genre]
                    result["byGenre"][genre] = rank_report(
                        [views[i] for i in idx],
                        truth[idx],
                        predicted[idx],
                        baseline[idx],
                    )
                axis_reports[axis] = result
            report["variants"][variant][name] = axis_reports
            for i, row in enumerate(rows):
                predictions[variant].append(
                    {
                        "id": row["filename"],
                        "genre": row["genre"],
                        "model": name,
                        "predicted": float(predicted[i]),
                        "human": labels[row["filename"]],
                    }
                )
    core.save(root / "external-report.json", report)
    core.save(root / "external-predictions.json", predictions)
    print(
        json.dumps(
            {
                v: report["variants"][v]["aesthetics_selected"]["AE"]
                for v in report["variants"]
            },
            indent=2,
        )
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["extract", "evaluate"])
    parser.add_argument("--root", required=True)
    parser.add_argument("--models")
    parser.add_argument("--aim")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    if args.command == "extract" and not args.models:
        parser.error("extract requires --models")
    {"extract": extract, "evaluate": evaluate}[args.command](args)


if __name__ == "__main__":
    main()
