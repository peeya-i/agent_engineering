"""Deterministically calculate discount amount and net ARR.

Example:
  python calculate_quote.py --arr 92000 --discount-percent 12
"""

import argparse
import json
from decimal import Decimal, ROUND_HALF_UP


def money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--arr", type=Decimal, required=True)
    parser.add_argument("--discount-percent", type=Decimal, required=True)
    args = parser.parse_args()

    if args.arr < 0:
        raise SystemExit("arr must be non-negative")
    if args.discount_percent < 0 or args.discount_percent > 100:
        raise SystemExit("discount-percent must be between 0 and 100")

    discount_amount = money(args.arr * args.discount_percent / Decimal("100"))
    net_arr = money(args.arr - discount_amount)
    result = {
        "arr": f"{money(args.arr):.2f}",
        "discount_percent": f"{args.discount_percent.normalize()}",
        "discount_amount": f"{discount_amount:.2f}",
        "net_arr": f"{net_arr:.2f}",
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
