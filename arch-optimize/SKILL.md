---
name: arch-optimize
description: "USER-INITIATED ONLY. Audit codebase hotspots to surface shallow modules, leaky seams, and testability bottlenecks, then plan targeted module-deepening refactors."
disable-model-invocation: true
---

# Architecture Optimize

Periodic architectural survey and module-deepening workflow. Turns fragmented, shallow code into **deep modules** with high caller leverage, strong maintenance locality, and clean test seams.

## 1. Deep-Module Principles (Evaluation Lens)

- **Depth & Leverage**: A deep module hides substantial complexity, policy, and invariants behind a small, simple interface. A shallow module exposes an interface nearly as complex as its implementation.
- **The Deletion Test**: Imagine deleting the module/layer. If total complexity drops, it was pure pass-through indirection; if complexity explodes across N callers, it earns its keep.
- **Interface = Test Seam**: Callers and tests cross the same public seam. Needing to mock internal helpers or inspect private state proves the seam is in the wrong place.
- **Two-Adapter Rule**: One implementation means a hypothetical seam; do not introduce an interface/port unless at least two concrete adapters exist (e.g., production I/O + in-memory test double) or an architectural boundary requires decoupling.
- **Dependency Classification for Deepening**:
  1. *In-process pure/state*: Merge shallow pieces directly; test through the unified interface.
  2. *Local stand-in available (SQLite/in-memory FS)*: Keep seam internal; test with real local stand-in.
  3. *Owned remote boundary / Third-party I/O*: Inject a minimal port at the boundary; provide real + in-memory/mock adapters.

## 2. Hotspot Discovery

1. **Scope first**: Use the subsystem named by the user; otherwise inspect `git log --oneline -n 100` to prioritize high-churn hotspots where architectural friction actually taxes ongoing work. Respect any existing `GLOSSARY.md` and `docs/adr/` decisions.
2. **Explore**: Use indexed symbol search (XERJ / LSP) or a read-only exploration subagent to trace call graphs and pinpoint:
   - Understanding one feature requires bouncing across many tiny files/layers;
   - Pass-through wrappers, single-implementation ports, or fragmented validation;
   - Modules tightly coupled across leaky state or untestable without heavy internal mocking.

## 3. Non-Intrusive Report & Interactive Deepening

Present 3–5 ranked refactoring candidates directly in Markdown in chat (with compact `mermaid` before/after structure diagrams where helpful). **Never auto-open browser windows or steal desktop focus**; write a `docs/` report file only if the user explicitly asks for a saved artifact.

For each candidate, show:
- **Title & Strength** (`Strong` | `Worth Exploring` | `Speculative`)
- **Involved Files**: Concrete paths
- **Friction**: Why current boundaries hurt locality or testability
- **Deepening Proposal**: Target interface shape, what moves inside, and which obsolete shallow tests/files get replaced
- **Blast Radius**: Callers affected and migration safety

End with a **Top Recommendation** and stop—ask which candidate the user wants to refine (via `clarify`), split (via `breakdown`), or execute (via `impl`).
