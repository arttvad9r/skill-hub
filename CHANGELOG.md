# Changelog

## Unreleased — public launch candidate

- Make bootstrap safe for public use: personal preferences are opt-in via `--preferences`.
- Add Apache-2.0 licensing for original Skill Hub material.
- Generalize the Android emulator skill so it is not tied to one machine's AVD fleet.
- Replace vendored Vercel agent-skill content with a project-owned wrapper that references the canonical public Web Interface Guidelines.
- Upgrade `.skillhub.toml` to v3 with per-target source/revision provenance.
- Refuse implicit adoption of unmanaged skills even when their contents match the Hub.
- Reject symlinks inside installable skill packages.
- Add public architecture, security, and contribution documentation.

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
