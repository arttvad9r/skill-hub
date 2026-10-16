# SkillHub evals

`codex_bootstrap_e2e.py` is a manual end-to-end eval for the global routing layer. It creates a disposable Git repository and gives Codex only a product request; the prompt does **not** name the skills it should use.

The eval passes only when Codex independently selects `project-workflow` and `skill-hub`, installs the lean `android-compose-app` profile, leaves Git history unchanged after the baseline commit (same HEAD, no new commits on any ref), keeps all managed skill copies current, runs no `adb`/`emulator`/`android-emu claim` commands, and produces a buildable APK.

The device check inspects the shell commands in the Codex trace. It cannot see device access through other tools, so it is evidence, not isolation; run the eval on a machine with no attached devices or running emulators when that guarantee matters.

Run it manually because it consumes a real Codex session and may access the network:

```bash
python3 evals/codex_bootstrap_e2e.py
```

Use `--keep` to retain the generated repository for inspection, or `--model MODEL` to pin a model. The eval runs Codex with `danger-full-access` inside a disposable repository because Android/Gradle tooling writes caches outside the working tree. Do not run it on an untrusted machine or with untrusted repository content.

Normal CI intentionally runs only deterministic local checks under `tests/`; it does not spend model quota.
