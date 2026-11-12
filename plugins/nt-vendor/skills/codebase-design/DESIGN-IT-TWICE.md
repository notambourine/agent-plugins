# Design it twice

Use this when the user wants alternative interfaces for a module they chose to deepen.
The first design is rarely the best one.

1. Show the user the problem: the constraints any interface must satisfy, the
   dependencies and their categories from [DEEPENING.md](DEEPENING.md), and a rough code
   sketch that illustrates the constraints without proposing anything. Then go straight
   to step 2 while they read.
2. Spawn at least three agents in parallel. Give each a technical brief with the file
   paths, the coupling, the dependency category, and what sits behind the seam, written
   in the terms of [SKILL.md](SKILL.md) and the project's `CONTEXT.md`. Give each a
   different constraint so the designs differ:
   - the smallest interface, with one to three entry points;
   - the most flexible interface, built for many use cases and for extension;
   - the interface that makes the most common call trivial;
   - ports and adapters, when dependencies cross the seam.
3. Each agent returns the full interface with its invariants, ordering, and error modes,
   a usage example, what the implementation hides, the dependency strategy and adapters,
   and where leverage is high and where it is thin.
4. Present the designs one at a time, then compare them on depth, locality, and seam
   placement.
5. Recommend one design, or a specific hybrid, and say why.
