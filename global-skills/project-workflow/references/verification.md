# Verification and convergence

Completion requires evidence that the requested outcome works, not confidence from reading the diff.

## 1. Define proof before implementation

For non-trivial work, state the outcome and the evidence that would prove it before changing code. This can live in the active plan, acceptance criteria, or a short working note; do not create a document just for ceremony.

Prefer the evidence closest to the user's goal:

- a build proves that code compiles/packages;
- a unit test proves a narrow contract;
- an integration test proves components cooperate under the tested conditions;
- a real runtime/user-flow check proves the actual scenario.

Do not substitute a weaker proxy for a practical stronger check. A successful build alone does not prove that pairing, navigation, permissions, persistence, UI layout, or another runtime flow works.

## 2. Converge against intent

For substantial work, compare the current implementation with the active requirements and plan. Search explicitly for:

- **missing** — a required behavior has no implementation;
- **partial** — only some states or paths satisfy the requirement;
- **contradictory** — behavior conflicts with requirements or established project behavior;
- **unrequested** — extra features, dependencies, abstractions, or refactors were added without need.

Fix issues that are clearly within agreed scope. Surface genuine product ambiguity instead of guessing.

## 3. Scale checks to risk

Use the lowest verification cost that still produces convincing evidence.

- **Low risk** — typo, rename, padding, isolated mechanical change: focused check plus relevant static/build validation.
- **Medium risk** — feature, bug fix, UX flow, integration change: targeted regression coverage plus the realistic behavior/user flow when practical.
- **High risk** — auth, security, user data, migrations, architecture boundaries, release/deploy behavior: deeper affected-suite coverage, realistic scenarios, and an independent read-only review when available.

Risk changes verification depth; it does not silently authorize destructive actions, production changes, publishing, or scope expansion.

## 4. Run checks from narrow to broad

Typical order:

1. reproduction or targeted tests for changed behavior;
2. relevant module/package tests;
3. lint/static/type checks touching the changed area;
4. build/package step;
5. broader suite when shared behavior or architecture was affected;
6. real user-visible scenario when practical, especially for UI, integration, lifecycle, permissions, persistence, device, or runtime behavior.

Do not run expensive unrelated suites merely as ritual. Do not skip a stronger practical check merely because compilation passed.

## 5. Turn repeat failures into guardrails

When a bug or missed requirement can be checked mechanically, encode it as a regression test, lint/static rule, eval, or CI/build check instead of adding another prose reminder. Use documentation or a skill only when the lesson genuinely requires human/model judgment. Global instructions are the last resort.

For a critical manual-only flow, keep the smallest durable verification pointer needed so later work knows how to re-check it.

## 6. Check documentation drift

If commands, setup, user-visible behavior, architecture decisions, verification contracts, or durable requirements changed, update the corresponding durable documentation. Do not update docs that are unaffected.

Remove temporary debug files, abandoned scaffolding, dead flags, unused dependencies, and temporary plan/spec artifacts whose lifecycle is complete.

## 7. Completion report

Report only checks that actually ran. Distinguish clearly:

- **verified** — command/scenario actually executed and passed;
- **not verified** — could not run or was intentionally skipped, with reason;
- **blocked** — external condition prevented completion.

A failed or unavailable required check means the work is not fully verified. Do not present it as finished.
