# Specification and plan

## Specification

Write a spec only when the work is substantial enough that product intent could be lost across implementation or sessions. Use already-known decisions; do not repeat discovery the user has already done. If the goal, intended user, success criterion, or scope is still materially unclear, resolve that through `discovery.md` first instead of hiding ambiguity inside the spec.

A useful spec contains only relevant sections:

- goal and user scenario;
- in-scope and explicitly out-of-scope behavior;
- constraints and compatibility requirements;
- observable requirements with acceptance criteria;
- important error, empty, loading, permission, offline, or edge states where applicable;
- unresolved questions that truly block a correct implementation.

For substantial specs, use stable requirement IDs (`R1`, `R2`, …). A requirement should describe behavior, not implementation mechanics.

Do not invent values or resolve product ambiguity for implementation convenience. Do not turn the spec into a file/function list.

`templates/requirements.md` is an optional starting point when a durable requirements document is useful. Remove irrelevant sections rather than filling them with boilerplate.

## Choosing an implementation approach

Before proposing architecture, inspect relevant code and use this ladder:

1. existing project capability;
2. platform/native capability;
3. standard library;
4. dependency already installed;
5. maintained external dependency;
6. custom implementation.

Choose the first level that solves the requirement cleanly. Prefer fewer moving parts and avoid abstractions for hypothetical future variants.

When several materially different approaches remain, compare only real alternatives and state the trade-off that matters to this project. Record an ADR only when the decision is consequential, has credible alternatives, and future reversal or rediscovery would be costly.

## Planning

A plan is for execution, not narration. Inspect real files, interfaces, project instructions, and verification commands before naming them.

Prefer vertical slices that produce a testable outcome. Example: “user can create a subscription” is usually better than separate “database”, “repository”, and “UI” phases that cannot be verified independently.

For each meaningful step include:

- outcome and why it exists;
- requirement IDs covered when present;
- verified files/components or clearly marked proposed additions;
- dependency on earlier steps if any;
- concrete verification and expected result.

Use a reproducing/failing test first for bug fixes and testable behavior where the codebase has a suitable test seam. Otherwise use the strongest relevant check without forcing TDD ceremony.

Do not include full future code, speculative paths, unrelated refactors, or a separate commit for every tiny action.

`templates/plan.md` is an optional skeleton for substantial work. Adapt its granularity to the task instead of reproducing it mechanically.

If the repository already uses an issue tracker and the work spans multiple independently useful slices or sessions, mirror those slices as tickets with explicit blocking relationships where that improves coordination. Do not introduce an issue tracker for a small solo task just to satisfy process. Likewise, maintain a glossary/domain model only when recurring domain vocabulary is important enough that inconsistent terminology would cause design or implementation errors.

## Plan self-check

Before execution verify:

- every requirement is covered by at least one step and one check;
- no step expands scope without a requirement;
- dependencies and interfaces are internally consistent;
- important failure states are covered;
- the plan is proportionate to the work.

For a complex change, a compact `requirement → step → verification` table is useful. For a small change, it is unnecessary. When parallel work or ordering is genuinely complex, add an explicit dependency/task graph; do not create one for a naturally linear plan.

## Document lifecycle

Durable product requirements may remain in `docs/REQUIREMENTS.md` or maintained product docs. A bounded feature spec may remain while it is useful as current product documentation; otherwise remove it after durable knowledge is transferred.

Implementation plans are temporary working state. Remove completed plans unless the project explicitly treats them as durable records. Important architectural decisions belong in ADRs, not in an ever-growing plan archive.
