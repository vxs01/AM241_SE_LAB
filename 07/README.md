# Lab 7: Fuzz Testing with Hypothesis

This lab hardens the coffee-shop input helpers against malformed values while
preserving their behavior for valid inputs.

## Bugs found and fixed

- `lookup_drink_code` crashed for `None` and unknown codes, and the mocha key
  did not match the normalized lookup key.
- `calculate_average_shot_cost` crashed for `None`, empty CSV input, and
  non-numeric values; it could also divide by zero.
- `parse_order_modifiers` crashed for `None`, empty input, entries without a
  colon, and values containing additional colons.

Invalid inputs now produce safe results: `None`, `0.0`, or `{}` as appropriate.

## Commands

Install the test dependencies:

```text
python -m pip install -r requirements.txt
```

Run the application:

```text
python processor.py
```

Run the fuzz tests:

```text
python -m pytest -q test_processor.py
```

The three property-based tests generate arbitrary Unicode strings and
`None`, while the focused tests verify valid behavior and minimized edge
cases identified by fuzzing.
