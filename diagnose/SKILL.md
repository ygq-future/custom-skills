---
name: diagnose
description: "Diagnose hard, flaky, or performance bugs with unknown root causes via a fast headless reproduction loop and falsifiable hypotheses."
---

# Diagnose

Disciplined root-cause loop for non-obvious bugs, flaky failures, and performance regressions. *(When the root cause is already known and verified, skip this skill and fix directly via `impl`.)*

## 1. Build a Tight Headless Reproduction Loop

Do NOT guess fixes from code inspection before establishing a reproducible pass/fail signal:
1. Pick the fastest non-intrusive headless runner that reaches the bug path: targeted failing test, CLI fixture command, HTTP/`curl` script, isolated replay harness, or headless browser script (for web DOM/console/network checks).
2. **Non-intrusive rule**: Never launch visible desktop GUI windows, steal window focus, take OS desktop screenshots, or simulate OS mouse/keyboard input unless explicitly requested.
3. **Tighten the signal**: Assert the exact reported failure mode (or baseline latency/allocation metric for perf regressions). For flaky bugs, amplify stress/concurrency/iterations until the failure reproduces reliably.
4. **Redact secrets**: Never echo tokens, keys, or auth headers into logs or chat (`<REDACTED>`).
5. If a headless repro is genuinely impossible without external fixtures/logs or human GUI interaction, state what was tried and ask for the minimal missing artifact—never guess blindly.

## 2. Minimize & Hypothesize

1. **Shrink the repro**: Strip unrelated inputs, config, and steps until only load-bearing elements remain.
2. **Rank 2–4 falsifiable hypotheses**: For each, state a concrete prediction: *"If `<X>` causes this, then `<probe/change Y>` will observe `<Z>`."*

## 3. Probe One Variable at a Time

1. Test hypotheses in order using debugger/REPL inspection, profilers/query plans (for perf), or minimal targeted logs.
2. Tag every temporary probe with a unique grep-friendly marker (e.g., `[DBG-7f2a]`). Never scatter untagged print statements.

## 4. Fix, Lock Down & Clean Up

1. Turn the minimized repro into a permanent behavioral regression test at the right public seam (when a valid seam exists) and watch it fail on the unpatched code.
2. Apply the minimal root-cause fix and confirm both the regression test and the original scenario pass.
3. Grep and remove **all** `[DBG-...]` probes and throwaway reproduction scripts.
4. Hand off into `post-impl` (and `code-review` if the fix spans multiple modules or alters public contracts) before yielding.
