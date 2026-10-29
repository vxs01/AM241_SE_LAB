import pytest
from coffee_shop_order import process_order_batch, check_espresso_machine


# process_order_batch

def test_branch_invalid_orders_type():
    with pytest.raises(ValueError):
        process_order_batch("not_a_list", 0.05)
    with pytest.raises(ValueError):
        process_order_batch(None, 0.05)


def test_branch_negative_tax_rate():
    with pytest.raises(ValueError):
        process_order_batch([], -0.05)


def test_branch_empty_orders_batch():
    assert process_order_batch([], 0.08) == {"total": 0.0, "status": "NO_SALE"}


def test_branch_unpaid_order_skipped():
    # second order has no "paid" key so it defaults to False
    orders = [{"paid": False, "size": "medium"}, {"size": "medium"}]
    assert process_order_batch(orders, 0.1) == {"total": 0.0, "status": "NO_SALE"}


def test_branch_all_coffee_sizes():
    orders = [
        {"paid": True, "size": "small"},
        {"paid": True, "size": "medium"},
        {"paid": True},  # no size -> medium
        {"paid": True, "size": "large"},
    ]
    # 3 + 4.5 + 4.5 + 6 = 18
    assert process_order_batch(orders, 0) == {"total": 18.0, "status": "COMPLETED"}


def test_branch_unknown_size_rejected():
    orders = [{"paid": True, "size": "extra_large"}, {"paid": True, "size": "small"}]
    assert process_order_batch(orders, 0.1) == {"total": 3.3, "status": "COMPLETED"}


def test_branch_negative_customization_cost():
    orders = [{
        "paid": True,
        "size": "small",
        "customizations": [{"type": "syrup", "cost": -2.0}, {"type": "oat_milk", "cost": 0.5}],
    }]
    assert process_order_batch(orders, 0) == {"total": 3.5, "status": "COMPLETED"}


def test_branch_allergen_alert_strict_and_non_strict():
    # strict -> total becomes 0 and the syrup after it is never added
    strict = {
        "paid": True,
        "size": "large",
        "strict_allergy": True,
        "customizations": [{"type": "allergen_alert"}, {"type": "syrup", "cost": 1.0}],
    }
    # not strict -> only counted as rejected, drink still charged
    not_strict = {
        "paid": True,
        "size": "small",
        "strict_allergy": False,
        "customizations": [{"type": "allergen_alert"}, {"type": "oat_milk", "cost": 0.5}],
    }
    result = process_order_batch([strict, not_strict], 0)
    assert result == {"total": 3.5, "status": "COMPLETED"}


def test_branch_syrup_cap_and_general_mod():
    orders = [{
        "paid": True,
        "size": "small",
        "customizations": [
            {"type": "syrup", "cost": 1.0},
            {"type": "syrup", "cost": 1.5},  # exactly at the cap
            {"type": "syrup", "cost": 3.0},  # gets capped to 1.5
            {"type": "extra_shot", "cost": 0.75},
        ],
    }]
    # 3 + 1 + 1.5 + 1.5 + 0.75 = 7.75
    assert process_order_batch(orders, 0) == {"total": 7.75, "status": "COMPLETED"}


def test_branch_member_discount():
    orders = [
        {"paid": True, "size": "small", "is_member": True},
        {"paid": True, "size": "small", "is_member": False},
    ]
    # 2.7 + 3.0
    assert process_order_batch(orders, 0) == {"total": 5.7, "status": "COMPLETED"}


def test_branch_rejected_items_threshold_boundary():
    # 4 rejections is still ok
    orders = [{"paid": True, "size": "bad_size"} for _ in range(4)]
    orders.append({"paid": True, "size": "small"})
    assert process_order_batch(orders, 0) == {"total": 3.0, "status": "COMPLETED"}

    # 5 rejections -> audit
    orders = [{"paid": True, "size": "bad_size"} for _ in range(5)]
    orders.append({"paid": True, "size": "small"})
    assert process_order_batch(orders, 0) == {"total": 3.0, "status": "AUDIT_REJECTED"}


def test_branch_batch_total_zero_no_sale():
    orders = [{
        "paid": True,
        "size": "small",
        "strict_allergy": True,
        "customizations": [{"type": "allergen_alert"}],
    }]
    assert process_order_batch(orders, 0.05) == {"total": 0.0, "status": "NO_SALE"}


# check_espresso_machine

def test_branch_espresso_empty_and_none():
    assert check_espresso_machine([]) == "NO_DATA"
    assert check_espresso_machine(None) == "NO_DATA"


def test_branch_espresso_cycle_overheat_reset_and_empty_cycle():
    # empty cycle, 96.0 is not overheating, single 98 resets after 95
    cycles = [[], [96.0, 95.5, 96.0], [98.0, 95.0, 97.0]]
    assert check_espresso_machine(cycles) == "OPTIMAL"


def test_branch_espresso_consecutive_overheat_shutdown():
    assert check_espresso_machine([[95.0, 96.5, 97.2]]) == "SHUTDOWN"
