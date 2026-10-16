# Architecture

Skill Hub separates agent configuration into three layers so specialized knowledge stays useful without becoming permanent global prompt context.

## 1. Global control plane

`skillhub bootstrap` installs only:

- `project-workflow` — development lifecycle router;
- `skill-hub` — capability-selection router;
- a `~/.local/bin/skillhub` symlink to the selected checkout.

The routing layer can target both agents (default) or only Claude/Codex with `--target`. Personal `CLAUDE.md` / `AGENTS.md` preferences are never installed unless the user explicitly passes `--preferences`; forced preference replacement creates a timestamped backup first. `skillhub unbootstrap` removes the routing skills/link belonging to this checkout and leaves user preference files untouched.

## 2. Inactive Hub catalog

`skills/` contains the canonical specialist copies and `profiles/` composes them into focused packs. Merely existing in the Hub does not make a skill visible to an agent working in another repository.

`catalog.toml` records source, revision, category, and license metadata. Third-party content is pinned and retains its upstream license.

## 3. Project-local capabilities

`skillhub install` copies selected skills into:

- Claude Code: `.claude/skills/<name>`
- Codex: `.agents/skills/<name>`

Copies are intentional. A later Hub update does not mutate a project until `skillhub sync` is run.

## Manifest v3

`.skillhub.toml` stores:

- selected profiles;
- explicitly selected skills;
- enabled targets;
- per-target content hashes;
- per-target source and revision provenance.

Per-target provenance matters because Claude and Codex copies can legitimately diverge when one copy has local edits or has not been synchronized yet.

## Ownership rules

Skill Hub only removes or refreshes a copy when it can prove ownership from the manifest and the current content still matches the hash it previously wrote.

| State | `install` | `sync` | `--force` |
| --- | --- | --- | --- |
| missing managed copy | copy | copy | copy |
| unchanged, current | keep | keep | keep |
| unchanged, Hub newer | keep + report outdated | refresh | refresh |
| locally modified managed copy | keep + report | refuse | replace |
| unmanaged existing directory | refuse | refuse | replace/adopt |
| deselected unchanged managed copy | remove | remove | remove |
| deselected locally modified copy | refuse | refuse | remove |

An unmanaged directory is not automatically adopted even when its bytes happen to match the Hub; otherwise a later profile removal could delete content Skill Hub did not originally own.

## Filesystem safety

- Skill/profile names use the Agent Skills-compatible lowercase-hyphen form and are bounded in length.
- Managed destination paths must resolve under the selected project.
- Symlinked destination skills are refused.
- Skill packages containing symlinks are rejected by verification and again before installation.
- Manifest paths are never accepted as arbitrary filesystem paths.

## Update philosophy

The Hub is deliberately explicit:

1. move the canonical Hub checkout to an intentional release/revision;
2. rerun `skillhub bootstrap` if the global routers should be refreshed;
3. `skillhub status <project>` reports project drift;
4. `skillhub sync <project>` applies safe updates;
5. locally modified copies require a human decision.

There is no silent auto-update from upstream and no global “install everything” mode.
