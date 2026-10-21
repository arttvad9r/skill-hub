---
name: project-workflow
description: Discover and shape substantial software work, bootstrap or normalize repositories, create durable requirements and implementation plans, guide execution, debug and review systematically, hand work across sessions, and verify completion. Use for new projects, messy repos, substantial features, refactors, migrations, bugs requiring investigation, reviews, or multi-step work; skip trivial edits.
---

# Project Workflow

Use the smallest amount of process that makes the work reliable and easy to continue across sessions.

## Modes

- **Discover / design** — clarify a substantial idea, scope, success criteria, and real alternatives before implementation.
- **Bootstrap** — new repository or existing repo without clear durable context.
- **Specify / plan** — substantial or ambiguous multi-step work.
- **Implement / resume** — execute or continue an agreed plan.
- **Debug** — reproduce a non-trivial problem, find its root cause, apply the smallest correct fix, and prove it.
- **Review** — judge a diff or implementation against intent and engineering quality without silently editing it.
- **Converge** — compare requirements, plan, and result before completion.
- **Handoff / resume** — preserve only the durable state needed to continue substantial unfinished work.
- **Retro** — turn a meaningful failure into the smallest useful guardrail.

Do not force this workflow onto a small, obvious edit.

## Shared rules

1. Explicit user instructions outrank this workflow and specialist skills. Skills provide reusable defaults, not authority to expand scope or ignore a direct constraint.
2. Preserve user intent, scope, and existing project conventions.
3. Prefer the smallest correct solution: existing project code → platform/native capability → standard library → installed dependency → maintained external dependency → custom code.
4. Research current authoritative documentation when a technical choice may have changed or materially affects the design.
5. Keep durable project context in the repository, not only in chat. Keep temporary process documents temporary.
6. Prefer context pointers over duplicated instructions in `AGENTS.md` or `CLAUDE.md`.
7. For non-trivial work, define the intended outcome and the evidence that would prove it before implementation. Prefer direct evidence of the requested behavior over proxy evidence such as compilation alone.
8. Scale verification and review to risk: low-risk mechanical edits need lightweight checks; medium-risk features, bugs, and UX flows need realistic behavior verification; high-risk auth, security, data, architecture, or release work needs deeper evidence and independent review when available.
9. Record only significant architectural decisions as ADRs; routine choices do not need one.
10. Do not turn process templates into mandatory bureaucracy; adapt or skip them when the project is simpler.
11. Installing a specialist skill makes it available; it does not make every installed skill mandatory for every task. Load a skill body only when its trigger matches the work.
12. Keep one writer per working tree. Use parallel agents only for independent read-only investigation/review or isolated worktrees with non-overlapping ownership.
## Discover and design

For a substantial new idea or materially ambiguous change, establish the real problem, intended user, success criteria, scope, constraints, and important unknowns before choosing architecture. Reuse decisions already present in the conversation or repository. Ask only about unresolved product choices that materially change the result.

When there is a real choice, compare a small number of viable approaches with project-specific trade-offs and recommend one. For an unvalidated product idea, prefer the cheapest meaningful validation before expensive implementation.

Read `references/discovery.md` when product intent or approach still needs shaping.

## Bootstrap

Inspect the repository before creating files. Preserve useful existing conventions and fix only missing or misleading context.

Before implementation, when the project needs domain-specific capabilities (a platform, framework, game, design, security, or infrastructure domain), use the `skill-hub` skill to select and install project-local specialist skills through the `skillhub` command. A small experiment with no specialized domain needs none. Base selection on explicit product requirements and observable repository facts, prefer curated profiles over individual skills, and never copy the whole Hub speculatively. Revisit selection only when the project gains a new specialized domain.

Scale documentation to the project:
- small experiment: usually `README.md` + concise agent instructions;
- normal app: add durable requirements when behavior is non-trivial and a plan for substantial current work;
- complex/long-lived system: add focused research, architecture docs, ADRs, or dependency/task mapping only when they carry real decision value.

Create only useful artifacts. Never create empty doc shells, session logs, duplicated instruction files, or speculative architecture.

Read `references/bootstrap.md` when bootstrapping or normalizing a repo.

## Specify and plan

Use known conversation context first. Ask only about unresolved choices that materially change product behavior or scope. Requirements must describe observable outcomes; use stable IDs (`R1`, `R2`, …) when cross-references help. Inspect the real codebase before naming files, interfaces, commands, or architecture. Prefer vertical, testable slices over plans grouped only by technical layers.

Read `references/spec-and-plan.md` for substantial specifications or plans.

## Implement and resume

Read the relevant requirements and current plan, then compare them with actual code and recent history so finished work is not repeated. Treat the plan as a guide, not a transcript. Technical changes within agreed behavior may update the plan; product or scope changes must remain explicit. Prefer focused changes and reuse existing code. Avoid speculative abstractions and unrelated cleanup.

A plan step is complete only after its corresponding verification succeeds. For non-trivial steps, decide what observation would prove the outcome before implementing it. When behavior has a cheap stable seam, prefer a focused failing/regression test before or alongside the implementation; do not force test-first ceremony where the test would be more expensive or brittle than the behavior.

## Debug

For non-trivial bugs, do not jump from symptom to speculative fix. Reproduce the failure, collect evidence, isolate the failing boundary, form and test the smallest plausible root-cause hypothesis, then fix the root cause and verify the original reproduction plus relevant regressions.

Read `references/debugging.md` for investigation-heavy bugs, regressions, flaky behavior, integration failures, or repeated unsuccessful fixes.

## Review

Review intent/spec correctness separately from engineering quality so one cannot mask the other. Verify material findings against concrete code or executable evidence. For medium/high-risk work, repeated failed fixes, or material uncertainty, prefer a fresh-context independent review when an appropriate reviewer is available; keep it read-only until findings are verified. Do not modify the reviewed change unless the user asks for fixes.

Read `references/review.md` for branch, PR, working-tree, or implementation reviews.

## Converge and verify

Before declaring substantial work done, compare requirements, plan, and implementation for **missing**, **partial**, **contradictory**, and **unrequested** behavior. Then run the strongest practical checks for the changed surface.

Read `references/verification.md` before completing substantial work.

## Handoff and resume

For substantial unfinished work that must cross sessions, update the active plan with only the state another agent cannot cheaply rediscover: completed slices, decisions, verification, blockers, and the next step. Do not create routine session logs.

Read `references/handoff.md` when work is intentionally stopping before completion or resuming from a prior handoff.

## Parallelism

Work directly for simple or sequential tasks. Use subagents when work is genuinely independent, benefits from isolated context, or can run in parallel without sharing mutable state. For parallel implementation, use isolated worktrees/branches and explicit ownership; never run two writers against the same working tree.

## Retro

After a meaningful failure, prefer a reusable guardrail in this order: test → lint/static rule → CI/build check → concise documentation. Add persistent instructions only for lessons that genuinely require judgment and cannot be enforced mechanically.

## Repository instructions

Prefer a short `AGENTS.md` as the shared project instruction source: real commands, non-obvious constraints, and pointers to durable docs. Do not copy README, requirements, architecture, or tutorials into it. Use `CLAUDE.md` only for genuinely Claude-specific behavior; otherwise point it to `AGENTS.md`.

The files under `templates/` are optional starting points, not required output formats.

## Completion report

State briefly what changed, what was actually verified, what works, and what remains unverified, blocked, or intentionally out of scope.
