# Recorded real-agent eval results

These are manual, quota-bearing end-to-end runs. They complement deterministic CI; they are not a general benchmark of model quality.

## 2026-10-16 — v0.4.1 release candidate

Tested code commit: [`98e582e`](https://github.com/arttvad9r/skill-hub/commit/98e582e6f61709267021bff8d28c90e3d3873faf)

Both agents received the same product request: create a minimal Kotlin/Jetpack Compose Android app, keep the repository continuable by another agent, run available local build/static checks, do not use an emulator/physical device, and do not create a Git commit. The prompt did **not** name `project-workflow`, `skill-hub`, or an Android profile.

| Agent | Version / model | Result | Routing evidence | Selected profile | Verification |
| --- | --- | --- | --- | --- | --- |
| Claude Code | 2.1.301 / `claude-opus-5-5` | **PASS** | Actual `Skill` tool calls: `project-workflow` → `skill-hub` | `android-compose-app` (3 skills) | debug APK exists; `skillhub status` current; Git HEAD unchanged; no device command detected |
| Codex CLI | 0.162.1 / configured `gpt-6.1-sol`, medium reasoning | **PASS** | Agent independently announced `project-workflow` → `skill-hub`, then installed the expected profile | `android-compose-app` (3 skills) | debug APK exists; `skillhub status` current; Git HEAD unchanged; no device command detected |

Wall-clock runtime on this machine:

- Claude Code: ~174 s
- Codex CLI: ~242 s

Environment for these runs:

- Linux `7.2.9-arch1-1` x86_64
- Python `3.14.8`
- OpenJDK `17.0.20.1`
- local Android SDK / Gradle caches available
- network access available for documentation/dependency/toolchain resolution

### What the eval proves

For this bootstrap scenario, both agents can start from a product request and converge on the intended control path without being told which Skill Hub profile to use. The harness then independently checks the resulting manifest, project-local skills, build artifact, Skill Hub status, Git history, and shell trace constraints.

The run is deliberately useful rather than synthetic: both agents had to work through the current Android toolchain. In the recorded Codex run, the first build exposed an SDK/toolchain compatibility mismatch; Codex corrected it and reran the verification loop before the harness passed.

### Limitations

- This is one Android/Compose bootstrap scenario, not coverage of every profile or framework.
- Real-agent runs are manual because they consume model quota and may use the network; normal GitHub Actions remains deterministic and quota-free.
- The “no device command” assertion inspects shell-command traces after removing here-doc payload text. It catches direct `adb`, emulator, and `android-emu claim/start/boot` invocations; it is evidence, not OS-level isolation.
- Cached SDK/Gradle state can affect runtime and dependency resolution even though the product repository itself starts disposable and clean.
- PASS means the workflow contract held for this scenario; it does not claim that every generated implementation is optimal.

To reproduce:

```bash
python3 evals/claude_bootstrap_e2e.py
python3 evals/codex_bootstrap_e2e.py
```
