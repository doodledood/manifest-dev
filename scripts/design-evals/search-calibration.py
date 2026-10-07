#!/usr/bin/env python3
"""Calibrate target-specific descriptors on VSGUI's real website search task.

Released TIME is observed search duration, including failed localization.
Never call it correct-search time. No acquisition, network, or identity features.
"""

import argparse
import csv
import hashlib
import importlib.util
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from PIL import Image

SPEC = importlib.util.spec_from_file_location(
    "site_calibration", Path(__file__).with_name("site-calibration.py")
)
core = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(core)
METRICS = {
    "contour": "m4_0",
    "figure_ground": "m5_0",
    "subband_entropy": "m7_0",
    "feature_congestion": "m8_0",
}
CONTROLS = ["cue_i", "cue_t", "cue_tc"]
TARGET = ["log_area", "log_aspect", "center_distance", "text_length"]
IMAGE = list(METRICS)


def error_report(rows, truth, predicted, baseline):
    result = core.stats(rows, truth, predicted, baseline)
    result["nCells"] = result.pop("nImages")
    result["nImages"] = len({r["image"] for r in rows})
    result["pairLimits"] = (
        "Pairs share screens/targets; separated pairs differ by>=1 second in cell medians, not independent sample size."
    )
    result["logMAE"] = float(np.mean(np.abs(np.log(predicted) - np.log(truth))))
    result["baselineLogMAE"] = float(np.mean(np.abs(np.log(baseline) - np.log(truth))))
    groups = sorted({r["group"] for r in rows})
    by_group = {g: [i for i, r in enumerate(rows) if r["group"] == g] for g in groups}
    rng = np.random.default_rng(20261007)
    deltas = []
    error = np.abs(np.log(predicted) - np.log(truth)) - np.abs(
        np.log(baseline) - np.log(truth)
    )
    for _ in range(1000):
        indices = np.concatenate(
            [by_group[g] for g in rng.choice(groups, size=len(groups), replace=True)]
        )
        deltas.append(float(np.mean(error[indices])))
    result["deltaLogMAE95CI"] = np.quantile(deltas, [0.025, 0.975]).tolist()
    return result


def csv_rows(path):
    with Path(path).open() as stream:
        return list(csv.DictReader(stream))


def source_split(original):
    if original.startswith("CHI_13_"):
        return "development"
    if original.startswith(("AVI_14_", "CHI_15_", "IJHCS_12_", "ICWE_19_", "CHI_20_")):
        return "train"
    return "test"


def image_group(original):
    if original.startswith(("webpages_clean_", "webpages_withad_")):
        return original.replace("webpages_clean_", "webpages_").replace(
            "webpages_withad_", "webpages_"
        )
    return original


