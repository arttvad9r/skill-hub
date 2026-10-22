# Discovery and design

Use this when product intent, scope, or implementation direction is materially uncertain. Skip it when the task is already clear.

## 1. Build shared understanding from existing context

Use the conversation, repository, linked docs, and existing product behavior before asking questions. Establish only what matters for the decision:

- what problem is being solved;
- who experiences it;
- what observable outcome means success;
- whether the current goal is validation, MVP, or a fuller product;
- relevant platforms, compatibility, operational, legal, cost, or time constraints;
- what is explicitly out of scope;
- which unknowns would materially change the solution.

Do not turn this into a questionnaire. If most answers are already known, state the resulting understanding briefly and continue.

## 2. Resolve only consequential ambiguity

Ask the user only when a choice changes product behavior, scope, irreversible cost, or a preference that cannot be derived technically. Prefer one concrete question at a time when choices depend on one another. When useful, present 2–4 short options with the recommended option first.

Do not ask about framework details, file layout, library choice, naming, or other implementation matters that can be determined from the codebase and current platform guidance.

## 3. Challenge assumptions cheaply

For an unvalidated idea, identify the riskiest assumption and prefer the cheapest meaningful test before expensive engineering. Examples include a clickable prototype, manual workflow, small data sample, user interview, benchmark, or narrow technical spike.

Do not build infrastructure merely to validate demand or feasibility.

## 4. Compare real approaches

When there is a meaningful implementation or product choice, present only viable alternatives. Usually two or three are enough. For each, compare the trade-offs that matter here: complexity, maintenance, UX, compatibility, cost, latency, lock-in, migration risk, or delivery speed.

Recommend one approach and explain why it best fits the stated goal. Do not invent alternatives just to fill a list. Apply the shared reuse-before-custom order from `SKILL.md`; do not repeat it as a separate design exercise.

## 5. Exit condition

Discovery is complete when the goal, success criterion, scope, important constraints, and chosen/recommended direction are clear enough to specify or implement without guessing product intent.

Persist durable decisions in the appropriate requirements/spec/ADR only if they will matter after the current conversation. Do not create a separate discovery log.
