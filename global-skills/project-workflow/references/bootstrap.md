# Bootstrap / normalize

## 1. Understand before writing

Inspect existing `README*`, `AGENTS.md`, `CLAUDE.md`, build/package files, CI, docs, repository status, and recent commits when useful. For brownfield work, derive the actual project shape from code rather than trusting stale prose.

Resolve only product choices that materially affect the initial structure. Do not ask about technical details the agent can determine from the repository or current platform guidance. If the product itself is still materially unclear, use `discovery.md` before committing to structure.

## 2. Research only decisions that need it

Use current authoritative docs for framework/platform setup, dependency choice, security-sensitive defaults, compatibility, or fast-moving tooling. Prefer a ready-made maintained solution over custom infrastructure when it clearly fits.

Research should answer a concrete decision. Do not create a research document just to prove research happened. Persist research only when its findings will affect future decisions or maintenance.

## 3. Select project-local specialist skills

When the repository needs domain-specific capabilities, follow the global `skill-hub` skill before implementation: it owns the selection rules, install commands, and update/removal semantics. Select the smallest curated profile set justified by the product and repository; do not install skills for hypothetical future work.

Installation is availability, not eager context: do not read every installed `SKILL.md`; load only a skill whose trigger applies to the current task. Skills installed into a new project may not be visible to the current session until reloaded (see `skill-hub`); read the needed `SKILL.md` by path rather than proceeding without it.

## 4. Documentation budget

Create the minimum durable set needed now:

- `README.md`: purpose, main capabilities, prerequisites, setup, run/build/test commands, and a short project map when useful.
- `AGENTS.md`: only verified commands, non-obvious constraints, and pointers such as “read `docs/REQUIREMENTS.md` when changing product behavior”.
- `docs/REQUIREMENTS.md`: only when the product has durable non-trivial requirements spanning multiple tasks.
- `docs/specs/<topic>.md`: for a substantial bounded feature whose requirements should survive across sessions.
- `docs/plans/<topic>.md`: temporary implementation plan for active substantial work.
- `docs/adr/NNNN-<decision>.md`: only when a significant architectural decision has alternatives and future reversal cost.

For a genuinely complex or long-lived system, increase the process budget only as evidence demands it. Useful additions can include:

- focused research notes for decisions likely to be revisited;
- an architecture overview when multiple subsystems and boundaries cannot be understood cheaply from code;
- ADRs for consequential choices with credible alternatives;
- a dependency/task graph when parallel work or sequencing is genuinely non-obvious.

Do not create `ARCHITECTURE.md`, glossary, roadmap, changelog, session logs, ADR folders, specs, research notes, dependency graphs, or plans merely because a template allows them.

## 5. Repository hygiene

Check that ignore rules cover generated output, local IDE/cache files, credentials, `.env`, signing material, and platform-specific build artifacts. Add `.env.example` only when environment variables are genuinely required and ensure it contains no secrets.

Do not commit secrets or generated artifacts. Do not rewrite unrelated history or configuration. Do not create commits unless the user asked for them or the surrounding workflow already clearly authorizes commits.

## 6. Automation budget

For a long-lived, shared, published, or frequently changed repository, move stable high-signal local checks into CI when doing so reduces regression risk. Start with the cheapest checks that protect real behavior: formatting/static analysis, focused tests, then build/package checks as appropriate. Keep throwaway prototypes and tiny experiments local unless automation has clear value.

CI should mirror commands that developers and agents can run locally. Do not make routine CI depend on production credentials, destructive external state, or irreversible actions. Release/deploy automation is a separate decision and should follow the project's actual release model.

When local tests use disposable fixtures and have no production access, `AGENTS.md` may explicitly authorize agents to run them, fix failures caused by the requested change, and rerun affected checks without asking for approval at every step.

## 7. Git workflow

When creating a new project, choose the branch model based on how releases work and document it in the project's `AGENTS.md` under `## Git`:

- With releases (store, tags, published versions): `main` holds released code only (tag `vX.Y.Z`), `dev` is integration; work in `feat/*` / `fix/*` from `dev`.
- Without releases: `main` is the working branch; work in `feat/*` / `fix/*` from `main`.
- If it is unclear whether the project will have releases, ask the user before choosing the model.

Do not impose or rewrite this branch model in an established repository that already has a deliberate Git workflow unless the user asks for it.

## 8. AGENTS.md shape

Keep it compact. `templates/agents.md` is an optional starting point; delete unused sections rather than filling them with boilerplate.

Typical content:

```md
# Project instructions

## Commands
Build: `<verified command>`
Test: `<verified command>`
Lint: `<verified command>`
Run: `<verified command>`

## Constraints
- <only non-obvious project-specific rules>

## Context
- Read `<path>` before changing <area>.

## Git
- <chosen branch model>
```

Never invent commands. If a command cannot be verified, label it unknown instead of guessing.

## 9. Brownfield normalization

Prefer surgical fixes over replacing project conventions. Identify stale or duplicated agent instructions, but remove or consolidate them only when their purpose is understood. Preserve useful domain knowledge even if its format differs from the preferred structure.

Do not retrofit greenfield documentation or Git conventions into an established repository merely for consistency with this skill.

Finish bootstrap by reporting what durable context was created or corrected and which uncertainties remain.
