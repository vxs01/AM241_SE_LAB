
import pytest
from coffee_shop_order import process_order_batch, check_espresso_machine


def test_invalid_orders():
    with pytest.raises(ValueError):
        process_order_batch("coffee", 0.05)


def test_negative_tax():
    with pytest.raises(ValueError):
        process_order_batch([], -0.01)


def test_all_sizes_and_unknown_size():
    orders = [
        {"paid": True, "size": "small"},
        {"paid": True, "size": "medium"},
        {"paid": True, "size": "large"},
        {"paid": True, "size": "extra-large"},
    ]
    result = process_order_batch(orders, 0)
    assert result == {"total": 13.5, "status": "COMPLETED"}


def test_unpaid_order_and_defaults():
    result = process_order_batch([{"paid": False}, {"paid": True}], 0)
    assert result == {"total": 4.5, "status": "COMPLETED"}


def test_customization_costs():
    orders = [{
        "paid": True,
        "size": "medium",
        "customizations": [
            {"type": "syrup", "cost": 2.0},
            {"type": "oat_milk", "cost": 0.5},
            {"type": "syrup", "cost": -1.0},
        ],
    }]
    result = process_order_batch(orders, 0)
    assert result == {"total": 6.5, "status": "COMPLETED"}


def test_allergy_non_strict_and_strict():
    orders = [
        {
            "paid": True,
            "size": "small",
            "customizations": [{"type": "allergen_alert"}],
        },
        {
            "paid": True,
            "size": "large",
            "strict_allergy": True,
            "customizations": [{"type": "allergen_alert"}],
        },
    ]
    result = process_order_batch(orders, 0)
    assert result == {"total": 3.0, "status": "COMPLETED"}


def test_member_discount_and_tax():
    result = process_order_batch(
        [{"paid": True, "size": "medium", "is_member": True}], 0.1
    )
    assert result == {"total": 4.46, "status": "COMPLETED"}


def test_audit_rejected():
    orders = [
        {"paid": True, "size": "unknown"}
        for _ in range(5)
    ]
    result = process_order_batch(orders, 0.05)
    assert result == {"total": 0.0, "status": "AUDIT_REJECTED"}


def test_no_sale():
    assert process_order_batch([], 0.05) == {
        "total": 0.0, "status": "NO_SALE"
    }


def test_espresso_no_data():
    assert check_espresso_machine([]) == "NO_DATA"


def test_espresso_optimal_and_reset():
    assert check_espresso_machine([[97, 95, 97], [96, 97]]) == "OPTIMAL"


def test_espresso_shutdown():
    assert check_espresso_machine([[97, 98]]) == "SHUTDOWN"
