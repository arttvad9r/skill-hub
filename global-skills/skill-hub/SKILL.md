---
name: skill-hub
description: Select and install project-local specialist skills through the skillhub command for Claude Code and Codex. Use during project bootstrap/normalization and whenever a project gains a new specialized domain such as Android, game development, design, security, performance, navigation, or testing. Prefer curated profiles based on objective project facts instead of guessing skill relevance.
---

# Skill Hub

Keep global skill context small. Specialized skills live in the Skill Hub checkout and are copied into the repository only when the project actually needs them.

## Selection workflow

1. Use conversation context and inspect the repository before selecting anything.
2. Run `skillhub detect <project>` for objective filesystem/build signals.
3. Run `skillhub profiles` or `skillhub show <profile>` when you need to inspect available packs.
4. Choose the smallest profile set justified by explicit product requirements or observable repository facts.
5. Prefer profiles over individual `--skill` installs. Do not read every Hub skill body to decide relevance.
6. Treat installed skills as available capabilities, not a checklist. For the current task, read/invoke only the specialist skill(s) whose trigger actually matches.
7. Install into both agents with `skillhub install --project <project> --profile <profile>`.
8. Add focused profiles later when scope makes them relevant. Installation is additive, never replaces existing copies, and is recorded in `<project>/.skillhub.toml`. Remove a profile, explicit skill, or agent target with `skillhub remove --project <project> --profile|--skill|--target ...` instead of deleting folders by hand.
9. Newly installed skills may not be visible in the session that installed them. In Claude Code a `.claude/skills/` directory created mid-session is not watched: tell the user they can run `/reload-skills`, and meanwhile read the needed `SKILL.md` directly from `.claude/skills/<name>/`. Codex usually detects changes; if not, the skill applies after a restart.
10. Use `skillhub status <project>` before claiming the project-local copies are current. It reports `outdated` (Hub changed), `modified-locally` (project copy edited), missing copies, and skills added to or removed from a profile.

## Decision rules

- Android app → `android-app`; Jetpack Compose app → `android-compose-app`. These are intentionally minimal.
- Setting up or materially changing Android test infrastructure → add `android-testing`.
- Adaptive/multi-form-factor Compose work → add `android-compose-ui`; do not add it merely because the app uses Compose.
- Android game → `android-game`.
- Original game assets or shader work → add `game-art`.
- Real-time action, camera, physics, or feedback polish → add `game-action`.
- Authored levels → add `game-levels`.
- NPC/game AI → add `game-ai`.
- Dialogue or save-heavy game → add `game-narrative`.
- Procedural generation → add `game-procedural`.
- Broad game project where all curated game disciplines are genuinely in scope → `game-full`.
- General interface/design work → add `design` (Impeccable + focused UI skills + UI/UX Pro Max).
- Web interface/site work → use `design-web`; it adds focused web-only UI skills and the final audit.
- If only a final standards audit is needed → add `design-web-audit`.
- Explicitly expressive/Awwwards-style public-facing site → optionally add `design-expressive`; do not use it for dashboards or ordinary app UI.
- Android navigation/security/performance/styles work → add the matching `android-*` profile.
- CameraX, identity, on-device AI, Media3, Play, Glance, Wear, TV, Cars, XR, Compose migration/performance, or AGP migration → add the matching focused `android-*` profile.
- Mobile accessibility work → `mobile-accessibility`; Android-specific accessibility → `android-accessibility`.
- A known game genre → add exactly one matching `game-genre-*` profile; game jam/prototype/Steam/itch workflow → matching `game-workflow-*` profile.
- Security-sensitive application or infrastructure work → `security-core`; explicit static-analysis task → `security-scan`; LLM/RAG/tool-using agent system → `security-llm`.
- Existing Dockerfile work → `docker-build`; existing Compose stack → `docker-compose`; Dockerizing a new project from scratch → `docker-project`.
- FastAPI API/service work → `fastapi` (official FastAPI guidance).

Do not install a profile for hypothetical future work. If a capability becomes relevant later, add it then.

## Safety and ownership

Project installs are copies, not symlinks. Hub updates never silently change existing repositories. `skillhub sync` is the explicit update operation: it refreshes unmodified copies and applies profile changes from the Hub.

The installer refuses to overwrite or delete a project-local skill it did not write unchanged (a local edit, or a skill it does not manage) unless `--force` is supplied. Do not use `--force` without first understanding the conflict; a local edit is usually intentional and should be kept or upstreamed to the Hub.
