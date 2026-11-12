---
name: codebase-design
description: Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when another skill needs the deep-module vocabulary.
disable-model-invocation: true
---
<!-- vendored: mattpocock/skills@c0d6901 skills/engineering/codebase-design (MIT). -->

# Codebase design

Design deep modules: a lot of behavior behind a small interface, placed at a clean seam
and tested through that interface.

## Terms

Use these terms exactly, and do not swap in the words each entry rules out.

- **Module**: anything with an interface and an implementation, at any scale: a function,
  a class, a package. Do not say component, service, or unit.
- **Interface**: everything a caller must know to use the module correctly. That includes
  types, invariants, ordering, error modes, required configuration, and performance. Do
  not say API or signature, which cover only the types.
- **Implementation**: the code inside the module.
- **Depth**: how much behavior a caller gets for each thing they must learn about the
  interface. A deep module puts a lot of behavior behind a small interface. A shallow
  module's interface is nearly as complex as its implementation.
- **Seam**: the place where a module's interface sits, and where behavior can change
  without editing callers. Do not say boundary.
- **Adapter**: a concrete thing that satisfies an interface at a seam.
- **Leverage**: what callers gain from depth. One implementation serves many call sites
  and tests.
- **Locality**: what maintainers gain from depth. Changes, bugs, knowledge, and tests
  concentrate in one place.

## Principles

- When designing an interface, try to reduce the methods, simplify the parameters, and
  hide more complexity inside.
- Depth is a property of the interface. A deep module can be built from small swappable
  parts, as long as those parts and their internal seams stay private.
- The deletion test: imagine deleting the module. If the complexity disappears, the
  module only passed calls through. If it reappears in every caller, keep the module.
- Callers and tests cross the same interface. Tests assert on outcomes seen through it
  and never on internals. A test that needs to reach past the interface means the module
  has the wrong shape.
- One adapter makes a seam hypothetical, and two make it real. Add a seam only when
  something varies across it.
- Accept dependencies as arguments instead of creating them inside.
- Return results instead of producing side effects.

To deepen a group of modules given its dependencies, read [DEEPENING.md](DEEPENING.md).
To compare alternative interfaces, read [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md).
