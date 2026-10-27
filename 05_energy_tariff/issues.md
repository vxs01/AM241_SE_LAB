# Issues – energy_system.py (PES1UG24AM241)

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| `eval()` on user input | Security (Bandit B307) | 63 | `eval(adjustment)` executes arbitrary code typed by the user | Parse with `float()` inside try/except ValueError |
| Bare `except:` | Bug / Style (Pylint W0702, Flake8 E722) | 41 | Swallows every error, including KeyboardInterrupt | Catch `(OSError, json.JSONDecodeError)` only |
| Mutable default argument | Bug (Pylint W0102) | 11 | `history=[]` is shared across calls, so history grows across unrelated calls | Default to `None`, create a new list inside |
| Negative readings accepted | Logic bug (not flagged by tools) | 57 | `M-03 = -50` gives a negative bill | Raise `ValueError` if `units < 0`, handle it in `main` |
| Files opened without `with` / no encoding | Pylint R1732, W1514 | 40, 46 | File handle may leak, encoding is platform dependent | Use `with open(..., encoding="utf-8")` |
| `global` statements | Design (Pylint W0603) | 25, 41 | Mutating module-level state through `global` | Mutate `METERS` in place; `raise_rates` returns a new list |
| Missing docstrings | Style (Pylint C0114, C0116) | all | No module or function docstrings | Add one-line docstrings |
| Formatting | Style (Flake8 E302, E305, E501) | various | Blank lines, line length over 79 | Reformat to PEP 8 |
| `main()` runs on import | Design | 68 | Code executes when the module is imported | Add `if __name__ == "__main__":` guard |
| Unknown meter in `compute_bill` | Bug | 17 | `meters[meter_id]` raises KeyError | Use `METERS.get(meter_id, 0)` |