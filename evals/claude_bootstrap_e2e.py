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
DEVICE_COMMAND = re.compile(
    r"(?:^|[;&|]\s*|\n\s*)(?:[A-Za-z_][A-Za-z0-9_]*=\S+\s+)*(?:adb(?:\s|$)|emulator(?:\s|$)|android-emu\s+(?:claim|start|boot)(?:\s|$))"
)


def strip_heredoc_bodies(command: str) -> str:
    """Remove here-doc payloads before checking which shell commands actually ran."""
    lines = command.splitlines()
    kept: list[str] = []
    delimiter: str | None = None
    for line in lines:
        if delimiter is not None:
            if line.strip() == delimiter:
                delimiter = None
            continue
        kept.append(line)
        match = re.search(r"<<-?\s*['\"]?([A-Za-z_][A-Za-z0-9_]*)['\"]?", line)
        if match:
            delimiter = match.group(1)
    return "\n".join(kept)


def run(cmd: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)


def parse_trace(path: Path) -> tuple[list[str], list[str], list[str], str]:
    texts: list[str] = []
    commands: list[str] = []
    skill_calls: list[str] = []
    raw = path.read_text(errors="replace")
    for line in raw.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        message = event.get("message", {})
        content = message.get("content", []) if isinstance(message, dict) else []
        for item in content if isinstance(content, list) else []:
            if item.get("type") == "text":
                texts.append(item.get("text", ""))
            elif item.get("type") == "tool_use":
                inp = item.get("input", {})
                if item.get("name") == "Bash" and isinstance(inp, dict):
                    commands.append(str(inp.get("command", "")))
                elif item.get("name") == "Skill" and isinstance(inp, dict):
                    skill = inp.get("skill")
                    if isinstance(skill, str):
                        skill_calls.append(skill)
                texts.append(json.dumps(item, ensure_ascii=False))
        if event.get("type") == "result":
            texts.append(str(event.get("result", "")))
    return texts, commands, skill_calls, raw


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a real Claude Code bootstrap eval against Skill Hub.")
    parser.add_argument("--model")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--keep", action="store_true")
    args = parser.parse_args()

    if shutil.which("claude") is None:
        raise SystemExit("claude is not on PATH")
    if shutil.which("skillhub") is None:
        raise SystemExit("skillhub is not on PATH")

    project = Path(tempfile.mkdtemp(prefix="skillhub-claude-e2e-"))
    artifact_dir = Path(tempfile.mkdtemp(prefix="skillhub-claude-e2e-artifacts-"))
    trace = artifact_dir / "claude.jsonl"

    try:
        run(["git", "init", "-q", "-b", "main"], project)
        run(["git", "config", "user.email", "skillhub-eval@example.invalid"], project)
        run(["git", "config", "user.name", "Skill Hub Eval"], project)
        (project / "README.md").write_text("# SkillHubProbe\n")
        run(["git", "add", "README.md"], project)
        run(["git", "commit", "-q", "-m", "test: baseline"], project)
        baseline = run(["git", "rev-parse", "HEAD"], project).stdout.strip()

        cmd = [
            "claude", "-p", "--verbose", "--output-format", "stream-json",
            "--permission-mode", "auto", "--permission-prompts", "none", "--no-session-persistence",
        ]
        if args.model:
            cmd += ["--model", args.model]
        cmd.append(PROMPT)

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
                raise SystemExit(f"Claude eval timed out after {args.timeout}s; trace: {trace}")

        if returncode != 0:
            raise SystemExit(f"Claude exited {returncode}; trace: {trace}")

        texts, commands, skill_calls, raw = parse_trace(trace)
        joined = "\n".join(texts) + "\n" + raw
        assert "project-workflow" in joined and "skill-hub" in joined, (
            "Claude did not expose both routing skills in the trace"
        )
        assert "project-workflow" in skill_calls and "skill-hub" in skill_calls, (
            f"Claude did not invoke both routing skills through the Skill tool: {skill_calls}"
        )
        device_commands = [
            command for command in commands if DEVICE_COMMAND.search(strip_heredoc_bodies(command))
        ]
        assert not device_commands, f"eval used a device or emulator despite the prompt: {device_commands}"

        manifest_path = project / ".skillhub.toml"
        assert manifest_path.is_file(), "missing .skillhub.toml"
        manifest = tomllib.loads(manifest_path.read_text())
        assert manifest.get("profiles") == ["android-compose-app"], manifest.get("profiles")
        installed = [item["name"] for item in manifest.get("skills", [])]
        assert installed == EXPECTED_SKILLS, installed

        status = run(["skillhub", "status", "."], project, check=False)
        assert status.returncode == 0, status.stdout + status.stderr
        assert run(["git", "rev-parse", "HEAD"], project).stdout.strip() == baseline, "Claude changed HEAD"
        assert run(["git", "rev-list", "--all", "--count"], project).stdout.strip() == "1", "Claude created a commit"
        assert (project / "AGENTS.md").is_file(), "missing AGENTS.md"
        assert (project / "app/build/outputs/apk/debug/app-debug.apk").is_file(), "debug APK was not produced"

        detect = run(["skillhub", "detect", "."], project)
        assert "android-compose-app" in detect.stdout, detect.stdout

        print(f"PASS: {project}")
        print("routing: project-workflow -> skill-hub")
        print("skill calls: " + ", ".join(skill_calls))
        print("profile: android-compose-app (lean 3-skill set)")
        print("verification: APK exists, skillhub status current, HEAD unchanged, no device commands")
        print(f"trace: {trace}")
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
