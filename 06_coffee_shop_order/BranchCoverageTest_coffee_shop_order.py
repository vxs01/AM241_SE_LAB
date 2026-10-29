import pytest
from coffee_shop_order import process_order_batch, check_espresso_machine


# ---------------------------------------------------------
# Branch Coverage Tests for process_order_batch
# ---------------------------------------------------------

def test_branch_invalid_orders_type():
    """Branch: not isinstance(orders, list) is True."""
    with pytest.raises(ValueError, match="Invalid orders list or tax rate"):
        process_order_batch("not_a_list", 0.05)
    with pytest.raises(ValueError, match="Invalid orders list or tax rate"):
        process_order_batch(None, 0.05)


def test_branch_negative_tax_rate():
    """Branch: tax_rate < 0 is True."""
    with pytest.raises(ValueError, match="Invalid orders list or tax rate"):
        process_order_batch([], -0.05)


def test_branch_empty_orders_batch():
    """Branch: orders list is empty -> loop does not execute, batch_total == 0.0 -> NO_SALE."""
    result = process_order_batch([], 0.08)
    assert result == {"total": 0.0, "status": "NO_SALE"}


def test_branch_unpaid_order_skipped():
    """Branch: not order.get('paid', False) is True -> continue."""
    orders = [
        {"paid": False, "size": "medium"},
        {"size": "medium"},  # missing paid key defaults to False
    ]
    result = process_order_batch(orders, 0.10)
    assert result == {"total": 0.0, "status": "NO_SALE"}


def test_branch_all_coffee_sizes():
    """Branches: size == 'small', 'medium', 'large' and default size."""
    orders = [
        {"paid": True, "size": "small"},               # 3.0
        {"paid": True, "size": "medium"},              # 4.5
        {"paid": True},                                # default medium 4.5
        {"paid": True, "size": "large"},               # 6.0
    ]
    # sum = 3.0 + 4.5 + 4.5 + 6.0 = 18.0
    # tax = 0.0 -> total 18.0
    result = process_order_batch(orders, 0.0)
    assert result == {"total": 18.0, "status": "COMPLETED"}


def test_branch_unknown_size_rejected():
    """Branch: unknown size falls into else -> rejected_items += 1, continue."""
    orders = [
        {"paid": True, "size": "extra_large"},  # rejected
        {"paid": True, "size": "small"},        # 3.0
    ]
    result = process_order_batch(orders, 0.10)
    # 3.0 * 1.10 = 3.3
    assert result == {"total": 3.3, "status": "COMPLETED"}


def test_branch_negative_customization_cost():
    """Branch: cost < 0 -> rejected_items += 1, continue."""
    orders = [
        {
            "paid": True,
            "size": "small",
            "customizations": [
                {"type": "syrup", "cost": -2.0},  # negative cost rejected
                {"type": "oat_milk", "cost": 0.50},
            ],
        }
    ]
    # base 3.0 + 0.5 = 3.5
    result = process_order_batch(orders, 0.0)
    assert result == {"total": 3.5, "status": "COMPLETED"}


def test_branch_allergen_alert_strict_and_non_strict():
    """Branches: mod_type == 'allergen_alert' with strict_allergy True and False."""
    # Strict allergy: item_total reset to 0.0 and break
    strict_order = {
        "paid": True,
        "size": "large",
        "strict_allergy": True,
        "customizations": [
            {"type": "allergen_alert"},
            {"type": "syrup", "cost": 1.0},  # never reached because of break
        ],
    }
    # Non-strict allergy: rejected_items incremented, continues
    non_strict_order = {
        "paid": True,
        "size": "small",
        "strict_allergy": False,
        "customizations": [
            {"type": "allergen_alert"},
            {"type": "oat_milk", "cost": 0.50},
        ],
    }
    orders = [strict_order, non_strict_order]
    # strict_order total: 0.0
    # non_strict_order total: 3.0 + 0.50 = 3.5
    result = process_order_batch(orders, 0.0)
    assert result == {"total": 3.5, "status": "COMPLETED"}


