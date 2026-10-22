import pytest

from service_body_test import Order


@pytest.fixture
def order():
    return Order("A-1", [
        {"price": 10.0, "quantity": 5},
        {"price": 3.0, "quantity": 2},
        {"price": 7.5, "quantity": 1},
    ])


@pytest.mark.parametrize("items, expected", [
    ([], 0.0),
    ([{"price": 10.0, "quantity": 5}], 50.0),
    ([{"price": 10.0, "quantity": 5}, {"price": 3.0, "quantity": 2}], 56.0),
    ([{"price": 2.5, "quantity": 2}, {"price": 0.1, "quantity": 3}], 5.3),
    ([{"price": 10.0, "quantity": 0}], 0.0),
    ([{"price": 0.0, "quantity": 5}], 0.0),
])
def test_total_for_different_items(items, expected):
    order = Order("A-1", items)
    assert order.total() == pytest.approx(expected)

def test_total_for_multiple_items(order):
    assert order.total() == pytest.approx(63.5)

def test_most_expensive_returns_highest_price(order):
    assert order.most_expensive() is order.items[0]

def test_most_expensive_uses_unit_price_not_quantity():
    items = [
        {"price": 5.0, "quantity": 100},
        {"price": 20.0, "quantity": 1},
        {"price": 10.0, "quantity": 2},
    ]
    assert Order("A-1", items).most_expensive() is items[1]

def test_most_expensive_with_one_item():
    item = {"price": 4.0, "quantity": 1}
    assert Order("A-1", [item]).most_expensive() is item

def test_most_expensive_with_equal_prices_returns_first():
    items = [
        {"price": 10.0, "quantity": 1},
        {"price": 10.0, "quantity": 3},
    ]
    assert Order("A-1", items).most_expensive() is items[0]

def test_most_expensive_with_empty_items_raises_value_error():
    with pytest.raises(ValueError):
        Order("A-1", []).most_expensive()

@pytest.mark.parametrize("percent, expected_prices", [
    (0, [10.0, 3.0, 7.5]),
    (10, [9.0, 2.7, 6.75]),
    (50, [5.0, 1.5, 3.75]),
    (100, [0.0, 0.0, 0.0]),
])
def test_apply_discount_changes_every_item(order, percent, expected_prices):
    order.apply_discount(percent)
    prices = [item["price"] for item in order.items]
    assert prices == pytest.approx(expected_prices)

@pytest.mark.parametrize("percent", [-5, -0.01, 100.01, 150])
def test_apply_discount_rejects_invalid_percent_without_changes(order, percent):
    old_prices = [item["price"] for item in order.items]

    with pytest.raises(ValueError, match="Invalid discount"):
        order.apply_discount(percent)

    assert [item["price"] for item in order.items] == pytest.approx(old_prices)

def test_apply_discount_updates_total(order):
    order.apply_discount(10)
    assert order.total() == pytest.approx(57.15)

def test_apply_discount_with_empty_items():
    order = Order("A-1", [])
    order.apply_discount(50)
    assert order.items == []

@pytest.mark.parametrize("items, expected", [
    ([], "<Order ORD-1: 0 items>"),
    ([{"price": 10.0, "quantity": 1}], "<Order ORD-1: 1 items>"),
    ([{"price": 10.0, "quantity": 1}, {"price": 5.0, "quantity": 2}],
     "<Order ORD-1: 2 items>"),
])
def test_repr_shows_order_id_and_item_count(items, expected):
    order = Order("ORD-1", items)
    assert repr(order) == expected