def prepare(args):
    root, out = Path(args.data), Path(args.out)
    targets = {
        (r["ueyes_img_name"], r["tgt_id"]): r
        for r in csv_rows(root / "vsgui10k_targets.csv")
    }
    metrics = {r["img_name"]: r for r in csv_rows(root / "vsgui10k_aim_results.csv")}
    trials = {}
    for row in csv_rows(root / "vsgui10k_fixations.csv"):
        if row["category"] != "web" or row["img_type"] != "2":
            continue
        key = tuple(
            row[k] for k in ["pid", "balanced_block_id", "new_img_name", "tgt_id"]
        )
        if key not in trials:
            trials[key] = {
                "metadata": row,
                "time": 0.0,
                "fixationDuration": 0.0,
                "fixationCount": 0,
            }
        trial = trials[key]
        trial["time"] = max(trial["time"], float(row["TIME"]))
        trial["fixationDuration"] += float(row["FPOGD"])
        trial["fixationCount"] += 1
    cells = defaultdict(list)
    participant_holdout = {
        r["metadata"]["pid"]
        for r in trials.values()
        if int(
            hashlib.sha256(
                ("search-participant-v1:" + r["metadata"]["pid"]).encode()
            ).hexdigest()[:8],
            16,
        )
        % 5
        == 0
    }
    image_info = {}
    excluded = defaultdict(int)
    for trial in trials.values():
        r = trial["metadata"]
        if r["absent"] not in {"True", "False"}:
            raise ValueError("Unexpected target-presence encoding")
        if r["absent"] == "True":
            excluded[
                "absent-target condition; geometry is not the absent cue location"
            ] += 1
            continue
        if trial["time"] <= 0:
            excluded["nonpositive author-equivalent search duration"] += 1
            continue
        target = targets[(r["img_name"], r["tgt_id"])]
        original = target["img_name"]
        split = source_split(original)
        if split != "test" and r["pid"] in participant_holdout:
            excluded["participant held out from fitting/development"] += 1
            continue
        key = (r["img_name"], r["tgt_id"], r["cue"])
        cells[key].append(trial)
        image_info[r["img_name"]] = {
            "original": original,
            "split": split,
            "group": image_group(original),
        }
    # Pixels enforce exact duplicates across source splits, independently of outcomes.
    by_pixels = defaultdict(list)
    for name in image_info:
        with Image.open(root / "vsgui10k-images" / name) as raw:
            image = raw.convert("RGB")
            fingerprint = hashlib.sha256(
                image.tobytes() + str(image.size).encode()
            ).hexdigest()
        by_pixels[fingerprint].append(name)
    for names in by_pixels.values():
        group = min(image_info[name]["group"] for name in names)
        priority = max(core.PRIORITY[image_info[name]["split"]] for name in names)
        for name in names:
            image_info[name]["group"] = group
            image_info[name]["excluded"] = (
                core.PRIORITY[image_info[name]["split"]] < priority
            )
    rows, labels = [], {split: {} for split in core.PRIORITY}
    for (name, target_id, cue), trials_for_cell in sorted(cells.items()):
        info = image_info[name]
        if info["excluded"]:
            excluded["exact duplicate image in a later split"] += len(trials_for_cell)
            continue
        r = trials_for_cell[0]["metadata"]
        width, height = float(r["tgt_width"]), float(r["tgt_height"])
        sx, sy = float(r["scale_x"]), float(r["scale_y"])
        if min(width, height, sx, sy) <= 0:
            raise ValueError("Present target requires positive geometry/scale")
        # Metadata scales are image fractions of a1920x1200 monitor, not
        # resize factors to multiply the original pixel dimensions again.
        aspect = (width * sx * 1920) / (height * sy * 1200)
        features = {f"cue_{c}": float(cue == c) for c in ["i", "t", "tc"]}
        features.update(
            {
                "log_area": float(np.log(width * sx * height * sy)),
                "log_aspect": float(np.log(aspect)),
                "center_distance": float(
                    np.hypot(
                        (float(r["tgt_x"]) + width / 2 - 0.5) * sx * 1920,
                        (float(r["tgt_y"]) + height / 2 - 0.5) * sy * 1200,
                    )
                    / np.hypot(1920, 1200)
                ),
                "text_length": float(len(r["tgt_text"])),
            }
        )
        for feature, column in METRICS.items():
            features[feature] = float(metrics[name][column])
        if not all(np.isfinite(v) for v in features.values()):
            raise ValueError(f"Missing/nonfinite descriptor: {name}")
        id = f"{name}|{target_id}|{cue}"
        rows.append(
            {
                "id": id,
                "image": name,
                "original": info["original"],
                "group": info["group"],
                "split": info["split"],
                "cue": cue,
                "features": features,
                "target": {
                    "x": float(r["tgt_x"]),
                    "y": float(r["tgt_y"]),
                    "width": width,
                    "height": height,
                },
            }
        )
        durations = [trial["time"] for trial in trials_for_cell]
        strict = [
            trial["time"]
            for trial in trials_for_cell
            if trial["metadata"]["pid"] in participant_holdout
        ]
        labels[info["split"]][id] = {
            "medianSeconds": float(np.median(durations)),
            "nTrials": len(durations),
            "strictHeldParticipantMedian": float(np.median(strict)) if strict else None,
            "strictHeldParticipantTrials": len(strict),
        }
    core.save(
        out / "search-features.json",
        {
            "rows": rows,
            "excluded": dict(excluded),
            "inputHashes": {
                p.name: core.digest(p)
                for p in [
                    root / "vsgui10k_fixations.csv",
                    root / "vsgui10k_targets.csv",
                    root / "vsgui10k_aim_results.csv",
                ]
            },
            "scriptSHA256": core.digest(__file__),
            "coreSHA256": core.digest(core.__file__),
            "protocolSHA256": core.digest(out / "search-plan.json"),
            "evidence": "AIM descriptors are released author outputs at source scale. Target coordinates are fixation-metadata fractions, not target-table percent. Outcome is maxTIME on search frames, including failed localization. Target-present websites only. Feature rows contain no gaze, duration or identity inputs.",
        },
    )
    for split, value in labels.items():
        core.save(out / f"search-labels-{split}.json", value)
    print(
        json.dumps(
            {
                split: {
                    "images": len({r["image"] for r in rows if r["split"] == split}),
                    "cells": sum(r["split"] == split for r in rows),
                }
                for split in core.PRIORITY
            },
            indent=2,
        )
    )


