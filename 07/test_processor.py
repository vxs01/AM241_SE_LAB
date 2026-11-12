from hypothesis import given, strategies as st

from processor import (
    calculate_average_shot_cost,
    lookup_drink_code,
    parse_order_modifiers,
)


@given(st.one_of(st.text(), st.none()))
def test_lookup_drink_code_no_crash(value):
    try:
        result = lookup_drink_code(value)
    except Exception as error:
        assert False, f"lookup_drink_code crashed with {error!r}"

    assert result is None or isinstance(result, float)


@given(st.one_of(st.text(), st.none()))
def test_calculate_average_shot_cost_safe(value):
    try:
        result = calculate_average_shot_cost(value)
    except Exception as error:
        assert False, f"calculate_average_shot_cost crashed with {error!r}"

    assert isinstance(result, float)


@given(st.one_of(st.text(), st.none()))
def test_parse_order_modifiers_safe(value):
    try:
        result = parse_order_modifiers(value)
    except Exception as error:
        assert False, f"parse_order_modifiers crashed with {error!r}"

    assert isinstance(result, dict)


def test_valid_inputs_keep_expected_results():
    assert lookup_drink_code("latte") == 4.50
    assert lookup_drink_code("moc") == 5.00
    assert calculate_average_shot_cost("1.0, 1.5, 2.0") == 1.5
    assert parse_order_modifiers("milk:oat;syrup:vanilla") == {
        "milk": "oat",
        "syrup": "vanilla",
    }


def test_malformed_inputs_are_safe():
    assert lookup_drink_code("unknown") is None
    assert calculate_average_shot_cost("") == 0.0
    assert calculate_average_shot_cost("1.0,not-a-number") == 0.0
    assert parse_order_modifiers("milk:oat;broken;syrup:vanilla") == {
        "milk": "oat",
        "syrup": "vanilla",
    }
