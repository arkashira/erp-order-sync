import json
from dataclasses import dataclass
from typing import List

@dataclass
class Order:
    id: int
    customer_name: str
    order_date: str
    total: float

class ErpOrderSync:
    def __init__(self, erp_system, external_source):
        self.erp_system = erp_system
        self.external_source = external_source

    def sync_orders(self) -> List[Order]:
        external_orders = self.external_source.get_orders()
        erp_orders = self.erp_system.get_orders()

        # Map and transform orders according to predefined rules
        mapped_orders = []
        for order in external_orders:
            if order not in erp_orders:
                mapped_order = Order(
                    id=order['id'],
                    customer_name=order['customer_name'],
                    order_date=order['order_date'],
                    total=order['total']
                )
                mapped_orders.append(mapped_order)

        return mapped_orders

class ErpSystem:
    def __init__(self):
        self.orders = []

    def get_orders(self) -> List[dict]:
        return self.orders

    def add_order(self, order: Order):
        self.orders.append({
            'id': order.id,
            'customer_name': order.customer_name,
            'order_date': order.order_date,
            'total': order.total
        })

class ExternalSource:
    def __init__(self, orders: List[dict]):
        self.orders = orders

    def get_orders(self) -> List[dict]:
        return self.orders

def main():
    external_source = ExternalSource([
        {'id': 1, 'customer_name': 'John Doe', 'order_date': '2022-01-01', 'total': 100.0},
        {'id': 2, 'customer_name': 'Jane Doe', 'order_date': '2022-01-02', 'total': 200.0}
    ])

    erp_system = ErpSystem()
    erp_order_sync = ErpOrderSync(erp_system, external_source)

    synced_orders = erp_order_sync.sync_orders()
    for order in synced_orders:
        erp_system.add_order(order)

    print(json.dumps(erp_system.get_orders(), indent=4))

if __name__ == '__main__':
    main()
