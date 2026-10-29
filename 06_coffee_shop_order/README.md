# Lab 6: Code and Branch Coverage – Report

**Name / SRN:** Sakaray Vishal / PES1UG24AM241
**Repo assigned:** L6_L7_03_coffee_shop_order
**File tested:** `coffee_shop_order.py`
**Tools:** pytest 9.1.1, coverage 7.17.0

## 1. Summary

`coffee_shop_order.py` has two functions, `process_order_batch` (order totals, customizations, allergy rules, member discount, tax) and `check_espresso_machine` (temperature cycles). The starter test only covered one simple order, so I wrote two test files, one for code coverage and one for branch coverage. Both reach 100% on `coffee_shop_order.py`.

## 2. Results

| Test file | Tests | Line coverage | Branch coverage |
|-----------|-------|---------------|-----------------|
| `test_coffee_shop.py` (starter) | 1 | 48% | 43% |
| `CodeCoverageTest_coffee_shop_order.py` | 12 | 100% (54/54) | - |
| `BranchCoverageTest_coffee_shop_order.py` | 15 | 100% (54/54) | 100% (38/38) |

Screenshots: `screenshots/code_coverage.png` and `screenshots/branch_coverage.png`.

## 3. Commands

```
pip install coverage pytest

coverage run -m pytest -v CodeCoverageTest_coffee_shop_order.py
coverage report -m

coverage run --branch -m pytest -v BranchCoverageTest_coffee_shop_order.py
coverage report -m
```

## 4. Code coverage tests

The missing lines from the starter run were the ValueError, the small/large/unknown sizes, unpaid orders, negative costs, syrup, allergen alerts, member discount, AUDIT_REJECTED / NO_SALE and the whole espresso function. I added one test for each of these so every line runs at least once.

## 5. Branch coverage tests

100% line coverage still left some conditions only tested one way, so for the branch file I made sure each `if` and loop goes both ways, and checked the boundary values:

- missing `paid` key and missing `size` key (defaults)
- syrup exactly 1.5 (not capped) and 3.0 (capped)
- strict allergy (total becomes 0, later customizations skipped) vs not strict
- exactly 4 rejections (COMPLETED) vs 5 (AUDIT_REJECTED)
- NO_SALE when orders were processed but the total is still 0
- temperature exactly 96.0 (not overheating), an empty cycle, and an overheat that resets
- `None` and `[]` for the espresso machine

## 6. Conclusion

Line coverage only shows that a line ran, not that both outcomes of a condition were tested. The code coverage tests already hit every line, but things like the 4 vs 5 rejections limit or the syrup at exactly 1.5 were only tested properly once I looked at branch coverage. Branch coverage is the more useful number for finding edge cases.
