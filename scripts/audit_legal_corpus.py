"""Validate the on-disk legal corpus before vector ingestion.

The audit intentionally does not decide whether a source is current. It checks
that every PDF has provenance metadata, is readable, and exposes basic text.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
LEGAL_ROOT = ROOT / "knowledge" / "legal"
REQUIRED = {"title", "source_type", "source_url", "official_source", "status", "jurisdiction", "last_verified"}


def main() -> int:
    failures = 0
    for pdf in sorted(LEGAL_ROOT.rglob("*.pdf")):
        sidecar = pdf.with_suffix(".metadata.json")
        if not sidecar.exists():
            print(f"FAIL metadata missing: {pdf.relative_to(ROOT)}")
            failures += 1
            continue
        metadata = json.loads(sidecar.read_text(encoding="utf-8"))
        missing = REQUIRED - metadata.keys()
        if missing:
            print(f"FAIL metadata fields missing: {pdf.name}: {', '.join(sorted(missing))}")
            failures += 1
            continue
        try:
            reader = PdfReader(str(pdf))
            text = reader.pages[0].extract_text() or ""
            if not text.strip():
                raise ValueError("first page has no extractable text")
            print(f"OK {pdf.relative_to(ROOT)} | pages={len(reader.pages)} | status={metadata['status']}")
        except Exception as exc:
            print(f"FAIL unreadable: {pdf.relative_to(ROOT)}: {exc}")
            failures += 1
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
