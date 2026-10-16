# Skill Hub

Curated project-local skill library and lifecycle manager for Claude Code and Codex.

## Commands
- Version: `skillhub --version`
- Install/update the minimal global layer: `skillhub bootstrap [--target both|claude|codex]`
- Remove this checkout's global layer: `skillhub unbootstrap [--target both|claude|codex]`
- Validate catalog/profiles: `skillhub verify`
- Verify generated browser catalog: `python3 tools/render_catalog.py --check`
- List profiles: `skillhub profiles`
- Inspect a profile: `skillhub show <profile>`
- Detect a project: `skillhub detect <project>`
- Install/add profiles: `skillhub install --project <project> --profile <profile>`
- Check managed copies: `skillhub status <project>`
- Update managed copies: `skillhub sync <project>`
- Deterministic tests: `python3 -m unittest discover -s tests -v`
- Real-agent evals: `python3 evals/codex_bootstrap_e2e.py` / `python3 evals/claude_bootstrap_e2e.py`

## Rules
- Keep the global skill set minimal; specialized skills belong in this Hub and are copied project-locally.
- Prefer objective profile selection over choosing individual skills by intuition.
- Do not add a skill without recording source, revision/import state, and license metadata in `catalog.toml`.
- Preserve upstream license files with vendored skills. Do not edit vendored upstream content unless the change is intentional and documented.
- Regenerate `CATALOG.md` whenever `catalog.toml` or `profiles/` changes.
- `backups/` is local recovery state and must not be committed.

## Public repository rules
- Keep public defaults machine- and user-agnostic; personal configuration must be explicit and opt-in.
- Do not vendor third-party material without a clear redistributable license and recorded provenance.
- Treat `bootstrap`, `unbootstrap`, `install`, `sync`, `remove`, manifest migration, and path handling as destructive-risk surfaces: add regression coverage for behavior changes.
- Prefer a smaller high-signal catalog/profile over adding overlapping skills for collection size.
- Public claims about agent compatibility/evals must match recorded evidence in `evals/RESULTS.md`.
