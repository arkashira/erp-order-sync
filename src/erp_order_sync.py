"""erp_order_sync – normalise order files (CSV/JSON) into a JSON payload.

Public API
---------
- load_and_normalise(input_path: str) -> list[dict]
- write_json(data: list[dict], output_path: str) -> None
- main() – entry point for the console script.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
from collections import defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, List, Mapping, MutableMapping


@dataclass
class Item:
    sku: str
    quantity: int
    price: float

    def to_dict(self) -> dict:
        return {"sku": self.sku, "quantity": self.quantity, "price": self.price}


@dataclass
class Order:
    order_id: str
    customer: str
    items: List[Item]

    def to_dict(self) -> dict:
        return {
            "order_id": self.order_id,
            "customer": self.customer,
            "items": [item.to_dict() for item in self.items],
        }


def _detect_format(path: Path) -> str:
    """Return 'csv' or 'json' based on file extension."""
    ext = path.suffix.lower()
    if ext == ".csv":
        return "csv"
    if ext == ".json":
        return "json"
    raise ValueError(f"Unsupported file extension: {ext}")


def _load_csv(path: Path) -> List[Mapping[str, str]]:
    """Read a CSV file and return a list of row dictionaries."""
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        raise ValueError("CSV file is empty or has no data rows.")
    required = {"order_id", "customer", "item_sku", "quantity", "price"}
    missing = required - set(rows[0].keys())
    if missing:
        raise ValueError(f"CSV missing required columns: {missing}")
    return rows


def _load_json(path: Path) -> List[Mapping]:
    """Read a JSON file and return the parsed object (expected list)."""
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("JSON root must be a list of orders.")
    if not data:
        raise ValueError("JSON file contains an empty list.")
    return data


def _normalise_csv_rows(rows: Iterable[Mapping[str, str]]) -> List[Order]:
    """Group CSV rows by order_id and produce Order objects."""
    grouped: MutableMapping[str, dict] = defaultdict(lambda: {"customer": "", "items": []})
    for row in rows:
        oid = row["order_id"]
        customer = row["customer"]
        sku = row["item_sku"]
        try:
            quantity = int(row["quantity"])
            price = float(row["price"])
        except ValueError as exc:
            raise ValueError(f"Invalid numeric value in row {row}") from exc

        if not grouped[oid]["customer"]:
            grouped[oid]["customer"] = customer
        elif grouped[oid]["customer"] != customer:
            raise ValueError(f"Inconsistent customer name for order {oid}")

        grouped[oid]["items"].append(Item(sku=sku, quantity=quantity, price=price))

    orders = [
        Order(order_id=oid, customer=info["customer"], items=info["items"])
        for oid, info in grouped.items()
    ]
    return orders


def _normalise_json_orders(raw_orders: Iterable[Mapping]) -> List[Order]:
    """Convert JSON order objects (with flexible keys) into Order objects."""
    orders: List[Order] = []
    for raw in raw_orders:
        try:
            oid = str(raw["id"])
            customer = raw["client"]
            products = raw["products"]
        except KeyError as exc:
            raise ValueError(f"Missing required key {exc} in JSON order {raw}") from exc

        items = []
        for prod in products:
            try:
                sku = prod["sku"]
                quantity = int(prod["qty"])
                price = float(prod["price"])
            except (KeyError, ValueError) as exc:
                raise ValueError(f"Invalid product entry {prod} in order {oid}") from exc
            items.append(Item(sku=sku, quantity=quantity, price=price))

        orders.append(Order(order_id=oid, customer=customer, items=items))
    return orders


def load_and_normalise(input_path: str) -> List[dict]:
    """Load a CSV or JSON order file, normalise it, and return a list of dicts."""
    path = Path(input_path)
    fmt = _detect_format(path)
    if fmt == "csv":
        raw_rows = _load_csv(path)
        orders = _normalise_csv_rows(raw_rows)
    else:  # json
        raw_orders = _load_json(path)
        orders = _normalise_json_orders(raw_orders)

    return [order.to_dict() for order in orders]


def write_json(data: List[dict], output_path: str) -> None:
    """Write the normalised data to a JSON file with pretty formatting."""
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Normalise order files for ERP sync.")
    parser.add_argument("--input", required=True, help="Path to input CSV or JSON file.")
    parser.add_argument("--output", required=True, help="Path to write normalised JSON.")
    return parser


def main() -> None:
    parser = _build_arg_parser()
    args = parser.parse_args()
    normalised = load_and_normalise(args.input)
    write_json(normalised, args.output)
    print(f"Wrote {len(normalised)} orders to {args.output}")


if __name__ == "__main__":
    main()
