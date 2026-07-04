---
name: backpass
description: Two-pass coding rhythm that fights agentic overbuild. Forward pass solves the problem; backward pass strips the result to its essential form — removing dead code, collapsing over-abstraction, simplifying control flow. Reports what was simplified. Use when user types /backpass or wants a forward/backward rhythm to produce cleaner, more legible code.
---

# Backpass: Two-Pass Coding

Activate by announcing: **"Backpass mode on."** Then apply the two-pass rhythm for this task.

**Why this exists**: Agentic coding naturally overbuilds on the first pass — scaffolding that hardens in place, abstractions that never earn their weight, solutions designed for problems that didn't materialize. The backward pass is the deliberate step to undo that drift before it compounds into tech debt.

**The tradeoff**: Backpass mode moves slower than a single-pass implementation. Use it when code quality and legibility matter more than raw speed.

---

## The Rhythm

```
FORWARD: Write code that solves the problem.
BACKWARD: Strip it to its essential form.
```

These are distinct cognitive modes. **Do not mix them.** Finish the forward pass before beginning the backward pass.

---

## Forward Pass

Write code that works. Rules:

- Solve the stated problem, nothing more
- Don't architect for hypothetical future requirements
- Don't block on perfect naming or structure — that's backward-pass work
- Commit to a working solution first; elegance comes second

When the forward pass is complete and tests pass, announce:

> **"Forward pass complete. Starting backward pass."**

---

## Backward Pass

Go through every file touched during the forward pass. For each one, apply the checklist below. After the backward pass, run tests — they must still pass.

### Elimination — does removing this break anything?

- [ ] Dead code: written but never called
- [ ] Scaffolding that stayed: temporary structure that hardened in place
- [ ] One-call helpers: functions extracted once, never reused — inline them
- [ ] Speculative parameters: args that are always the same value at every call site
- [ ] Unused imports, variables, type aliases, constants

### Simplification — can the same behavior be expressed more simply?

- [ ] Verbose control flow → early returns or guard clauses
- [ ] Nested conditionals → flattened or inverted logic
- [ ] Hand-rolled logic → stdlib or an existing dependency
- [ ] Multi-step transforms → a single pipeline, map, or comprehension
- [ ] Intermediate variables that exist only to be immediately passed elsewhere

### Interface — is the public surface right-sized?

- [ ] Public methods or functions that should be private
- [ ] Parameters that always travel together (candidates for a struct/dataclass)
- [ ] Return values carrying more than callers use

### Naming — does every name earn its length?

- [ ] Long names encoding what the type system already says
- [ ] Abbreviated names requiring the reader to decode
- [ ] Comments explaining what the code already shows clearly

---

## Rules

- **Equivalence-preserving**: the backward pass changes form, not behavior.
- **Tests are the gate**: run tests before starting, run them again after. If they break during the backward pass, stop and fix before continuing.
- **No new features**: if you spot missing behavior during the backward pass, note it — don't implement it. That's a new forward pass.
- **Prefer obvious simplicity over clever simplicity**: if a simplification requires careful reasoning to verify it's equivalent, leave it. The goal is code a reader can skim, not code that impresses on close inspection.

---

## Reporting

After the backward pass, give a brief summary:

```
Backward pass complete.
Simplified:
  - [file:line] inlined one-call helper `_build_payload` into caller
  - [file:line] replaced manual loop with list comprehension
  - [file:line] removed unused `timeout` parameter (always None)
  - [file:line] collapsed 4-branch if/elif into guard clause + early return
No behavior changes. Tests pass.
```

If nothing was simplified, say so explicitly: **"Backward pass complete. No simplifications found — forward pass was already minimal."**

---

## Stopping Criteria

The backward pass is done when:

1. Every remaining line is load-bearing
2. You cannot remove or simplify anything without changing behavior or readability
3. A reader would not pause on any line and wonder "why is this here?"
