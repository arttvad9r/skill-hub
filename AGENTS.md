# Skill Hub

Curated project-local skill library for Claude Code and Codex.

## Commands
- Install/update the minimal global layer: `skillhub bootstrap`
- Validate catalog/profiles: `skillhub verify`
- List profiles: `skillhub profiles`
- Inspect a profile: `skillhub show <profile>`
- Detect a project: `skillhub detect <project>`
- Install/add profiles: `skillhub install --project <project> --profile <profile>`
- Check managed copies: `skillhub status <project>`
- Update managed copies: `skillhub sync <project>`

## Rules
- Keep the global skill set minimal; specialized skills belong in this Hub and are copied project-locally.
- Prefer objective profile selection over choosing individual skills by intuition.
- Do not add a skill without recording source, revision/import state, and license metadata in `catalog.toml`.
- Preserve upstream license files with vendored skills. Do not edit vendored upstream content unless the change is intentional and documented.
- `backups/` is local recovery state and must not be committed.
## Public repository rules
- Keep public defaults machine- and user-agnostic; personal configuration must be explicit and opt-in.
- Do not vendor third-party material without a clear redistributable license and recorded provenance.
- Treat `install`, `sync`, `remove`, manifest migration, and path handling as destructive-risk surfaces: add regression coverage for behavior changes.
- Prefer a smaller high-signal catalog/profile over adding overlapping skills for collection size.
