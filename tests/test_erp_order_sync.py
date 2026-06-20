from erp_order_sync import ErpOrderSync, ErpSystem, ExternalSource, Order

def test_sync_orders():
    external_source = ExternalSource([
        {'id': 1, 'customer_name': 'John Doe', 'order_date': '2022-01-01', 'total': 100.0},
        {'id': 2, 'customer_name': 'Jane Doe', 'order_date': '2022-01-02', 'total': 200.0}
    ])

    erp_system = ErpSystem()
    erp_order_sync = ErpOrderSync(erp_system, external_source)

    synced_orders = erp_order_sync.sync_orders()
    assert len(synced_orders) == 2

    erp_system.add_order(synced_orders[0])
    synced_orders = erp_order_sync.sync_orders()
    assert len(synced_orders) == 1

def test_sync_orders_empty_external_source():
    external_source = ExternalSource([])
    erp_system = ErpSystem()
    erp_order_sync = ErpOrderSync(erp_system, external_source)

    synced_orders = erp_order_sync.sync_orders()
    assert len(synced_orders) == 0

def test_sync_orders_empty_erp_system():
    external_source = ExternalSource([
        {'id': 1, 'customer_name': 'John Doe', 'order_date': '2022-01-01', 'total': 100.0},
        {'id': 2, 'customer_name': 'Jane Doe', 'order_date': '2022-01-02', 'total': 200.0}
    ])

    erp_system = ErpSystem()
    erp_order_sync = ErpOrderSync(erp_system, external_source)

    synced_orders = erp_order_sync.sync_orders()
    assert len(synced_orders) == 2

def test_order_mapping():
    order = Order(1, 'John Doe', '2022-01-01', 100.0)
    assert order.id == 1
    assert order.customer_name == 'John Doe'
    assert order.order_date == '2022-01-01'
    assert order.total == 100.0
