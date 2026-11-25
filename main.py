#!/usr/bin/env python3
"""Famous Last Words at 1 Percent - make.fun entry.

Writes the funniest one-line farewell a phone could say as its
battery hits 1 percent to /output/entry.txt (or $OUTPUT_DIR/entry.txt).
Standard library only; fully deterministic: the same text every run.

The phone speaks in its own voice about its own dying battery:
it spent its life pretending it would read those 47 open tabs
later, and its final act of mercy is freeing the 6 a.m. alarm.
"""

import hashlib
import os
from pathlib import Path

ENTRY = (
    "Tell my 47 open tabs I died doing what I loved: pretending "
    "I'd read them later \u2014 and tell the 6 a.m. alarm: surprise, "
    "you're free too."
)


def verify(path: Path) -> None:
    """Read the written file back and verify it byte for byte.

    The digest of the bytes on disk must equal the digest of the
    intended entry encoded as UTF-8; any mismatch, a wrong length
    against the 1-to-199-character gate, blank content, or a stray
    newline aborts the run instead of submitting a corrupt entry.
    """
    data = path.read_bytes()
    expected = ENTRY.encode("utf-8")
    if hashlib.sha256(data).hexdigest() != hashlib.sha256(expected).hexdigest():
        raise SystemExit("entry digest mismatch: file on disk differs from ENTRY")
    text = data.decode("utf-8")
    if not 1 <= len(text) <= 199:
        raise SystemExit(f"entry is {len(text)} chars, must be 1-199")
    if not text.strip():
        raise SystemExit("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry must be a single line")


def main() -> None:
    out_dir = Path(os.environ.get("OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "entry.txt"
    out_path.write_text(ENTRY, encoding="utf-8")
    verify(out_path)


if __name__ == "__main__":
    main()
