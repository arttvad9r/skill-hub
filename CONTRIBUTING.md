# Contributing

Skill Hub is curated rather than exhaustive. A new skill or profile should improve agent performance enough to justify its maintenance and discovery-context cost.

## Before adding a skill

A good candidate has:

- a concrete, reusable task or domain trigger;
- meaningful knowledge beyond what a strong coding model already knows;
- a maintained source when vendored from upstream;
- an explicit redistributable license;
- no machine-specific secrets, paths, device names, or personal preferences;
- minimal overlap with skills already present.

Project-specific knowledge should normally stay in that project's `AGENTS.md` or local skill instead of entering the shared Hub.

## Third-party imports

For vendored material:

1. pin a commit/release revision;
2. record source URL, revision, category, license, and license path in `catalog.toml`;
3. preserve the upstream license with the installed skill when required;
4. update `THIRD_PARTY.md`;
5. do not vendor content whose redistribution terms are unclear.

When external rules can be referenced at runtime instead of copied, prefer a small project-owned wrapper over questionable redistribution.

## Profiles

Profiles should be the smallest useful capability pack. Avoid creating a broad profile simply because several skills are related.

Base profiles should be conservative. Optional testing, performance, accessibility, security, platform, genre, or release skills should remain opt-in unless the repository facts make them clearly relevant.

## Tests

Run before opening a PR:

```bash
./bin/skillhub verify
python3 -m unittest discover -s tests -v
```

Changes to routing/workflow behavior should also run:

```bash
python3 evals/codex_bootstrap_e2e.py
```

Add a regression test for installer ownership, manifest migration, path handling, profile composition, or other behavior that could overwrite/delete user files.

## Style

- Python: standard library first; the CLI intentionally has no runtime dependencies.
- Skills: concise frontmatter descriptions with progressive disclosure in references/scripts where useful.
- Docs: explain behavior and invariants, not transient implementation history.
