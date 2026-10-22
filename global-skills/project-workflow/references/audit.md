# Repository audit

Use this for a repository, package, or subsystem audit when the user asks what is broken, risky, slow, bloated, missing, or worth improving. Audit is read-only unless the user separately asks for fixes.

## 1. Map the system first

Establish what the audited scope does and how it is expected to run. Read the smallest useful set of repository context: README/project instructions, build/deploy configuration, dependency manifests, entry points, tests, and architecture docs when they exist.

Trace the important flows end to end rather than reading files alphabetically. Prioritize paths involving user input, auth/permissions, money, persisted data, background jobs, external integrations, shared state, or other high-cost failure surfaces.

Determine the expected load from repository evidence when possible: local tool, single-user app, small service, multi-process production service, etc. Judge scale against that evidence and state material assumptions. For a large repository, go deeper where failure cost is highest and say what was not inspected.

## 2. Audit in risk order

Check these dimensions separately:

1. **Correctness** — wrong results, crashes, broken callers/contracts, edge cases, lifecycle/state mistakes, inconsistent duplicated rules.
2. **Security and data integrity** — trust-boundary validation, injection/path issues, auth/permission mistakes, secret exposure, unsafe writes, swallowed failures, destructive ordering.
3. **Scale and concurrency** — races, check-then-write patterns, per-process state that must be shared, unbounded memory/work, N+1 behavior, unexpectedly quadratic paths, duplicate background work.
4. **Regression evidence** — important logic or a previously broken behavior has no focused check capable of catching the failure.
5. **Performance** — material hot-path waste, repeated expensive work, avoidable I/O, latency or resource regressions relevant to expected load.
6. **Lean architecture** — dead/speculative code, redundant dependencies, duplicate helpers, pass-through wrappers, abstractions with no current need, near-copies that should share one source of truth, or functions/classes mixing unrelated responsibilities.

Do not confuse “lean” with “few files”. Split code when responsibilities are genuinely unrelated; do not create helpers solely to make functions look shorter.

## 3. Verify each finding

Every material finding needs a concrete case or evidence: an input, state, call path, expected load, test, trace, or code path showing what fails and why. No concrete failure/risk case means no defect finding.

Before calling code dead or duplicated, search the repository broadly enough to rule out tests, fixtures, configuration, generated/dynamic references, and alternate entry points.

Treat an explicit `shortcut: <limit>, <when to upgrade>` comment as a documented trade-off, not automatically a defect. Report it only when current requirements/load already exceed the stated limit or the shortcut is unsafe.

Recommend the smallest credible correction. Prefer deleting or reusing code when that genuinely solves the issue; do not propose frameworks, layers, config, or rewrites without evidence they are needed.

## 4. Report for action

Start with a short system summary and material load/coverage assumptions. Then group findings by action priority:

- **Must fix** — correctness, security, data loss, or failure under expected load.
- **Should fix** — meaningful reliability/performance risk, missing regression protection, costly duplication or unnecessary complexity.
- **Nice to have** — low-risk simplification or measurable but non-critical improvement.

Number findings across groups. For each material finding state:

- location/surface;
- what the code does;
- concrete failure or cost;
- smallest credible fix;
- consequence of leaving it as-is.

Avoid style-only findings and vague “consider” advice. For large audits, prioritize the highest-value findings rather than producing an exhaustive lint list. End with a concise verdict and `Not checked:` when important surfaces could not be inspected or executed.