def test_branch_syrup_cap_and_general_mod():
    """Branches: syrup cost <= 1.5, syrup cost > 1.5 (capped), and non-syrup mod."""
    orders = [
        {
            "paid": True,
            "size": "small",  # 3.0
            "customizations": [
                {"type": "syrup", "cost": 1.0},   # cost <= 1.5 -> 1.0
                {"type": "syrup", "cost": 1.5},   # boundary cost <= 1.5 -> 1.5
                {"type": "syrup", "cost": 3.0},   # cost > 1.5 -> capped at 1.5
                {"type": "extra_shot", "cost": 0.75},  # general mod -> 0.75
            ],
        }
    ]
    # 3.0 + 1.0 + 1.5 + 1.5 + 0.75 = 7.75
    result = process_order_batch(orders, 0.0)
    assert result == {"total": 7.75, "status": "COMPLETED"}


def test_branch_member_discount():
    """Branches: order.get('is_member', False) True and False."""
    orders = [
        {"paid": True, "size": "small", "is_member": True},   # 3.0 * 0.9 = 2.7
        {"paid": True, "size": "small", "is_member": False},  # 3.0
    ]
    # sum = 2.7 + 3.0 = 5.7
    result = process_order_batch(orders, 0.0)
    assert result == {"total": 5.7, "status": "COMPLETED"}


def test_branch_rejected_items_threshold_boundary():
    """Branch: rejected_items <= 4 vs rejected_items > 4 (AUDIT_REJECTED)."""
    # Exactly 4 rejections: should NOT trigger AUDIT_REJECTED
    four_rejections = [
        {"paid": True, "size": "bad_size"} for _ in range(4)
    ]
    four_rejections.append({"paid": True, "size": "small"})  # 3.0
    res4 = process_order_batch(four_rejections, 0.0)
    assert res4["status"] == "COMPLETED"
    assert res4["total"] == 3.0

    # Exactly 5 rejections: triggers AUDIT_REJECTED
    five_rejections = [
        {"paid": True, "size": "bad_size"} for _ in range(5)
    ]
    five_rejections.append({"paid": True, "size": "small"})  # 3.0
    res5 = process_order_batch(five_rejections, 0.0)
    assert res5["status"] == "AUDIT_REJECTED"
    assert res5["total"] == 3.0


def test_branch_batch_total_zero_no_sale():
    """Branch: batch_total == 0.0 -> NO_SALE when items processed but total remains 0."""
    orders = [
        {
            "paid": True,
            "size": "small",
            "strict_allergy": True,
            "customizations": [{"type": "allergen_alert"}],
        }
    ]
    # strict allergy zeroes item_total, rejected_items = 1 <= 4, batch_total == 0.0
    result = process_order_batch(orders, 0.05)
    assert result == {"total": 0.0, "status": "NO_SALE"}


# ---------------------------------------------------------
# Branch Coverage Tests for check_espresso_machine
# ---------------------------------------------------------

def test_branch_espresso_empty_and_none():
    """Branch: not temperature_cycles is True -> NO_DATA."""
    assert check_espresso_machine([]) == "NO_DATA"
    assert check_espresso_machine(None) == "NO_DATA"


def test_branch_espresso_cycle_overheat_reset_and_empty_cycle():
    """Branches: cycle empty, temp > 96.0 single overheat then reset (temp <= 96.0)."""
    # Includes empty subcycle and safe temperature sequence
    cycles = [
        [],                   # empty inner cycle
        [96.0, 95.5, 96.0],   # boundary temp == 96.0 is safe (not > 96.0)
        [98.0, 95.0, 97.0],   # single overheat resets when 95.0 encountered
    ]
    assert check_espresso_machine(cycles) == "OPTIMAL"


def test_branch_espresso_consecutive_overheat_shutdown():
    """Branch: temp > 96.0 twice consecutively (overheat_streak >= 2) -> SHUTDOWN."""
    cycles = [
        [95.0, 96.5, 97.2]  # streak reaches 2
    ]
    assert check_espresso_machine(cycles) == "SHUTDOWN"
