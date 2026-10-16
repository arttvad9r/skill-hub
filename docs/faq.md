# FAQ

## Does Skill Hub load the whole catalog into every agent session?

No. Only `project-workflow` and `skill-hub` are installed globally. Specialist skills stay inactive in the Hub until a selected profile copies them into a project.

## Does Skill Hub run a daemon or background service?

No. `bootstrap` installs two routing skills and a CLI link. Claude Code or Codex invokes the CLI when the workflow calls for specialist capabilities; nothing continuously scans or mutates your repositories in the background.

## Do I need both Claude Code and Codex?

No. `bootstrap --target claude|codex` and project `install --target claude|codex` can target only one agent. `both` is the default.

## Does Skill Hub automatically change existing projects when I update the Hub?

No. Project installs are copies, not symlinks. Run `skillhub status` to see drift and `skillhub sync` to update unchanged managed copies explicitly.

## What if I edited an installed skill inside my project?

`status` reports it as `modified-locally`. `sync` refuses to overwrite or delete it unless you explicitly use `--force`.

## What happens to skills I installed myself?

Skill Hub does not adopt, overwrite, or delete unmanaged project-local skill directories simply because they have the same name/content. Ownership is recorded in `.skillhub.toml` per agent target.

## Should `.skillhub.toml` and project-local skills be committed?

Usually yes if you want collaborators and CI agents to receive the same repository-local capabilities. They are ordinary project files. If your team intentionally keeps agent configuration out of source control, follow the repository policy instead.

## How do I update Skill Hub?

Prefer a tagged release:

```bash
git -C ~/SkillHub fetch --tags
git -C ~/SkillHub checkout v0.4.1
~/SkillHub/bin/skillhub bootstrap
```

Then use `skillhub status` and `skillhub sync` in projects that should receive the update.

## How do I uninstall it?

Remove project profiles/targets with `skillhub remove`. Remove the global routing layer and CLI link with:

```bash
~/SkillHub/bin/skillhub unbootstrap
```

User-level `CLAUDE.md` / `AGENTS.md` files are not deleted by `unbootstrap`.

## Why are copied skills used instead of symlinks?

A project should not change just because the central Hub checkout moved to a newer revision. Copies make updates explicit and allow Skill Hub to hash the exact content it wrote.

## Why not just install every useful skill globally?

Global skill sprawl makes relevance harder to reason about and increases the chance of overlapping instructions. Skill Hub uses progressive disclosure: two routers globally, specialist capabilities only where the project needs them.

## Why are some popular frameworks missing?

The goal is quality and operational predictability, not raw skill count. A source is added when it provides real specialist signal, clear triggering conditions, maintainable provenance, and redistributable licensing.

## Is Windows supported?

The current bootstrap/path model is Unix-oriented. Linux is the primary environment and macOS is covered by deterministic CI. WSL is the recommended Windows route until native Windows behavior is tested and equally safe.
