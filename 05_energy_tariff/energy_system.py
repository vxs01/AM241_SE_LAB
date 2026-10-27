"""Utility meter tracker with a three-tier electricity tariff."""
import json
from datetime import datetime

METERS = {}
BASE_RATES = [3.5, 5.0, 7.5]
SPIKE_LIMIT = 500
TIER_1_LIMIT = 100
TIER_2_LIMIT = 300


def record_reading(meter_id, units, history=None):
    """Add units to a meter and log the reading in history."""
    if units < 0:
        raise ValueError("units cannot be negative")
    if history is None:
        history = []
    history.append((meter_id, units, str(datetime.now())))
    METERS[meter_id] = METERS.get(meter_id, 0) + units
    return history


def compute_bill(meter_id, tier_rates):
    """Return the tiered bill for a meter (0 if the meter is unknown)."""
    units = METERS.get(meter_id, 0)
    tier_1 = min(units, TIER_1_LIMIT)
    tier_2 = min(max(units - TIER_1_LIMIT, 0), TIER_2_LIMIT - TIER_1_LIMIT)
    tier_3 = max(units - TIER_2_LIMIT, 0)
    return (tier_1 * tier_rates[0]
            + tier_2 * tier_rates[1]
            + tier_3 * tier_rates[2])


def raise_rates(rates, percent):
    """Return a new list of rates increased by the given percentage."""
    return [rate * (1 + percent / 100) for rate in rates]


def flag_spikes():
    """Return the ids of meters whose usage exceeds SPIKE_LIMIT."""
    return [meter for meter, units in METERS.items() if units > SPIKE_LIMIT]


def load_meter_data(file="meters.json"):
    """Load meter data from a JSON file; start empty if unreadable."""
    try:
        with open(file, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError):
        data = {}
    METERS.clear()
    METERS.update(data)


def save_meter_data(file="meters.json"):
    """Save meter data to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(METERS, handle)


def main():
    """Run the demo."""
    history = []
    for meter_id, units in (("M-01", 120), ("M-02", 640), ("M-03", -50)):
        try:
            record_reading(meter_id, units, history)
        except ValueError as err:
            print(f"Skipped {meter_id}: {err}")
    print("Readings stored so far:", len(history))

    rates = raise_rates(BASE_RATES, 10)
    print(f"Bill M-01: {compute_bill('M-01', rates):.2f}")
    print(f"Bill M-03: {compute_bill('M-03', rates):.2f}")
    print("Spikes:", flag_spikes())

    raw = input("Extra units for M-01 (number, Enter for 0): ") or "0"
    try:
        record_reading("M-01", float(raw), history)
    except ValueError:
        print("Invalid or negative number, ignoring.")

    save_meter_data()
    load_meter_data()
    print(f"Bill M-01 after reload: {compute_bill('M-01', rates):.2f}")


if __name__ == "__main__":
    main()
    