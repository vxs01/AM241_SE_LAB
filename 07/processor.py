"""Helpers for looking up and validating coffee-shop order data."""


MENU_PRICES = {
    "LAT": 4.50,
    "CAP": 4.00,
    "ESP": 3.00,
    "AME": 3.50,
    "MOC": 5.00,
}


def lookup_drink_code(code_string):
    """Return a drink price, or None when the code is invalid."""
    if not isinstance(code_string, str):
        return None

    return MENU_PRICES.get(code_string.upper()[:3])


def calculate_average_shot_cost(pricing_csv):
    """Return the average of a comma-separated price list, or 0.0 if invalid."""
    if not isinstance(pricing_csv, str) or not pricing_csv.strip():
        return 0.0

    try:
        prices = [float(price.strip()) for price in pricing_csv.split(",")]
    except (TypeError, ValueError):
        return 0.0

    if not prices:
        return 0.0

    return sum(prices) / len(prices)


def parse_order_modifiers(order_spec):
    """Parse ``key:value`` modifiers, ignoring malformed entries."""
    if not isinstance(order_spec, str) or not order_spec:
        return {}

    modifier_dict = {}
    for item in order_spec.split(";"):
        if ":" not in item:
            continue

        key, value = item.split(":", 1)
        key = key.strip()
        if key:
            modifier_dict[key] = value.strip()

    return modifier_dict


def main():
    print("==== Running lookup_drink_code ====")
    drink_input = input("Enter drink code prefix (e.g. LAT, CAP, ESP): ")
    price = lookup_drink_code(drink_input)
    print("Base Price: $", price)

    print("\n==== Running calculate_average_shot_cost ====")
    shots_input = input("Enter CSV of shot prices (e.g. 1.0, 1.5, 2.0): ")
    avg_price = calculate_average_shot_cost(shots_input)
    print("Average Shot Price: $", avg_price)

    print("\n==== Running parse_order_modifiers ====")
    spec_input = input("Enter modifiers (e.g. milk:oat;syrup:vanilla): ")
    mods = parse_order_modifiers(spec_input)
    print("Parsed Modifiers:", mods)


if __name__ == "__main__":
    main()
