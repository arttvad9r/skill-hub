# Skill Hub real-agent evals

The scripts in this directory are manual end-to-end evals for the global routing layer. Each creates a disposable Git repository and gives the agent only a product request; the prompt does **not** name the skills it should use.

Current harnesses:

- `codex_bootstrap_e2e.py` — Codex CLI;
- `claude_bootstrap_e2e.py` — Claude Code.

A bootstrap eval passes only when the agent independently exposes evidence of the `project-workflow → skill-hub` routing chain, installs the lean `android-compose-app` profile, leaves Git history unchanged after the baseline commit, keeps managed skill copies current, runs no `adb`/`emulator`/`android-emu claim` commands, and produces a debug APK.

The device check inspects shell commands in the agent trace. It cannot prove that other external tools never touched a device, so it is evidence rather than isolation; run evals on a machine with no attached devices/running emulators when that guarantee matters.

Run manually because these tests consume real agent quota and may access the network:

```bash
python3 evals/codex_bootstrap_e2e.py
python3 evals/claude_bootstrap_e2e.py
```

Both scripts support `--keep` to retain the generated repository and `--model MODEL` to pin a model when the CLI supports it.

The Codex harness uses an ephemeral full-access session because Android/Gradle tooling writes caches outside the disposable working tree. The Claude harness uses non-interactive auto permissions with permission prompts disabled, so actions requiring additional approval fail instead of being implicitly granted.

Normal CI intentionally runs only deterministic local checks under `tests/`; it does not spend model quota.

Recorded successful runs and environment details live in [RESULTS.md](RESULTS.md).
