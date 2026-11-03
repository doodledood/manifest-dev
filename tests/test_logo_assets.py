"""Shipped brand marks stay RGBA with a transparent field; Cursor's copies are plated.

Dropping an opaque RGB export into assets/logo.png or site/logo.png paints a
square on GitHub dark-mode README and the Pages favicon. IHDR color type 6
plus transparent corners fail that class.

The Cursor Marketplace asks for a 1:1 logo on a background plate, so each Cursor
plugin ships the same mark over an opaque plate inside its own directory
(docs/adr/20261103-each-cursor-plugin-ships-its-own-plated-logo.md).
"""

from __future__ import annotations

import struct
import zlib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
LOGO_PATHS = (ROOT / "assets" / "logo.png", ROOT / "site" / "logo.png")


def _png_ihdr_and_pixels(path: Path) -> tuple[int, int, bytes]:
    data = path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", f"{path} is not a PNG"
    pos = 8
    width = height = bit_depth = color_type = None
    idat = bytearray()
    while pos + 8 <= len(data):
        length = int.from_bytes(data[pos : pos + 4], "big")
        kind = data[pos + 4 : pos + 8]
        chunk = data[pos + 8 : pos + 8 + length]
        pos += 12 + length
        if kind == b"IHDR":
            width, height, bit_depth, color_type, *_ = struct.unpack(">IIBBBBB", chunk)
        elif kind == b"IDAT":
            idat.extend(chunk)
        elif kind == b"IEND":
            break
    assert isinstance(width, int) and isinstance(height, int)
    assert color_type == 6, f"{path} must be RGBA (IHDR color type 6), got {color_type}"
    assert bit_depth == 8, f"{path} must be 8-bit, got {bit_depth}"
    raw = zlib.decompress(bytes(idat))
    bpp = 4
    stride = width * bpp
    rows: list[bytearray] = []
    prev = bytearray(stride)
    i = 0
    for _ in range(height):
        filt = raw[i]
        scan = bytearray(raw[i + 1 : i + 1 + stride])
        i += 1 + stride
        if filt == 1:
            for x in range(stride):
                scan[x] = (scan[x] + (scan[x - bpp] if x >= bpp else 0)) & 255
        elif filt == 2:
            for x in range(stride):
                scan[x] = (scan[x] + prev[x]) & 255
        elif filt == 3:
            for x in range(stride):
                left = scan[x - bpp] if x >= bpp else 0
                scan[x] = (scan[x] + (left + prev[x]) // 2) & 255
        elif filt == 4:
            for x in range(stride):
                a = scan[x - bpp] if x >= bpp else 0
                b = prev[x]
                c = prev[x - bpp] if x >= bpp else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if pa <= pb and pa <= pc else b if pb <= pc else c
                scan[x] = (scan[x] + pr) & 255
        elif filt != 0:
            raise AssertionError(f"{path}: unsupported PNG filter {filt}")
        rows.append(scan)
        prev = scan
    return width, height, b"".join(rows)


@pytest.mark.parametrize("path", LOGO_PATHS, ids=lambda p: p.name)
def test_shipped_logo_has_transparent_field(path: Path) -> None:
    assert path.is_file(), path
    width, height, pixels = _png_ihdr_and_pixels(path)
    assert path.stat().st_size < 200_000, f"{path} is {path.stat().st_size} bytes"

    def alpha(x: int, y: int) -> int:
        return pixels[(y * width + x) * 4 + 3]

    corners = (
        alpha(0, 0),
        alpha(width - 1, 0),
        alpha(0, height - 1),
        alpha(width - 1, height - 1),
    )
    assert corners == (0, 0, 0, 0), f"{path} corners are not transparent: {corners}"


PLATED_LOGO_PATHS = tuple(
    ROOT / "claude-plugins" / plugin / "assets" / "logo.png"
    for plugin in ("manifest-dev", "manifest-dev-tools")
)


# Holds docs/adr/20261103-each-cursor-plugin-ships-its-own-plated-logo.md.
def test_cursor_plugin_logos_are_the_mark_on_an_opaque_square_plate() -> None:
    """Each plugin's logo is square, opaque everywhere, identical across plugins,
    and matches assets/logo.png wherever the mark itself is opaque, so the plated
    copy cannot drift from the brand mark."""
    first = PLATED_LOGO_PATHS[0].read_bytes()
    for path in PLATED_LOGO_PATHS:
        assert path.is_file(), path
        assert path.read_bytes() == first, f"{path} differs from {PLATED_LOGO_PATHS[0]}"
        assert path.stat().st_size < 200_000, f"{path} is {path.stat().st_size} bytes"
    width, height, plated = _png_ihdr_and_pixels(PLATED_LOGO_PATHS[0])
    src_w, src_h, mark = _png_ihdr_and_pixels(LOGO_PATHS[0])
    assert width == height == src_w == src_h, (width, height, src_w, src_h)
    assert all(a == 255 for a in plated[3::4]), "plated logo has transparent pixels"
    for i in range(0, len(mark), 4):
        if mark[i + 3] == 255:
            assert plated[i : i + 3] == mark[i : i + 3], f"pixel {i // 4} drifted"
