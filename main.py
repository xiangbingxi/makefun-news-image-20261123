#!/usr/bin/env python3
"""Entry point for news-image-20261123.

Pure standard library: copies the finished image (entry.png, rendered
offline with PIL) to $MAKEFUN_OUTPUT_DIR/entry.png. No rendering happens
here, so the run needs no fonts and no network.
"""
import hashlib
import os
import shutil
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAX_BYTES = 1048576


def check_png_whole(data):
    """Walk every PNG chunk, verify its CRC and that IEND ends the file."""
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return "not a PNG"
    pos = 8
    seen_iend = False
    while pos + 8 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        end = pos + 8 + length + 4
        if end > len(data):
            return "truncated chunk %r" % ctype
        crc = struct.unpack(">I", data[end - 4:end])[0]
        if zlib.crc32(data[pos + 4:end - 4]) & 0xFFFFFFFF != crc:
            return "bad CRC in chunk %r" % ctype
        if ctype == b"IEND":
            seen_iend = True
            if end != len(data):
                return "trailing bytes after IEND"
            break
        pos = end
    if not seen_iend:
        return "missing IEND"
    return None


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(SRC, "rb") as f:
        data = f.read()
    err = check_png_whole(data)
    if err is not None:
        print("error: entry.png invalid (%s)" % err, file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print("error: entry.png exceeds 1 MiB", file=sys.stderr)
        return 1
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    digest = hashlib.sha256(data).hexdigest()
    print("entry.png: %d bytes sha256=%s" % (len(data), digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
