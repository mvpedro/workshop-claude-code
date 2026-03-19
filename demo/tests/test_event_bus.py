from src.api.events.bus import clear, publish, subscribe
from src.api.events.types import OrderCreated


def test_publish_calls_subscribers():
    received = []
    subscribe(OrderCreated, lambda e: received.append(e))
    event = OrderCreated(order_id="1", customer_id="c1", total=1000, item_count=2)
    publish(event)
    assert len(received) == 1
    assert received[0].order_id == "1"
    clear()


def test_publish_no_subscribers():
    clear()
    event = OrderCreated(order_id="1", customer_id="c1", total=1000, item_count=2)
    publish(event)


def test_handler_error_does_not_break_others():
    received = []
    def bad_handler(e):
        raise ValueError("boom")
    subscribe(OrderCreated, bad_handler)
    subscribe(OrderCreated, lambda e: received.append(e))
    event = OrderCreated(order_id="1", customer_id="c1", total=1000, item_count=2)
    publish(event)
    assert len(received) == 1
    clear()
