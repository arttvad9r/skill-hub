# Changelog

## Unreleased

- Add a curated motion stack with original production routing, UI animation craft/review, Remotion reference integration, reusable video workflows, data motion, WebGL, and Manim profiles.
- Refactor `project-workflow` into a smaller progressive-disclosure router with explicit implementation and repository-audit modes.
- Add impact-surface mapping, reuse-before-write, smallest-complete-change guidance, concrete review findings, risk-triggered regression checks, and optional documented `shortcut:` limits.

## v0.4.1 — 2026-10-16 — Repository and onboarding polish

- Rework README around the user outcome, automatic project routing, reproducible quick start, safe lifecycle, and common recipes.
- Add generated `CATALOG.md`, profile recipes, FAQ, and catalog freshness checks.
- Add `skillhub --version`, target-specific bootstrap/unbootstrap, safe global uninstall, and backups before forced preference replacement.
- Expand public issue/PR templates, private vulnerability reporting guidance, and third-party provenance documentation.
- Add a Claude Code real-agent bootstrap eval alongside the Codex harness and publish recorded results.
- Extend deterministic CI to Linux and macOS.

## v0.4.0 — 2026-10-16 — Public launch

- Make bootstrap safe for public use: personal preferences are opt-in via `--preferences`.
- Add Apache-2.0 licensing for original Skill Hub material.
- Generalize the Android emulator skill so it is not tied to one machine's AVD fleet.
- Replace vendored Vercel agent-skill content with a project-owned wrapper that references the canonical public Web Interface Guidelines.
- Upgrade `.skillhub.toml` to v3 with per-target source/revision provenance.
- Refuse implicit adoption of unmanaged skills even when their contents match the Hub.
- Reject symlinks inside installable skill packages.
- Add public architecture, security, and contribution documentation.

The public repository intentionally starts from a clean v0.4-era history; pre-public development history was kept private rather than publishing machine-specific/personal setup history.

## Post-v0.3 hardening

- Added safe install/sync/remove ownership semantics and v2 per-target hashes.
- Added path traversal/name validation, profile drift reporting, local-edit protection, and broader regression coverage.
- Added Docker and FastAPI capabilities plus workflow/review/handoff improvements and a real Codex bootstrap eval.

## v0.3.0

Expanded Android, accessibility, game genre/workflow, and security coverage.

## v0.2.0

Added the curated design stack and design profiles.

## v0.1.0

Made the Hub self-contained with bootstrap support, provenance records, and minimal global routing skills.
