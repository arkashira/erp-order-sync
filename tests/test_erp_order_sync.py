import json
import os
from pathlib import Path

import pytest

from erp_order_sync import load_and_normalise, write_json, _normalise_csv_rows, _normalise_json_orders


def test_normalise_csv_rows_happy_path():
    rows = [
        {
            "order_id": "1001",
            "customer": "Acme Corp",
            "item_sku": "ABC-1",
            "quantity": "2",
            "price": "9.99",
        },
        {
            "order_id": "1001",
            "customer": "Acme Corp",
            "item_sku": "XYZ-5",
            "quantity": "1",
            "price": "19.95",
        },
        {
            "order_id": "1002",
            "customer": "Globex",
            "item_sku": "LMN-3",
            "quantity": "5",
            "price": "4.5",
        },
    ]
    orders = _normalise_csv_rows(rows)
    assert len(orders) == 2
    # Verify first order
    o1 = next(o for o in orders if o.order_id == "1001")
    assert o1.customer == "Acme Corp"
    assert len(o1.items) == 2
    assert o1.items[0].sku == "ABC-1"
    assert o1.items[0].quantity == 2
    assert o1.items[0].price == 9.99
    # Verify second order
    o2 = next(o for o in orders if o.order_id == "1002")
    assert o2.customer == "Globex"
    assert len(o2.items) == 1
    assert o2.items[0].sku == "LMN-3"


def test_normalise_csv_rows_inconsistent_customer_raises():
    rows = [
        {
            "order_id": "1001",
            "customer": "Acme Corp",
            "item_sku": "ABC-1",
            "quantity": "2",
            "price": "9.99",
        },
        {
            "order_id": "1001",
            "customer": "Other Corp",
            "item_sku": "XYZ-5",
            "quantity": "1",
            "price": "19.95",
        },
    ]
    with pytest.raises(ValueError, match="Inconsistent customer name"):
        _normalise_csv_rows(rows)


def test_normalise_json_orders_happy_path():
    raw = [
        {
            "id": "2001",
            "client": "Beta Ltd",
            "products": [
                {"sku": "A1", "qty": 3, "price": 5.0},
                {"sku": "B2", "qty": 1, "price": 12.5},
            ],
        },
        {
            "id": "2002",
            "client": "Gamma Inc",
            "products": [{"sku": "C3", "qty": 7, "price": 2.2}],
        },
    ]
    orders = _normalise_json_orders(raw)
    assert len(orders) == 2
    assert orders[0].order_id == "2001"
    assert orders[0].customer == "Beta Ltd"
    assert len(orders[0].items) == 2
    assert orders[0].items[1].sku == "B2"
    assert orders[0].items[1].quantity == 1
    assert orders[0].items[1].price == 12.5


def test_load_and_normalise_csv_file(tmp_path: Path):
    csv_content = """order_id,customer,item_sku,quantity,price
1001,Acme Corp,ABC-1,2,9.99
1001,Acme Corp,XYZ-5,1,19.95
"""
    csv_file = tmp_path / "orders.csv"
    csv_file.write_text(csv_content, encoding="utf-8")
    result = load_and_normalise(str(csv_file))
    assert isinstance(result, list)
    assert result[0]["order_id"] == "1001"
    assert len(result[0]["items"]) == 2


def test_write_json_creates_file(tmp_path: Path):
    data = [
        {"order_id": "1", "customer": "C", "items": [{"sku": "X", "quantity": 1, "price": 0.99}]}
    ]
    out_file = tmp_path / "out.json"
    write_json(data, str(out_file))
    assert out_file.is_file()
    loaded = json.loads(out_file.read_text(encoding="utf-8"))
    assert loaded == data
