"""Read local source HTML or decode supplied images; never render or fetch assets."""

from __future__ import annotations

import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


class SourceHTML(HTMLParser):
    """Source inventory without browser tree repair, CSS or JavaScript evaluation."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.elements: list[dict[str, Any]] = []
        self.stack: list[dict[str, Any]] = []
        self.nodes: list[dict[str, Any]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        e: dict[str, Any] = {
            "id": f"source-{len(self.elements)}",
            "tag": tag,
            "attributes": dict(attrs),
            "ancestors": list(self.stack),
            "text": [],
        }
        self.elements.append(e)
        if tag not in {
            "area",
            "base",
            "br",
            "col",
            "embed",
            "hr",
            "img",
            "input",
            "link",
            "meta",
            "param",
            "source",
            "track",
            "wbr",
        }:
            self.stack.append(e)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                self.stack = self.stack[:i]
                break

    def handle_data(self, data: str) -> None:
        if any(e["tag"] in {"head", "script", "style", "template"} for e in self.stack):
            return
        text = " ".join(data.split())
        if not text:
            return
        for e in self.stack:
            e["text"].append(data)
        self.nodes.append(
            {
                "id": f"text-{len(self.nodes)}",
                "text": text,
                "entityRef": self.stack[-1]["id"] if self.stack else None,
            }
        )

    def inventory(self) -> dict[str, Any]:
        def text(e: dict[str, Any]) -> str:
            return " ".join("".join(e["text"]).split())

        def inert(e: dict[str, Any]) -> bool:
            return any(
                p["tag"] in {"head", "script", "style", "template"}
                for p in e["ancestors"]
            )

        labels = [e for e in self.elements if e["tag"] == "label" and not inert(e)]
        controls = []
        media = []
        headings = []
        languages = []
        for e in self.elements:
            a = e["attributes"]
            if inert(e):
                continue
            entry = {
                "id": e["id"],
                "sourceId": a.get("id"),
                "tag": e["tag"],
                "text": text(e),
            }
            if "lang" in a or "dir" in a:
                languages.append(
                    {**entry, "language": a.get("lang"), "direction": a.get("dir")}
                )
            if e["tag"] in {"h1", "h2", "h3", "h4", "h5", "h6"}:
                headings.append({**entry, "level": int(e["tag"][1])})
            if e["tag"] in {"img", "video", "audio", "source", "svg", "canvas"}:
                media.append(
                    {
                        **entry,
                        "src": a.get("src"),
                        "alt": a.get("alt"),
                        "declaredWidth": a.get("width"),
                        "declaredHeight": a.get("height"),
                    }
                )
            if (
                e["tag"] not in {"input", "select", "textarea", "button", "summary"}
                and not (e["tag"] == "a" and "href" in a)
                and a.get("role")
                not in {
                    "button",
                    "link",
                    "checkbox",
                    "textbox",
                    "tab",
                    "switch",
                    "radio",
                    "combobox",
                    "menuitem",
                    "slider",
                    "spinbutton",
                }
            ):
                continue
            if e["tag"] == "input" and a.get("type", "").lower() == "hidden":
                continue
            associated = [
                text(p)
                for p in labels
                if (a.get("id") and p["attributes"].get("for") == a["id"])
                or any(p is ancestor for ancestor in e["ancestors"])
            ]
            candidate = (
                a.get("aria-label")
                or " ".join(associated)
                or text(e)
                or (
                    a.get("value")
                    if e["tag"] == "input"
                    and a.get("type", "").lower() in {"button", "submit", "reset"}
                    else None
                )
                or a.get("alt")
                or a.get("title")
            )
            controls.append(
                {
                    **entry,
                    "role": a.get("role"),
                    "nameCandidate": candidate or None,
                    "associatedLabels": associated,
                    "ariaLabelledby": a.get("aria-labelledby"),
                    "placeholder": a.get("placeholder"),
                    "attributes": a,
                    "sourceHidden": any(
                        "hidden" in p["attributes"] for p in [*e["ancestors"], e]
                    ),
                }
            )
        return {
            "nodes": self.nodes,
            "controls": controls,
            "headings": headings,
            "media": media,
            "languages": languages,
            "coverage": {
                "basis": "HTML source; no execution, CSS, browser tree repair or external resources",
                "rendered": False,
            },
        }


def image(path: str, artifact_dir: str | None) -> dict[str, Any]:
    try:
        from PIL import Image, ImageFilter, ImageOps
    except ImportError as error:
        raise ValueError(
            "Image decoding requires Pillow: install it in your Python environment and set DESIGN_TOOLS_PYTHON if needed"
        ) from error
    with Image.open(path) as supplied:
        orientation = supplied.getexif().get(274, 1)
        frame = ImageOps.exif_transpose(supplied).convert("RGBA")
        original = {"width": frame.width, "height": frame.height}
        white = Image.new("RGBA", frame.size, "white")
        white.alpha_composite(frame)
        full = white.convert("RGB")
        files = []
        if artifact_dir:
            directory = Path(artifact_dir)
            directory.mkdir(parents=True, exist_ok=True)
            thumb = full.copy()
            thumb.thumbnail((240, 240), Image.Resampling.LANCZOS)
            for name, view in [
                ("grayscale.png", ImageOps.grayscale(full)),
                ("blur.png", full.filter(ImageFilter.GaussianBlur(8))),
                ("thumbnail.png", thumb),
            ]:
                view.save(directory / name)
                files.append(name)
        full.thumbnail((512, 512), Image.Resampling.LANCZOS)
        return {
            "width": full.width,
            "height": full.height,
            "data": list(full.convert("RGBA").tobytes()),
            "originalSize": original,
            "decoder": f"Pillow {Image.__version__}",
            "resampling": "LANCZOS; maximum edge 512",
            "exifOrientationApplied": orientation != 1,
            "scope": "First frame; alpha composited over white; embedded ICC profiles not transformed",
            "artifacts": files,
        }


def main() -> None:
    if sys.argv[1] == "html":
        parser = SourceHTML()
        parser.feed(sys.stdin.read())
        parser.close()
        result = parser.inventory()
    elif sys.argv[1] == "image":
        result = image(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    else:
        raise ValueError("Unknown artifact input")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        print(f"artifact-input: {error}", file=sys.stderr)
        sys.exit(1)
