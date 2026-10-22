# Change review

Use this mode when judging an existing diff, branch, PR, commit range, or completed implementation. Review is evidence gathering, not another implementation pass. Do not modify code unless the user asks for fixes after the findings.

## 1. Establish the boundary and intent

Identify the review surface: working tree, merge base, commits, branch, PR, or explicit files. Read the relevant requirements/specs/ADRs/project instructions before judging implementation choices.

Start with the diff, then read connected code when behavior crosses the changed lines:

- callers/consumers of changed APIs or behavior;
- important callees and shared helpers the change relies on;
- relevant tests/fixtures;
- configuration, schemas, exports/interfaces, persistence, or docs affected by the behavior;
- the user/data flow through the changed surface.

A change can break code it never edits. When a signature, return contract, state transition, persisted shape, or shared behavior changes, search the affected consumers before concluding the review.

## 2. Judge against the real operating context

Determine expected load and deployment shape from repository evidence when relevant. A local script, mobile app, single-process service, and horizontally scaled backend have different failure modes. State a material load assumption if the repository does not make it clear.

Review in this order:

1. **Intent/spec correctness** — requested behavior is complete, coherent, and does not add unrequested scope.
2. **Correctness** — results, edge cases, lifecycle/state, callers/contracts, failure paths.
3. **Security/data integrity** — trust boundaries, auth/permissions, secrets, unsafe writes, destructive ordering, swallowed errors.
4. **Scale/concurrency** — races, duplicated work, per-process state, unbounded growth, N+1 or unexpectedly expensive paths under expected load.
5. **Regression evidence** — risky new/fixed behavior has a focused check capable of failing when the bug returns.
6. **Performance** — material regressions or hot-path waste relevant to this project.
7. **Lean/maintainability** — dead/speculative code, duplicate logic, unnecessary dependencies/wrappers/config, or responsibilities mixed enough to make correctness hard to reason about.

Keep these axes separate so clean code cannot hide wrong behavior and a working happy path cannot hide unsafe architecture.

## 3. Verify findings before reporting them

A material finding requires a concrete case: an input, state, caller, expected-load scenario, test, trace, or code path that demonstrates what can fail or why the cost is real. If there is no concrete failure/risk case, do not report it as a defect.

Re-read the relevant lines and verify assumptions. Before calling code unused, search broadly enough to account for tests, fixtures, config, generated/dynamic references, and alternate entry points.

A documented `shortcut: <limit>, <when to upgrade>` is a deliberate trade-off, not automatically a finding. Report it when current requirements/load cross the limit or the shortcut is unsafe.

Propose the smallest credible fix. Avoid style taste, speculative future-proofing, and vague “consider” advice.

## 4. Use independent review selectively

For medium/high-risk changes, repeated failed fixes, or meaningful uncertainty, prefer a fresh-context read-only reviewer when available and worth the cost. Give it the intended outcome, acceptance criteria, changed surface, and verification evidence; do not prime it with the implementer's defense.

Verify independent findings before acting on them. After roughly two or three meaningful review/fix cycles, persistent serious findings signal that the approach or assumptions should be reconsidered rather than patched indefinitely.

## 5. Report findings for action

Put findings first and group by action priority:

- **Must fix** — wrong behavior, serious security/data risk, or failure under expected load.
- **Should fix** — meaningful reliability/performance issue, missing regression guard, duplication or complexity with concrete maintenance cost.
- **Nice to have** — low-risk simplification or small measurable improvement.

Number findings across groups. For each material finding include: severity/priority, location, what the code is doing, concrete problem, smallest fix, and consequence of leaving it unchanged.

If no material finding exists, say so and state what was actually checked. End with `Not checked:` when an important surface or runtime scenario could not be verified.
