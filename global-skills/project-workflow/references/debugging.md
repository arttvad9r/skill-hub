# Systematic debugging

Use this for non-trivial bugs, regressions, flaky behavior, integration failures, or when an attempted fix did not solve the problem. For an obvious typo or deterministic one-line defect, fix it directly and verify it.

## 1. Reproduce before changing code

Get the smallest reliable reproduction you can. Record the exact failing command, scenario, input, environment, and observed result when those details matter.

If the failure cannot be reproduced, gather evidence rather than guessing: logs, stack traces, state transitions, version differences, recent changes, or a narrowed diagnostic check.

## 2. Locate the failing boundary

Trace the path from expected behavior to observed failure. Narrow the problem by checking boundaries between components, data transformations, lifecycle/state transitions, external integrations, and assumptions about environment or timing.

Distinguish symptom from cause. A downstream null, timeout, render glitch, or exception is not automatically the root cause.

Before editing a shared function, interface, state transition, schema, or lifecycle path, map the affected surface far enough to avoid a local symptom patch: relevant callers/consumers, siblings using the same shared path, tests/fixtures, config/interfaces, persistence, and user-visible flows. Fix the violated assumption once at the narrowest shared root when that is the correct boundary.

For regressions, inspect the smallest relevant history or diff when it can materially shorten the search.

## 3. Form one testable hypothesis

State the smallest plausible root-cause hypothesis supported by current evidence and identify what observation would confirm or reject it. Test that hypothesis before making a production fix.

Do not stack multiple speculative changes together. If a hypothesis fails, discard it and use the new evidence to form the next one.

## 4. Fix the root cause

Apply the smallest change that corrects the violated assumption or failing boundary. Prefer existing project patterns and avoid unrelated cleanup, broad rewrites, defensive layers, retries, sleeps, or catch-all fallbacks that merely hide the symptom.

If the correct fix requires changing intended product behavior or scope, make that change explicit rather than silently redefining the bug.

## 5. Prevent regression

Where a suitable test seam exists, add or improve a reproducing regression test that fails before the fix and passes after it. Otherwise use the strongest practical deterministic check for the failure mode.

For race conditions or flaky failures, prefer a deterministic trigger, invariant, or stress/repetition check over arbitrary delays.

## 6. Verify beyond the reproduction

Re-run the original failing scenario and the relevant nearby tests/checks. Confirm that the fix did not merely change the symptom or break adjacent behavior.

If a required check cannot run, report the limitation. Do not call the bug fixed solely because the code looks plausible.

## 7. Escalation rule

After two unsuccessful speculative fixes, stop patching. Return to reproduction and evidence collection, re-check assumptions and recent changes, and narrow the failing boundary again.

If the failure exposed a repeatable class of mistake, use the workflow retro rule: prefer a test, static/lint rule, or CI/build guardrail before adding more prose instructions.