def tune(args):
    out = Path(args.out)
    data = core.load(out / "search-features.json")
    for path, field in [
        (Path(__file__), "scriptSHA256"),
        (Path(core.__file__), "coreSHA256"),
        (out / "search-plan.json", "protocolSHA256"),
    ]:
        if core.digest(path) != data[field]:
            raise ValueError(
                "Preparation inputs changed; regenerate in a fresh directory"
            )
    train = [r for r in data["rows"] if r["split"] == "train"]
    dev = [r for r in data["rows"] if r["split"] == "development"]
    labels = core.load(out / "search-labels-train.json")
    dev_labels = core.load(out / "search-labels-development.json")
    y = np.log([labels[r["id"]]["medianSeconds"] for r in train])
    target = np.log([dev_labels[r["id"]]["medianSeconds"] for r in dev])
    candidates = []
    for name, names in [
        ("cue_control", CONTROLS),
        ("target_geometry", CONTROLS + TARGET),
        ("global_image", CONTROLS + IMAGE),
        ("target_and_image", CONTROLS + TARGET + IMAGE),
    ]:
        for alpha in [0.1, 1, 10, 100, 1000]:
            model = core.fit(core.matrix(train, names), y, alpha, False)
            estimated = core.predict(core.matrix(dev, names), model)
            candidates.append(
                {
                    "name": name,
                    "features": names,
                    "alpha": alpha,
                    "model": model,
                    "developmentLogMAE": float(np.mean(np.abs(estimated - target))),
                    "developmentSpearman": core.correlation(estimated, target),
                }
            )
    candidates.sort(key=lambda c: c["developmentLogMAE"])
    frozen = {
        "winner": candidates[0],
        "arms": {
            name: next(c for c in candidates if c["name"] == name)
            for name in [
                "cue_control",
                "target_geometry",
                "global_image",
                "target_and_image",
            ]
        },
        "developmentSearch": candidates,
        "frozenHashes": {
            p.name: core.digest(p)
            for p in [
                Path(__file__),
                Path(core.__file__),
                out / "search-plan.json",
                out / "search-features.json",
                out / "search-labels-train.json",
                out / "search-labels-development.json",
                out / "search-labels-test.json",
            ]
        },
    }
    core.save(out / "search-frozen.json", frozen)
    print(
        json.dumps(
            {
                name: {k: v for k, v in arm.items() if k not in ["model", "features"]}
                for name, arm in frozen["arms"].items()
            },
            indent=2,
        )
    )


def evaluate(args):
    out = Path(args.out)
    frozen = core.load(out / "search-frozen.json")
    for filename, expected in frozen["frozenHashes"].items():
        path = (
            Path(__file__).with_name(filename)
            if filename.endswith(".py")
            else out / filename
        )
        if core.digest(path) != expected:
            raise ValueError(f"Frozen input changed: {filename}")
    with (out / "search-test-started.json").open("x") as marker:
        json.dump(
            {
                "frozenSHA256": core.digest(out / "search-frozen.json"),
                "note": "Labels consumed; repeated reads are regression evidence.",
            },
            marker,
        )
    rows = [
        r
        for r in core.load(out / "search-features.json")["rows"]
        if r["split"] == "test"
    ]
    labels = core.load(out / "search-labels-test.json")
    truth = np.array([labels[r["id"]]["medianSeconds"] for r in rows])
    baseline_arm = frozen["arms"]["cue_control"]
    baseline = np.exp(
        core.predict(core.matrix(rows, baseline_arm["features"]), baseline_arm["model"])
    )
    report = {
        "frozenSHA256": core.digest(out / "search-frozen.json"),
        "testLabelsSHA256": core.digest(out / "search-labels-test.json"),
        "arms": {},
        "winner": frozen["winner"]["name"],
        "limits": "Observed search duration, not verified success. Static screenshots viewed on laboratory monitors. Test source images unseen in fitting; same participants may occur in the main result. Strict participant sensitivity excludes held-out people from both fitting/development. Bootstrap clusters screenshot/template groups and omits remaining participant variation.",
    }
    predictions = {}
    for name, arm in frozen["arms"].items():
        estimated = np.exp(
            core.predict(core.matrix(rows, arm["features"]), arm["model"])
        )
        result = error_report(rows, truth, estimated, baseline)
        result["byCue"] = {}
        for cue in sorted({r["cue"] for r in rows}):
            indices = [i for i, r in enumerate(rows) if r["cue"] == cue]
            result["byCue"][cue] = error_report(
                [rows[i] for i in indices],
                truth[indices],
                estimated[indices],
                baseline[indices],
            )
        indices = [
            i
            for i, r in enumerate(rows)
            if labels[r["id"]]["strictHeldParticipantMedian"] is not None
        ]
        strict_truth = np.array(
            [labels[rows[i]["id"]]["strictHeldParticipantMedian"] for i in indices]
        )
        result["unseenParticipantsAndImages"] = error_report(
            [rows[i] for i in indices],
            strict_truth,
            estimated[indices],
            baseline[indices],
        )
        report["arms"][name] = result
        predictions[name] = [
            {
                "id": r["id"],
                "image": r["image"],
                "cue": r["cue"],
                "target": r["target"],
                "observedMedianSeconds": float(truth[i]),
                "predictedSeconds": float(estimated[i]),
                "nTrials": labels[r["id"]]["nTrials"],
            }
            for i, r in enumerate(rows)
        ]
    core.save(out / "search-test-report.json", report)
    core.save(out / "search-test-predictions.json", predictions)
    print(
        json.dumps(
            {
                name: {
                    k: v
                    for k, v in result.items()
                    if k
                    in [
                        "spearman",
                        "spearman95CI",
                        "mae",
                        "logMAE",
                        "nImages",
                        "nDuplicateGroups",
                    ]
                }
                for name, result in report["arms"].items()
            },
            indent=2,
        )
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare", "tune", "evaluate"])
    parser.add_argument("--out", required=True)
    parser.add_argument("--data")
    args = parser.parse_args()
    {"prepare": prepare, "tune": tune, "evaluate": evaluate}[args.command](args)


if __name__ == "__main__":
    main()
