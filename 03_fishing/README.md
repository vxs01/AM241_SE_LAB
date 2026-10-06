# Fishing Lab

This project is a single-topic Fishing-lite game using **Pygame**. It
introduces students to timed casting mechanics, overlap-based catch
detection, and stateful entity variety, using a small, readable
object-oriented codebase.

---

## What's Provided

A working Fishing game with:

- A boat and hook - the hook casts downward and retracts back to the
  surface on its own, in a continuous loop
- Fish that swim back and forth across the pond at fixed depths and
  wrap around the screen edges
- A hook that snags a fish on contact - the fish rides up attached to
  the hook and is only actually caught (scored, removed from the pond)
  once the hook fully returns to the surface
- A running score display

It has **one deliberate bug** and **three features** left for you to
build. You are expected to **analyze**, **interact with an AI
assistant**, and **complete/fix** the game to make it fully functional
and more interesting.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**

---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the game:

```bash
python main.py
```

**Controls:** Currently none - the hook casts and retracts on its own
in a loop. That changes once you complete Task 3.

---

## Tasks to Complete

Each task must be completed using an iterative process involving LLM
suggestions and your critical code review.

### Task 1: Fix the catch-detection bug

> A fish is supposed to be caught only when the hook actually overlaps
> it. In the current build, `check_catch` (in `game/catch.py`) only
> compares the hook's depth to the fish's depth, within a fixed
> 10-pixel tolerance - it never compares horizontal position at all.
> That means a fish can register as caught while it's still far off to
> one side of the screen, just because the hook happens to be passing
> through its depth. Fix the check so it's based on the hook and fish
> actually overlapping, not just being at a similar depth.

### Task 2: Implement multiple fish types

> Introduce at least two fish types that differ in movement speed and
> point value (for example, a slow low-value fish and a fast
> high-value one). Give each type its own look (color and/or size) so
> they're visually distinguishable, and make sure the correct point
> value is awarded when each type is caught.

### Task 3: Implement player-controlled casting

> Change the hook so the player decides when it casts, instead of it
> looping automatically. Pressing a key should start a cast if the
> hook is currently idle; it should then travel down and return on its
> own (already handled) once it reaches maximum depth or catches a
> fish. A new cast should not be able to interrupt one that's already
> in progress.

### Task 4: Implement a 30-second round timer

> Add a 30-second countdown for the round. Display the remaining time
> on screen. Once it reaches zero, no further catches should be
> possible, the round should end, and the final score should be shown
> clearly. Provide a way to start a new round with the score and timer
> both reset.

---

## Expected Behavior

- A fish is only caught when the hook genuinely overlaps it - not just
  when it's at a similar depth anywhere on screen.
- A caught fish visibly rides up on the hook as it retracts; the score
  only increases once it's fully back at the surface.
- Different fish types are visually distinguishable and award the
  correct point value.
- Once casting is player-controlled, pressing the cast key while the
  hook is already out should do nothing - it should not interrupt or
  restart the current cast.
- The round lasts exactly 30 seconds. Once time runs out, no further
  catches should be possible, and the final score should be shown
  clearly.

---

## Folder Structure

```
fishing/
├── main.py
├── requirements.txt
├── game/
│   ├── game_engine.py
│   ├── hook.py
│   ├── fish.py
│   ├── catch.py
│   └── renderer.py
└── README.md
```

---

## Submission Checklist

Submission is only the following three things:

- [ ] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [ ] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [ ] The Chat/LLM used page link, with the complete chat history
