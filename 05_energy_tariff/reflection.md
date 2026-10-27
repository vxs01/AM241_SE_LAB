# Reflection

**Q1. What did static analysis catch that careful reading alone might have missed?**

Reading `energy_system.py` I noticed the negative reading for M-03 and that
`eval()` on user input looked risky. I did not notice the mutable default
argument `history=[]`, which is shared between calls and only causes trouble
when the function is called more than once. I also overlooked the files opened
without `with` or an encoding, and the `global` statements. Pylint flagged
these immediately (W0102, R1732, W1514, W0603), and Bandit confirmed that
`eval()` is a real security hole (B307). The tools find latent problems that are
easy to skip when the code "looks fine".

**Q2. How do the three tools complement each other?**

Each tool covers a different area. **Bandit** is the security guard: it found
the `eval()` call. **Pylint** is the strict reviewer: it caught design and
quality problems (mutable default, global state, missing docstrings, file
handling) and scored the file 5.96/10 at the start. **Flake8** is the grammar
checker: it enforced PEP 8 (blank lines, line length, the unused `sys` import,
the bare `except`, and the missing newline at the end of the file). Together
they cover security, quality and style. Using only one would have left whole
categories unchecked.

**Q3. How did I decide what to fix and in what order?**

I went by severity and by the tool order in the lab. First the Bandit finding,
because `eval()` on user input is the most dangerous issue (arbitrary code
execution). Then the Flake8 style issues, which were quick, mechanical fixes.
Finally the Pylint quality issues (mutable default, globals, resource handling,
docstrings) to get the score above 9.5. After each commit I reran the relevant
tool to confirm the fix worked and that nothing else broke.

**Q4. How will I use static analysis in future work?**

I will run Pylint, Bandit and Flake8 regularly while I work, ideally in a
pre-commit hook or a CI step, instead of only at the end of a project. A clean
10.00/10 Pylint score, a zero-issue Bandit scan and an empty Flake8 report give
a concrete, repeatable bar for "is this code ready to share?". The tools do not
replace careful testing, though: they never flagged the negative-reading bug,
which I found by running the program and thinking about the logic.
