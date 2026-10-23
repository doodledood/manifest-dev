"""Shipped brand marks stay RGBA with a transparent field.

Dropping an opaque RGB export into assets/logo.png or site/logo.png paints a
square on GitHub dark-mode README and the Pages favicon. IHDR color type 6
plus transparent corners fail that class.
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
