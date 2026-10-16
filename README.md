# Skill Hub

**Curated, project-local Agent Skills for Claude Code and Codex — with lean profiles, safe sync, provenance, and real-agent evals.**

[![Skill Hub CI](https://github.com/arttvad9r/skill-hub/actions/workflows/skillhub.yml/badge.svg)](https://github.com/arttvad9r/skill-hub/actions/workflows/skillhub.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-5b5bd6)](https://developers.openai.com/api/docs/guides/tools-skills)

Most skill repositories answer **“what skills can I install?”**. Skill Hub focuses on the harder operational question:

> **Which capabilities should this repository get, how do I keep global context small, and how do I update them without silently overwriting local work?**

Skill Hub keeps only two small routing skills global. Domain expertise is selected through profiles and copied into each project under `.claude/skills/` and `.agents/skills/`. A manifest records ownership, per-agent provenance, and hashes so updates are explicit and inspectable.

## Why this is different

- **Project-local by default** — Android guidance does not appear in your web app; game skills do not appear in your backend.
- **Curated profiles, not “install everything”** — `android-compose-app`, `design-web`, `game-action`, `security-core`, `docker-compose`, and dozens more.
- **Safe ownership model** — unmanaged or locally edited skills are not overwritten/deleted unless you explicitly use `--force`.
- **Pinned provenance and licenses** — vendored skills record source, revision, and upstream license; original Skill Hub material is Apache-2.0.
- **Copies, not symlinks** — Hub updates cannot silently change an existing project.
- **Objective detection** — `skillhub detect` infers a conservative base set from repository facts such as Android/Compose, Docker, FastAPI, Godot, Unity, or Unreal markers.
- **Tested as agent infrastructure** — deterministic regression tests plus a real Codex bootstrap eval exercise routing, project setup, build failure recovery, and verification behavior.
- **Zero Python dependencies** — the CLI uses Python's standard library only.

Current catalog: **98 skills across 63 profiles**.

## Quick start

Requirements: Python 3.11+ and Claude Code and/or Codex. Linux is the primary tested environment.

```bash
git clone https://github.com/arttvad9r/skill-hub.git ~/SkillHub
~/SkillHub/bin/skillhub bootstrap
```

`bootstrap` installs only the global `project-workflow` and `skill-hub` routers plus a `~/.local/bin/skillhub` symlink. It does **not** replace your existing `CLAUDE.md` or `AGENTS.md` preferences.

Then, inside a project:

```bash
skillhub detect .
skillhub install --project . --profile android-compose-app
skillhub status .
```

Example detection:

```text
Facts: android, jetpack-compose, dockerfile
Base profiles: android-compose-app, docker-build
Add focused packs from product facts; do not infer optional capabilities without evidence.
```

Add only what is actually useful:

```bash
skillhub install --project . \
  --profile android-compose-app \
  --profile android-navigation \
  --profile design
```

When the Hub changes:

```bash
skillhub status .
skillhub sync .
```

`sync` refreshes copies that Skill Hub previously wrote and that remain unmodified. Local edits are reported and preserved unless `--force` is intentional.

## Optional user preferences

Personal agent preferences are deliberately **not** a public default. If you want Skill Hub to keep the same user-level preferences for Claude Code and Codex, start from the example and pass your file explicitly:

```bash
cp ~/SkillHub/global-config/user-preferences.example.md ~/.config/skillhub/user-preferences.md
$EDITOR ~/.config/skillhub/user-preferences.md
skillhub bootstrap --preferences ~/.config/skillhub/user-preferences.md
```

## What is in the catalog?

The Hub mixes carefully selected upstream skills with a small amount of project-owned glue:

| Area | Examples |
| --- | --- |
| Android | CLI/emulator workflow, Compose, Navigation 3, testing, security, profiling/R8, CameraX, Media3, Play, Wear, TV, Cars, XR, on-device AI |
| Design | Impeccable, focused UI skills, UI/UX Pro Max, optional expressive design, web-interface audit wrapper |
| Games | engine-neutral input/UI/performance, game feel, camera/physics/audio, art/shaders, AI, level design, narrative/save, procedural generation, genres and shipping workflows |
| Accessibility | WCAG/mobile accessibility, TalkBack/VoiceOver, focus, touch targets, scaling, motion, forms, RTL and audits |
| Security | application/infrastructure review, optional Semgrep workflow, LLM/agent security |
| Infrastructure | official Docker build/Compose/foundation skills and the official FastAPI skill |

Engine-specific game packs are intentionally not bundled yet. A skill belongs here only when it has enough signal to justify its maintenance and context cost.

List everything locally:

```bash
skillhub profiles
skillhub show design-web
```

## Safety model

The project manifest (`.skillhub.toml`, currently v3) tracks skill ownership separately for Claude and Codex:

- hash of the copy Skill Hub wrote;
- source and revision for that target;
- installed profiles and explicit skills;
- active agent targets.

That lets the CLI distinguish:

- `current` — managed copy matches the Hub;
- `outdated` — Hub changed but the project copy is untouched;
- `modified-locally` — project copy changed after installation;
- missing / profile-added / profile-removed states.

Skill names and managed paths are validated, destinations are confined to project skill directories, and skill packages containing symlinks are rejected.

See [docs/architecture.md](docs/architecture.md) for the full model.

## Agent workflow

The two global routing skills form a deliberately small control plane:

```text
user request
    ↓
project-workflow
    ├─ discovery / bootstrap / plan
    ├─ implementation / debugging
    ├─ review / verification
    └─ handoff / resume
            ↓
        skill-hub
            ↓
   project-local specialist skills
```

This follows the same broad direction as current agent guidance: keep repository instructions concise, use progressive disclosure for specialized knowledge, and verify work with executable feedback loops rather than ever-growing prompt scaffolding.

- OpenAI: [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)
- OpenAI: [Using skills to accelerate OSS maintenance](https://developers.openai.com/blog/skills-agents-sdk)
- Anthropic: [Agent Skills](https://www.anthropic.com/research/skills)

## Commands

```text
skillhub verify
skillhub bootstrap [--preferences FILE]
skillhub profiles
skillhub show <profile>
skillhub detect [project]
skillhub install --project <path> --profile <profile> [--profile ...]
skillhub install --project <path> --skill <skill> [--target claude|codex|both]
skillhub status [project]
skillhub sync [project]
skillhub remove --project <path> --profile <profile>
skillhub remove --project <path> --skill <skill>
skillhub remove --project <path> --target claude|codex
```

## Verification

```bash
skillhub verify
python3 -m unittest discover -s tests -v
```

Routing/workflow changes should also run the real-agent eval manually:

```bash
python3 evals/codex_bootstrap_e2e.py
```

The deterministic suite is quota-free and runs in GitHub Actions. The real-agent eval intentionally gives Codex a product request rather than telling it which skills to invoke.

## Repository layout

```text
bin/             CLI
profiles/        curated capability packs
skills/          inactive specialist-skill library
global-skills/   the two minimal routers
catalog.toml     source / revision / license metadata
tests/           deterministic installer regression tests
evals/           real-agent behavior evals
sources/         upstream license and provenance records
global-config/   optional user-preference example
```

## Contributing

New skills are welcome when they fill a real capability gap, have a clear trigger, and have redistributable licensing. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before adding a new source or profile.

## License

Original Skill Hub code and project-owned skills are licensed under the [Apache License 2.0](LICENSE). Vendored third-party material keeps its original license; see [THIRD_PARTY.md](THIRD_PARTY.md).
