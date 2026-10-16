#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import signal
import subprocess
import tempfile
import tomllib
from pathlib import Path

PROMPT = """Create a new minimal Android app named SkillHubProbe using Kotlin and Jetpack Compose. One screen should show text and one button. This is a new project. Choose reasonable current technical defaults yourself, make the repository easy for another AI agent to continue, and run local build/static checks that are available. Do not use an emulator or physical device in this eval. Do not make a git commit. Keep the implementation minimal."""
EXPECTED_SKILLS = ["android-cli", "android-emu", "edge-to-edge"]
# Any direct ADB/emulator invocation or an android-emu lease counts as device use.
DEVICE_COMMAND = re.compile(r"(?:^|[\s;&|(`'\"/])(?:adb|emulator|android-emu\s+(?:claim|start|boot))(?:\s|$)")


def run(cmd: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)


def parse_trace(path: Path) -> list[dict]:
    result: list[dict] = []
    for line in path.read_text(errors="replace").splitlines():
        try:
            result.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a real Codex bootstrap eval against SkillHub.")
    parser.add_argument("--model")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--keep", action="store_true")
    args = parser.parse_args()

    if shutil.which("codex") is None:
        raise SystemExit("codex is not on PATH")
    if shutil.which("skillhub") is None:
        raise SystemExit("skillhub is not on PATH")

    project = Path(tempfile.mkdtemp(prefix="skillhub-codex-e2e-"))
    artifact_dir = Path(tempfile.mkdtemp(prefix="skillhub-codex-e2e-artifacts-"))
    trace = artifact_dir / "codex.jsonl"
    final = artifact_dir / "final.txt"

    try:
        run(["git", "init", "-q", "-b", "main"], project)
        run(["git", "config", "user.email", "skillhub-eval@example.invalid"], project)
        run(["git", "config", "user.name", "SkillHub Eval"], project)
        (project / "README.md").write_text("# SkillHubProbe\n")
        run(["git", "add", "README.md"], project)
        run(["git", "commit", "-q", "-m", "test: baseline"], project)
        baseline = run(["git", "rev-parse", "HEAD"], project).stdout.strip()

        cmd = ["codex", "--search", "-a", "never", "-s", "danger-full-access"]
        if args.model:
            cmd += ["-m", args.model]
        cmd += ["exec", "--ephemeral", "--json", "-C", str(project), "-o", str(final), PROMPT]

        with trace.open("w") as out:
            proc = subprocess.Popen(
                cmd,
                cwd=project,
                stdin=subprocess.DEVNULL,
                stdout=out,
                stderr=subprocess.STDOUT,
                text=True,
                start_new_session=True,
            )
            try:
                returncode = proc.wait(timeout=args.timeout)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGTERM)
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    os.killpg(proc.pid, signal.SIGKILL)
                raise SystemExit(f"Codex eval timed out after {args.timeout}s; trace: {trace}")

        if returncode != 0:
            raise SystemExit(f"Codex exited {returncode}; trace: {trace}")

        events = parse_trace(trace)
        agent_messages = [
            e.get("item", {}).get("text", "")
            for e in events
            if e.get("type") == "item.completed" and e.get("item", {}).get("type") == "agent_message"
        ]
        first_message = agent_messages[0] if agent_messages else ""
        assert "project-workflow" in first_message and "skill-hub" in first_message, (
            "Codex did not independently announce both routing skills in its first agent message"
        )

        commands = [
            e.get("item", {}).get("command", "")
            for e in events
            if e.get("type") in {"item.started", "item.completed"}
            and e.get("item", {}).get("type") == "command_execution"
        ]
        device_commands = [command for command in commands if DEVICE_COMMAND.search(command)]
        assert not device_commands, f"eval used a device or emulator despite the prompt: {device_commands}"

        manifest_path = project / ".skillhub.toml"
        assert manifest_path.is_file(), "missing .skillhub.toml"
        manifest = tomllib.loads(manifest_path.read_text())
        assert manifest.get("profiles") == ["android-compose-app"], manifest.get("profiles")
        installed = [item["name"] for item in manifest.get("skills", [])]
        assert installed == EXPECTED_SKILLS, installed

        status = run(["skillhub", "status", "."], project, check=False)
        assert status.returncode == 0, status.stdout + status.stderr
        assert run(["git", "rev-parse", "HEAD"], project).stdout.strip() == baseline, "Codex changed HEAD (commit or amend)"
        assert run(["git", "rev-list", "--all", "--count"], project).stdout.strip() == "1", "Codex created a commit"
        assert (project / "AGENTS.md").is_file(), "missing AGENTS.md"
        assert (project / "app/build/outputs/apk/debug/app-debug.apk").is_file(), "debug APK was not produced"

        detect = run(["skillhub", "detect", "."], project)
        assert "android-compose-app" in detect.stdout, detect.stdout

        print(f"PASS: {project}")
        print("routing: project-workflow -> skill-hub")
        print("profile: android-compose-app (lean 3-skill set)")
        print("verification: APK exists, skillhub status current, HEAD unchanged, no device commands")
        print(f"trace: {trace}")
        print(f"final: {final}")
        return 0
    finally:
        if args.keep:
            print(f"kept project: {project}")
            print(f"kept artifacts: {artifact_dir}")
        else:
            shutil.rmtree(project, ignore_errors=True)
            shutil.rmtree(artifact_dir, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
