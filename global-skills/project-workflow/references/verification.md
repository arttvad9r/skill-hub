# Verification and convergence

Completion requires evidence, not confidence from reading the diff.

## 1. Converge against intent

For substantial work, compare the current implementation with the active requirements and plan. Search explicitly for:

- **missing** — a required behavior has no implementation;
- **partial** — only some states or paths satisfy the requirement;
- **contradictory** — behavior conflicts with requirements or established project behavior;
- **unrequested** — extra features, dependencies, abstractions, or refactors were added without need.

Fix issues that are clearly within agreed scope. Surface genuine product ambiguity instead of guessing.

## 2. Choose checks by risk

Use the narrowest checks that genuinely prove the change, then widen where regression risk justifies it.

Typical order:

1. reproducing or targeted tests for changed behavior;
2. relevant module/package tests;
3. lint/static/type checks touching the changed area;
4. build/package step;
5. broader suite when shared behavior or architecture was affected;
6. real user-visible scenario when practical, especially for UI, integration, lifecycle, permissions, or runtime behavior.

Do not run expensive unrelated suites merely as ritual. Do not skip a stronger practical check merely because compilation passed.

## 3. Check documentation drift

If commands, setup, user-visible behavior, architecture decisions, or durable requirements changed, update the corresponding durable documentation. Do not update docs that are unaffected.

Remove temporary debug files, abandoned scaffolding, dead flags, unused dependencies, and temporary plan/spec artifacts whose lifecycle is complete.

## 4. Completion report

Report only checks that actually ran. Distinguish clearly:

- **verified** — command/scenario actually executed and passed;
- **not verified** — could not run or was intentionally skipped, with reason;
- **blocked** — external condition prevented completion.

A failed or unavailable required check means the work is not fully verified. Do not present it as finished.