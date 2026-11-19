#!/usr/bin/env python3
"""news-image-20261119: write the front page image to the output dir.

The entry image (entry.png, a 1024x1024 front page summing up the world
news of Thursday 19 November 2026) ships in this repository next to this
program. This program only copies it to $MAKEFUN_OUTPUT_DIR (default
/output) after checking it is a whole PNG. Standard library only, no
network, fully deterministic: the same bytes are written on every run.
"""

import hashlib
import os
import struct
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
# A whole PNG ends with the 12-byte IEND chunk: zero length, "IEND",
# and its fixed CRC.
PNG_IEND = b"\x00\x00\x00\x00IEND\xaeB`\x82"


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dst = os.path.join(out_dir, "entry.png")

    with open(src, "rb") as f:
        data = f.read()

    if not data.startswith(PNG_MAGIC):
        print("entry.png: bad PNG magic", file=sys.stderr)
        return 1
    if not data.endswith(PNG_IEND):
        print("entry.png: missing IEND trailer", file=sys.stderr)
        return 1
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        print(f"entry.png: expected 1024x1024, got {width}x{height}",
              file=sys.stderr)
        return 1
    if len(data) > 1048576:
        print("entry.png: over the 1 MiB limit", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    with open(dst, "wb") as f:
        f.write(data)

    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {dst} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
