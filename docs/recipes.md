# Profile recipes

Skill Hub is intentionally conservative: start with the smallest profile that matches facts you already know, then add focused packs only when the project or task requires them.

## Android Compose app

```bash
skillhub install --project . --profile android-compose-app
```

Adds the minimal Android/Compose tooling profile. Add focused capabilities later:

```bash
skillhub install --project . --profile android-navigation
skillhub install --project . --profile android-testing
skillhub install --project . --profile android-security
skillhub install --project . --profile android-performance
```

Do **not** add adaptive UI, CameraX, Media3, Wear, TV, Cars, or XR unless the product actually uses them.

## Web UI or public site

```bash
skillhub install --project . --profile design-web
```

Use `design-web-audit` instead when you only want a final standards review without the full design/tooling pack.

Use `design-expressive` only for deliberately high-variance editorial/marketing experiences; it is not a default dashboard/app profile.

## Desktop or native app UI

```bash
skillhub install --project . --profile design
```

This keeps the design stack cross-platform and avoids web-only HTML/CSS skills.

## New Dockerized service

```bash
skillhub install --project . --profile docker-project
```

For FastAPI:

```bash
skillhub install --project . --profile fastapi
```

Add `security-core` when the service crosses trust boundaries, handles auth/secrets, exposes privileged operations, or otherwise deserves explicit security review.

## Existing Compose stack

```bash
skillhub install --project . --profile docker-compose
```

Add `docker-build` when Dockerfile/image work is in scope. Add `docker-safety` when agents may manipulate destructive container state.

## Game project

Start narrow:

```bash
skillhub install --project . --profile game-core
```

Then compose one genre and only the relevant disciplines:

```bash
skillhub install --project . --profile game-genre-tower-defense
skillhub install --project . --profile game-action
skillhub install --project . --profile game-art
```

If the project truly spans most engine-neutral disciplines, `game-full` exists — but it should be the exception rather than the starting point.

## LLM / RAG / tool-using agent

Use the normal application profile first, then add:

```bash
skillhub install --project . --profile security-llm
```

This focuses on prompt-injection boundaries, model-controlled tools, retrieval/memory provenance, deterministic authorization, data leakage, and unbounded resource use.

## Accessibility work

Cross-mobile accessibility:

```bash
skillhub install --project . --profile mobile-accessibility
```

Android-focused work:

```bash
skillhub install --project . --profile android-accessibility
```

## Only one agent

Project install:

```bash
skillhub install --project . --profile design-web --target claude
# or --target codex
```

Global routing layer:

```bash
~/SkillHub/bin/skillhub bootstrap --target claude
# or --target codex
```

## When no profile is the right answer

A small experiment with no specialist domain needs no profile. Do not install profiles for hypothetical future work. If a capability becomes relevant later, add it then.
