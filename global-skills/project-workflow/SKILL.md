---
name: project-workflow
description: Route substantial software work through the smallest reliable workflow: discovery, bootstrap, specification, implementation, debugging, review, repository audit, verification, handoff, and retrospective guardrails. Use for new projects, ambiguous or multi-step work, non-trivial bugs, reviews/audits, refactors, migrations, or long-running work; skip trivial edits.
---

# Project Workflow

Use the smallest amount of process that makes the requested outcome reliable. This file is a router; load detailed references only when their mode applies.

## Modes

- **Discover / design** — product intent, scope, success criteria, or approach is materially unclear. Read `references/discovery.md`.
- **Bootstrap / normalize** — a new repository or an existing repo lacks reliable durable context. Read `references/bootstrap.md`.
- **Specify / plan** — substantial work needs durable requirements or a multi-step implementation plan. Read `references/spec-and-plan.md`.
- **Implement / resume** — execute non-trivial work with the smallest complete change. Read `references/implementation.md`.
- **Debug** — reproduce, isolate, fix the root cause, and prove the original failure is gone. Read `references/debugging.md`.
- **Review** — judge a diff, branch, PR, or completed change without silently editing it. Read `references/review.md`.
- **Audit** — inspect a repository or subsystem for correctness, risk, scale, test gaps, performance, and unnecessary complexity. Read `references/audit.md`.
- **Converge / verify** — prove the requested outcome and check for missing, partial, contradictory, or unrequested behavior. Read `references/verification.md`.
- **Handoff / resume** — preserve only durable state that another session cannot cheaply rediscover. Read `references/handoff.md`.
- **Retro** — turn a meaningful failure into the smallest reusable guardrail.

Do not force this workflow onto a small, obvious edit.

## Shared rules

1. Explicit user instructions outrank this workflow and specialist skills. Skills provide reusable defaults, not authority to expand scope or ignore a direct constraint.
2. Preserve user intent and existing project conventions. Ask only about unresolved product, preference, or irreversible choices that materially change the result; determine reversible technical details from the repository and current evidence.
3. For non-trivial implementation, think in this order: **outcome → evidence → impact surface → reuse → smallest complete change → verify**. Smallest means no missing callers, tests, fixtures, config, exports, state transitions, or user-visible paths required by the change.
4. Prefer existing project code/patterns, then platform or standard-library capability, then an already-installed dependency, then a maintained external dependency, and only then custom infrastructure. Do not add flexibility, abstractions, config, or dependencies for hypothetical future needs.
5. Never simplify away trust-boundary validation, data-loss prevention, security, accessibility basics, required error handling, real-hardware calibration, or behavior the user explicitly requested.
6. Scale evidence and independent review to risk. Compilation is not proof of runtime behavior when a practical stronger check exists.
7. Keep durable project knowledge in the repository, but prefer pointers over duplicated prose. Turn repeatable failures into tests, static rules, evals, or CI before adding persistent instructions.
8. Keep one writer per working tree. Parallel agents are for independent read-only investigation/review or isolated worktrees with explicit non-overlapping ownership.

## Product ambiguity gate

Do not invent preference-heavy product decisions merely to keep moving. Engine, story, visual identity, branding, monetization, destructive migrations, or other consequential choices need an explicit prior decision when they materially affect the result. Reversible implementation details normally do not.

## Specialist skills

When domain-specific capability is needed, use the global `skill-hub` router to select the smallest justified project-local profile set. Installation makes a skill available; it does not make every installed skill relevant to every task. Load specialist skill bodies only when their triggers match.

## Risk and review

Use lightweight checks for mechanical low-risk edits; realistic behavioral evidence for normal features, bugs, integrations, and UX flows; and deeper affected-suite evidence plus independent read-only review when practical for auth, security, user data, migrations, architecture boundaries, releases, or repeated failed fixes.

After roughly two or three meaningful review/fix cycles, persistent serious findings mean re-check assumptions or architecture instead of continuing an endless patch loop.

## Parallelism and long work

Work directly for simple or sequential tasks. For substantial unfinished work crossing sessions, keep the active plan updated with completed slices, decisions, verification, blockers, and the next actionable step. Do not create routine session logs.

## Retro

After a meaningful failure, prefer a reusable guardrail in this order: test → lint/static rule → eval/CI/build check → concise documentation. Persistent instructions are the last resort when the lesson genuinely requires judgment.

## Repository instructions

Prefer a short `AGENTS.md` with verified commands, non-obvious constraints, and pointers to durable docs. Use `CLAUDE.md` only for genuinely Claude-specific behavior; otherwise point it to `AGENTS.md`. Templates are optional starting points, not mandatory output formats.

## Completion report

State briefly what changed, what was actually verified, what works, and what remains unverified, blocked, intentionally out of scope, or a known accepted risk.
