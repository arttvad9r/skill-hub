# Skills library

This directory is the **inactive specialist-skill library** used by Skill Hub.

Skills here are not loaded globally. `skillhub install` copies only the skills selected by a project's profiles into:

- `.claude/skills/` for Claude Code;
- `.agents/skills/` for Codex.

Each directory contains one Agent Skill with a `SKILL.md` file and, when needed, references, scripts, assets, or upstream license material.

## Browse the library

The generated [catalog](../CATALOG.md) is the easiest way to browse all current skills and profiles from GitHub. It includes category, source, pinned revision, and license metadata.

For third-party attribution and license locations, see [THIRD_PARTY.md](../THIRD_PARTY.md).

## Do not install everything

The library is intentionally larger than any one project should receive. Prefer curated profiles and install only capabilities justified by the repository or the current task:

```bash
skillhub detect .
skillhub show android-compose-app
skillhub install --project . --profile android-compose-app
```

Project-local copies are tracked in `.skillhub.toml`; `skillhub status` and `skillhub sync` manage updates without silently replacing local edits.
