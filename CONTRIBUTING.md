# Contributing

Skill Hub is curated rather than exhaustive. A new skill or profile should improve agent performance enough to justify its maintenance, licensing, and discovery-context cost.

## First contribution

The smallest useful change is usually one of these:

- improve documentation or a profile description;
- add a regression test for installer/detection behavior;
- add a focused profile around skills already in the catalog;
- propose a high-signal skill source with clear redistribution terms.

For any change:

```bash
git clone https://github.com/arttvad9r/skill-hub.git
cd skill-hub
./bin/skillhub verify
python3 tools/render_catalog.py --check
python3 -m unittest discover -s tests -v
```

## Add a profile in 5 steps

1. Create `profiles/<name>.toml` with a precise description, `extends`, and/or `skills`.
2. Keep it smaller than a generic “install everything” pack; make optional capabilities opt-in.
3. Run `./bin/skillhub show <name>` and check the resolved skill set.
4. Regenerate the browser catalog:
   ```bash
   python3 tools/render_catalog.py
   ```
5. Run verify/tests and explain in the PR which concrete project/task should select this profile.

## Add a skill in 6 steps

1. Confirm a concrete, reusable trigger and a capability gap a strong coding model does not already cover well.
2. Put the skill in `skills/<name>/` and keep `SKILL.md` frontmatter concise.
3. Add `catalog.toml` metadata: category, source, pinned revision, source URL, license, and license file.
4. For vendored material, preserve the upstream license/notice with the installed skill when required and update `THIRD_PARTY.md`.
5. Add or update the narrowest profile(s) that should expose the skill.
6. Regenerate `CATALOG.md`, run verify/tests, and add a regression test when behavior or ownership rules changed.

## Before adding a third-party skill

A good candidate has:

- a concrete, reusable task or domain trigger;
- meaningful specialist knowledge beyond baseline model capability;
- a maintained source;
- an explicit redistributable license;
- no machine-specific secrets, paths, device names, or personal preferences;
- minimal overlap with skills already present.

Project-specific knowledge should normally stay in that project's `AGENTS.md` or local skill instead of entering the shared Hub.

For vendored material:

1. pin a commit/release revision;
2. record provenance and license metadata in `catalog.toml`;
3. preserve upstream attribution/licenses as required;
4. update `THIRD_PARTY.md`;
5. do not vendor content whose redistribution terms are unclear.

When external rules can be referenced at runtime instead of copied, prefer a small project-owned wrapper over questionable redistribution.

## Profiles

Profiles should be the smallest useful capability pack. Avoid creating a broad profile simply because several skills are related.

Base profiles should be conservative. Optional testing, performance, accessibility, security, platform, genre, or release skills should remain opt-in unless repository facts make them clearly relevant.

## Verification levels

### Documentation-only

Run:

```bash
python3 tools/render_catalog.py --check
```

and any checks affected by the edited document.

### Profiles / catalog / installer

Run:

```bash
./bin/skillhub verify
python3 tools/render_catalog.py --check
python3 -m unittest discover -s tests -v
```

### Routing / workflow behavior

Also run the relevant real-agent eval when available:

```bash
python3 evals/codex_bootstrap_e2e.py
python3 evals/claude_bootstrap_e2e.py
```

These evals consume real agent quota and may access the network. If you cannot run one, say so in the PR; a maintainer can run the quota-bearing eval when the change actually requires it.

Add a regression test for installer ownership, manifest migration, path handling, profile composition, or other behavior that could overwrite/delete user files.

## Pull requests

Keep PRs narrow. In the description, include:

- what problem/capability gap the change addresses;
- why it belongs in the shared Hub rather than one repository;
- exact verification run;
- source/revision/license for third-party material;
- any real-agent eval that was not run and why.

## Style

- Python: standard library first; the CLI intentionally has no runtime dependencies.
- Skills: concise frontmatter descriptions with progressive disclosure in references/scripts where useful.
- Docs: explain behavior and invariants, not transient implementation history.
