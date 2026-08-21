#!/usr/bin/env python3
"""Calculate deterministic renewal quote values.

Usage:
    python calculate_quote.py --arr 92000 --discount-pct 12
"""

from __future__ import annotations

import argparse
import json


def calculate_quote(arr: float, discount_pct: float) -> dict[str, float]:
    """Return list ARR, discount amount, and net ARR."""
    if arr < 0:
        raise ValueError("arr must be >= 0")
    if not 0 <= discount_pct <= 100:
        raise ValueError("discount_pct must be between 0 and 100")

    discount_amount = arr * (discount_pct / 100.0)
    net_arr = arr - discount_amount

    return {
        "list_arr": round(arr, 2),
        "discount_pct": round(discount_pct, 4),
        "discount_amount": round(discount_amount, 2),
        "net_arr": round(net_arr, 2),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--arr", type=float, required=True)
    parser.add_argument("--discount-pct", type=float, required=True)
    args = parser.parse_args()
    print(json.dumps(calculate_quote(args.arr, args.discount_pct), indent=2))


if __name__ == "__main__":
    main()
