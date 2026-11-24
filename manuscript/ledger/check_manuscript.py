#!/usr/bin/env python3
"""Confirm the manuscript quotes the ledger's headline figures."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT = "\n".join(p.read_text() for p in sorted(ROOT.glob("*.md")))

REQUIRED = [
    "€259,145",
    "€430,708",
    "€690,000",
    "€179,811",
    "€213,898",
    "5.99 percent",
    "€730,000",
    "2.90",
    "3.84",
    "€176,700",
    "€63,300",
    "€70,000,000",
    "€64,400,000",
    "€48,000,000",
    "€42,400,000",
    "€12,880,000",
    "€8,480,000",
    "€44,384",
    "€2,400,000",
    "€36,000",
    "€324,000",
    "€1,338,484",
    "€1,361,516",
    "€1,846,600",
    "€166,600",
    "32.975 percent",
    "€194,932",
    "€33,979",
    "€3,703,704",
    "€3,508,772",
    "€175,610",
    "7.3 percent",
    "€4,200,000",
    "73 days",
    "€579,324",
    "€453,888",
    "6.92 percent",
    "€5,454,545",
    "€14,795",
    "€6,360,000",
    "0.225 percent",
    "€1,137,338",
    "€224,177",
    "€438,484",
    "€681,075",
    "€87,805",
    "€360,000",
]


def main() -> None:
    missing = [s for s in REQUIRED if s not in TEXT]
    if missing:
        raise SystemExit("missing figures:\n" + "\n".join(missing))
    print(f"ok, {len(REQUIRED)} figures found")


if __name__ == "__main__":
    main()
