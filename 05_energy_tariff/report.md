# Lab 5: Static Code Analysis – Report

**Name / SRN:** PES1UG24AM241
**File analysed:** `energy_system.py` (Energy Consumption & Tariff Calculator)
**Tools:** Pylint 4.1.3, Bandit 1.9.4, Flake8 7.4.1

## 1. Summary

`energy_system.py` was analysed with Pylint, Bandit and Flake8 before and after fixing. The fixes were made in three commits, one per tool. After the changes, Bandit reports no issues, Flake8 reports no issues, and Pylint rates the code 10.00/10.

## 2. Results (before vs after)

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.96 / 10 | 10.00 / 10 |
| Bandit | 1 issue (B307, Medium severity, High confidence) | 0 issues |
| Flake8 | 13 issues (E302 x7, E501 x2, F401, E722, E305, W292) | 0 issues |

Reports: `before/` and `after/` folders (`pylint_report.txt`, `bandit_report.txt`, `flake8_report.txt`).

## 3. Commits

1. **Bandit fix:** removed `eval()` on user input (B307 / Pylint W0123). The extra units are now parsed with `float()` inside a `try/except ValueError`.
2. **Flake8 fix:** removed the unused `import sys` (F401), added the 2 blank lines between functions (E302/E305), wrapped the lines over 79 characters (E501), replaced the bare `except:` with `except Exception:` (E722) and added the missing newline at the end of the file (W292).
3. **Pylint fix:**
   - added docstrings
   - replaced the mutable default argument `history=[]` with `None`
   - removed the `global` statements (module state is changed in place, and `raise_rates` returns a new list)
   - opened files with `with open(..., encoding="utf-8")`
   - used f-strings and a dict/list comprehension in `flag_spikes`
   - removed the `elif` after `return` by simplifying the tier calculation
   - replaced the bare except with specific exceptions
   - added the `if __name__ == "__main__":` guard

## 4. Bugs not flagged by the tools

- **Negative readings:** a reading of `-50` for M-03 was accepted and gave a negative bill. Negative units now raise a `ValueError`, which `main` handles by skipping the reading.
- **Shared history list:** the mutable default `history=[]` meant the history was shared between unrelated calls. A new list is now created per call unless one is passed in.
- **Unknown meter:** `compute_bill` raised a `KeyError` for an unknown meter id. It now uses `METERS.get(meter_id, 0)`.

## 5. Verification

After each commit the relevant tool was rerun and the new report saved in `after/`. The program was run again after the final commit and behaves as expected: M-03's negative reading is skipped, M-01's bill is 495.00 and M-02 is flagged as a spike.

## 6. Conclusion

Static analysis found the insecure `eval`, style problems and several code-quality issues quickly, and it also pointed to the `global` state and file handling that needed cleaning up. It did not find the logic bugs (negative readings), so the tools complement manual review and running the program rather than replace them.
