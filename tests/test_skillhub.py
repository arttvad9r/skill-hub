#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import tomllib
import unittest
from pathlib import Path

HUB = Path(__file__).resolve().parents[1]
CLI = HUB / "bin" / "skillhub"


def run(*args: str, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(CLI), *args],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )


class SkillHubTests(unittest.TestCase):
    def test_verify(self) -> None:
        result = run("verify")
        self.assertIn("OK: 98 skills, 63 profiles", result.stdout)

    def test_public_readme_catalog_count_matches_hub(self) -> None:
        catalog = tomllib.loads((HUB / "catalog.toml").read_text())["skills"]
        profiles = list((HUB / "profiles").glob("*.toml"))
        readme = (HUB / "README.md").read_text()
        self.assertIn(f"**{len(catalog)} skills across {len(profiles)} profiles**", readme)

    def test_android_compose_default_is_lean(self) -> None:
        result = run("show", "android-compose-app")
        skills = [line[2:] for line in result.stdout.splitlines() if line.startswith("- ")]
        self.assertEqual(skills, ["android-cli", "android-emu", "edge-to-edge"])
        self.assertNotIn("testing-setup", skills)
        self.assertNotIn("adaptive", skills)

    def test_detect_compose_project(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skillhub-detect-") as tmp:
            project = Path(tmp)
            (project / "settings.gradle.kts").write_text('rootProject.name = "Demo"\n')
            app = project / "app"
            app.mkdir()
            (app / "build.gradle.kts").write_text(
                'plugins { id("com.android.application"); id("org.jetbrains.kotlin.plugin.compose") }\n'
                'android { buildFeatures { compose = true } }\n'
            )
            result = run("detect", str(project))
            self.assertIn("android", result.stdout)
            self.assertIn("jetpack-compose", result.stdout)
            self.assertIn("android-compose-app", result.stdout)

    def test_detect_docker_and_fastapi(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skillhub-server-detect-") as tmp:
            project = Path(tmp)
            (project / "Dockerfile").write_text("FROM python:3.13-slim\n")
            (project / "compose.yaml").write_text("services: {}\n")
            panel = project / "panel"
            panel.mkdir()
            (panel / "pyproject.toml").write_text('[project]\ndependencies = ["fastapi>=0.120"]\n')
            result = run("detect", str(project))
            self.assertIn("dockerfile", result.stdout)
            self.assertIn("docker-compose", result.stdout)
            self.assertIn("fastapi", result.stdout)
            self.assertIn("docker-build", result.stdout)
            self.assertIn("docker-compose", result.stdout)
            self.assertIn("fastapi", result.stdout)

    def test_sync_retires_unchanged_managed_skill(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skillhub-retire-") as tmp:
            project = Path(tmp)
            run("install", "--project", str(project), "--profile", "android-compose-ui")
            self.assertTrue((project / ".agents/skills/adaptive").is_dir())

            manifest_path = project / ".skillhub.toml"
            text = manifest_path.read_text()
            text = text.replace('profiles = ["android-compose-ui"]', 'profiles = ["android-compose-app"]')
            manifest_path.write_text(text)

            run("sync", str(project))
            self.assertFalse((project / ".agents/skills/adaptive").exists())
            self.assertFalse((project / ".claude/skills/adaptive").exists())
            self.assertTrue((project / ".agents/skills/android-cli").is_dir())
            self.assertTrue((project / ".agents/skills/edge-to-edge").is_dir())
            manifest = tomllib.loads(manifest_path.read_text())
            self.assertEqual(
                [item["name"] for item in manifest["skills"]],
                ["android-cli", "android-emu", "edge-to-edge"],
            )

    def test_project_workflow_contract(self) -> None:
        root = HUB / "global-skills/project-workflow"
        workflow = (root / "SKILL.md").read_text()
        bootstrap = (root / "references/bootstrap.md").read_text()
        self.assertIn("Explicit user instructions outrank this workflow", workflow)
        self.assertIn("Keep one writer per working tree", workflow)
        self.assertIn("references/review.md", workflow)
        self.assertIn("references/handoff.md", workflow)
        shared = workflow.split("## Shared rules", 1)[1].split("## Discover and design", 1)[0]
        numbers = [int(line.split(".", 1)[0]) for line in shared.splitlines() if line[:1].isdigit()]
        self.assertEqual(numbers, list(range(1, len(numbers) + 1)))
        self.assertIn("## 6. Automation budget", bootstrap)
        self.assertTrue((root / "references/review.md").is_file())
        self.assertTrue((root / "references/handoff.md").is_file())

    def test_sync_preserves_modified_retired_skill(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skillhub-retire-modified-") as tmp:
            project = Path(tmp)
            run("install", "--project", str(project), "--profile", "android-compose-ui")
            modified = project / ".agents/skills/adaptive/SKILL.md"
            modified.write_text(modified.read_text() + "\nlocal edit\n")

            manifest_path = project / ".skillhub.toml"
            text = manifest_path.read_text().replace(
                'profiles = ["android-compose-ui"]', 'profiles = ["android-compose-app"]'
            )
            manifest_path.write_text(text)

            result = run("sync", str(project), check=False)
            self.assertEqual(result.returncode, 2)
            self.assertIn("modified locally, no longer selected", result.stderr)
            self.assertTrue(modified.exists())

    def test_manifest_path_traversal_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skillhub-traversal-") as tmp:
            project = Path(tmp)
            docs = project / "project-docs"
            docs.mkdir()
            (docs / "requirements.md").write_text("keep me\n")
            (project / ".skillhub.toml").write_text(
                'version = 1\nprofiles = []\nexplicit_skills = []\ntargets = ["codex"]\n\n'
                '[[skills]]\nname = "../../project-docs"\nsha256 = "x"\n'
            )
            result = run("install", "--project", str(project), "--profile", "android-app", check=False)
            self.assertEqual(result.returncode, 2)
            self.assertIn("Invalid skill name", result.stderr)
            self.assertTrue((docs / "requirements.md").is_file())

    def test_install_keeps_local_edits_and_sync_refuses(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skillhub-local-edit-") as tmp:
            project = Path(tmp)
            run("install", "--project", str(project), "--profile", "android-compose-app")
            edited = project / ".agents/skills/android-cli/SKILL.md"
            edited.write_text(edited.read_text() + "\nlocal rule\n")

            run("install", "--project", str(project), "--profile", "android-testing")
            self.assertIn("local rule", edited.read_text())

            status = run("status", str(project), check=False)
            self.assertEqual(status.returncode, 1)
            self.assertIn("codex=modified-locally", status.stdout)

            sync = run("sync", str(project), check=False)
            self.assertEqual(sync.returncode, 2)
            self.assertIn("modified locally", sync.stderr)
            self.assertIn("local rule", edited.read_text())

            run("sync", str(project), "--force")
            self.assertNotIn("local rule", edited.read_text())
            self.assertEqual(run("status", str(project)).returncode, 0)


    def test_install_does_not_adopt_identical_unmanaged_copy(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skillhub-unmanaged-identical-") as tmp:
            project = Path(tmp)
            dst = project / ".agents/skills/android-cli"
            shutil.copytree(HUB / "skills/android-cli", dst)
            result = run("install", "--project", str(project), "--profile", "android-app", "--target", "codex", check=False)
            self.assertEqual(result.returncode, 2)
            self.assertIn("not managed by skillhub", result.stderr)
            self.assertFalse((project / ".skillhub.toml").exists())

    def test_manifest_tracks_provenance_per_target(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skillhub-provenance-") as tmp:
            project = Path(tmp)
            run("install", "--project", str(project), "--profile", "android-app")
            codex = project / ".agents/skills/android-cli/SKILL.md"
            codex.write_text(codex.read_text() + "\nlocal edit\n")

            manifest_path = project / ".skillhub.toml"
            before = tomllib.loads(manifest_path.read_text())
            android_before = next(item for item in before["skills"] if item["name"] == "android-cli")
            self.assertEqual(before["version"], 3)
            self.assertEqual(set(android_before["revisions"]), {"claude", "codex"})

            # Adding another profile must preserve the locally modified Codex provenance.
            run("install", "--project", str(project), "--profile", "android-testing")
            after = tomllib.loads(manifest_path.read_text())
            android_after = next(item for item in after["skills"] if item["name"] == "android-cli")
            self.assertEqual(android_after["revisions"]["codex"], android_before["revisions"]["codex"])
            self.assertIn("local edit", codex.read_text())

    def test_verify_rejects_skill_symlinks(self) -> None:
        if not hasattr(Path, "symlink_to"):
            self.skipTest("symlinks unsupported")
        with tempfile.TemporaryDirectory(prefix="skillhub-symlink-fixture-") as tmp:
            target = Path(tmp) / "target.txt"
            target.write_text("outside\n")
            link = HUB / "skills/code-security/.skillhub-test-link"
            try:
                link.symlink_to(target)
                result = run("verify", check=False)
                self.assertEqual(result.returncode, 1)
                self.assertIn("contains symlink", result.stderr)
            finally:
                link.unlink(missing_ok=True)

    def test_ownership_is_tracked_per_target(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skillhub-targets-") as tmp:
            project = Path(tmp)
            run("install", "--project", str(project), "--profile", "android-app", "--target", "claude")
            independent = project / ".agents/skills/android-cli"
            independent.mkdir(parents=True)
            (independent / "SKILL.md").write_text("---\nname: android-cli\ndescription: mine\n---\n")

            result = run("install", "--project", str(project), "--target", "codex", check=False)
            self.assertEqual(result.returncode, 2)
            self.assertIn("not managed by skillhub", result.stderr)
            self.assertIn("description: mine", (independent / "SKILL.md").read_text())
            manifest = tomllib.loads((project / ".skillhub.toml").read_text())
            self.assertEqual(manifest["targets"], ["claude"])

    def test_remove_profile_and_target(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skillhub-remove-") as tmp:
            project = Path(tmp)
            run("install", "--project", str(project), "--profile", "android-compose-app",
                "--profile", "android-testing")
            run("remove", "--project", str(project), "--profile", "android-testing")
            manifest = tomllib.loads((project / ".skillhub.toml").read_text())
            self.assertEqual(manifest["profiles"], ["android-compose-app"])
            self.assertFalse((project / ".claude/skills/testing-setup").exists())

            run("remove", "--project", str(project), "--target", "codex")
            self.assertFalse((project / ".agents/skills/android-cli").exists())
            self.assertTrue((project / ".claude/skills/android-cli").is_dir())

            run("remove", "--project", str(project), "--target", "claude")
            self.assertFalse((project / ".claude/skills/android-cli").exists())
            self.assertFalse((project / ".skillhub.toml").exists())

    def test_install_requires_existing_project(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skillhub-missing-") as tmp:
            missing = Path(tmp) / "typo"
            result = run("install", "--project", str(missing), "--profile", "fastapi", check=False)
            self.assertEqual(result.returncode, 2)
            self.assertFalse(missing.exists())

    def test_detect_android_module_not_named_app(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skillhub-modules-") as tmp:
            project = Path(tmp)
            module = project / "feature"
            module.mkdir()
            (module / "build.gradle.kts").write_text(
                "plugins { alias(libs.plugins.android.application); alias(libs.plugins.kotlin.compose) }\n"
            )
            result = run("detect", str(project))
            self.assertIn("jetpack-compose", result.stdout)
            self.assertIn("android-compose-app", result.stdout)

    def test_installed_licenses_travel_with_vendored_skills(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skillhub-license-") as tmp:
            project = Path(tmp)
            run("install", "--project", str(project), "--profile", "docker-project", "--profile", "fastapi")
            manifest = tomllib.loads((project / ".skillhub.toml").read_text())
            catalog = tomllib.loads((HUB / "catalog.toml").read_text())["skills"]
            for item in manifest["skills"]:
                if catalog[item["name"]]["source"] == "local":
                    continue
                skill_dir = project / ".claude/skills" / item["name"]
                self.assertTrue(
                    any("licen" in p.name.lower() for p in skill_dir.iterdir()),
                    f"{item['name']} has no upstream license file",
                )

    def test_original_skills_use_root_license(self) -> None:
        catalog = tomllib.loads((HUB / "catalog.toml").read_text())["skills"]
        self.assertTrue((HUB / "LICENSE").is_file())
        for name, meta in catalog.items():
            if meta["source"] == "local":
                self.assertEqual(meta["license"], "Apache-2.0", name)
                self.assertEqual(meta["license_file"], "LICENSE", name)

    def test_bootstrap_does_not_overwrite_user_config_by_default(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skillhub-home-") as tmp:
            home = Path(tmp)
            claude_config = home / ".claude/CLAUDE.md"
            codex_config = home / ".codex/AGENTS.md"
            claude_config.parent.mkdir(parents=True)
            codex_config.parent.mkdir(parents=True)
            claude_config.write_text("keep claude\n")
            codex_config.write_text("keep codex\n")
            env = os.environ.copy()
            env["HOME"] = str(home)
            subprocess.run([str(CLI), "bootstrap"], text=True, capture_output=True, check=True, env=env)
            self.assertEqual(claude_config.read_text(), "keep claude\n")
            self.assertEqual(codex_config.read_text(), "keep codex\n")
            self.assertTrue((home / ".claude/skills/project-workflow").is_dir())
            self.assertTrue((home / ".codex/skills/skill-hub").is_dir())

    def test_bootstrap_preferences_are_explicit(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skillhub-home-prefs-") as tmp:
            home = Path(tmp) / "home"
            home.mkdir()
            prefs = Path(tmp) / "prefs.md"
            prefs.write_text("# My preferences\n")
            env = os.environ.copy()
            env["HOME"] = str(home)
            subprocess.run(
                [str(CLI), "bootstrap", "--preferences", str(prefs)],
                text=True,
                capture_output=True,
                check=True,
                env=env,
            )
            self.assertEqual((home / ".claude/CLAUDE.md").read_text(), prefs.read_text())
            self.assertEqual((home / ".codex/AGENTS.md").read_text(), prefs.read_text())

    def test_version_is_available_without_subcommand(self) -> None:
        result = subprocess.run([str(CLI), "--version"], text=True, capture_output=True, check=True)
        self.assertRegex(result.stdout.strip(), r"^skillhub \d+\.\d+\.\d+$")

    def test_unbootstrap_removes_only_routing_layer(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skillhub-unbootstrap-") as tmp:
            home = Path(tmp)
            claude_config = home / ".claude/CLAUDE.md"
            codex_config = home / ".codex/AGENTS.md"
            claude_config.parent.mkdir(parents=True)
            codex_config.parent.mkdir(parents=True)
            claude_config.write_text("keep claude\n")
            codex_config.write_text("keep codex\n")
            env = os.environ.copy()
            env["HOME"] = str(home)
            subprocess.run([str(CLI), "bootstrap"], text=True, capture_output=True, check=True, env=env)
            subprocess.run([str(CLI), "unbootstrap"], text=True, capture_output=True, check=True, env=env)
            self.assertFalse((home / ".claude/skills/project-workflow").exists())
            self.assertFalse((home / ".claude/skills/skill-hub").exists())
            self.assertFalse((home / ".codex/skills/project-workflow").exists())
            self.assertFalse((home / ".codex/skills/skill-hub").exists())
            self.assertFalse((home / ".local/bin/skillhub").exists())
            self.assertEqual(claude_config.read_text(), "keep claude\n")
            self.assertEqual(codex_config.read_text(), "keep codex\n")

    def test_bootstrap_can_target_one_agent(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skillhub-one-target-") as tmp:
            home = Path(tmp)
            env = os.environ.copy()
            env["HOME"] = str(home)
            subprocess.run(
                [str(CLI), "bootstrap", "--target", "codex"],
                text=True,
                capture_output=True,
                check=True,
                env=env,
            )
            self.assertTrue((home / ".codex/skills/project-workflow").is_dir())
            self.assertTrue((home / ".codex/skills/skill-hub").is_dir())
            self.assertFalse((home / ".claude/skills/project-workflow").exists())
            subprocess.run(
                [str(CLI), "unbootstrap", "--target", "codex"],
                text=True,
                capture_output=True,
                check=True,
                env=env,
            )
            self.assertFalse((home / ".codex/skills/project-workflow").exists())

    def test_targeted_unbootstrap_keeps_shared_cli_when_other_agent_remains(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skillhub-partial-unbootstrap-") as tmp:
            home = Path(tmp)
            env = os.environ.copy()
            env["HOME"] = str(home)
            subprocess.run([str(CLI), "bootstrap"], text=True, capture_output=True, check=True, env=env)
            link = home / ".local/bin/skillhub"
            self.assertTrue(link.is_symlink())
            subprocess.run(
                [str(CLI), "unbootstrap", "--target", "codex"],
                text=True, capture_output=True, check=True, env=env,
            )
            self.assertTrue((home / ".claude/skills/project-workflow").is_dir())
            self.assertFalse((home / ".codex/skills/project-workflow").exists())
            self.assertTrue(link.is_symlink())
            subprocess.run(
                [str(CLI), "unbootstrap", "--target", "claude"],
                text=True, capture_output=True, check=True, env=env,
            )
            self.assertFalse(link.exists())

    def test_force_preferences_creates_backup(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skillhub-prefs-backup-") as tmp:
            home = Path(tmp) / "home"
            home.mkdir()
            claude_config = home / ".claude/CLAUDE.md"
            codex_config = home / ".codex/AGENTS.md"
            claude_config.parent.mkdir(parents=True)
            codex_config.parent.mkdir(parents=True)
            claude_config.write_text("old claude\n")
            codex_config.write_text("old codex\n")
            prefs = Path(tmp) / "prefs.md"
            prefs.write_text("new preferences\n")
            env = os.environ.copy()
            env["HOME"] = str(home)
            subprocess.run(
                [str(CLI), "bootstrap", "--preferences", str(prefs), "--force"],
                text=True,
                capture_output=True,
                check=True,
                env=env,
            )
            self.assertEqual(claude_config.read_text(), prefs.read_text())
            self.assertEqual(codex_config.read_text(), prefs.read_text())
            claude_backups = list(claude_config.parent.glob("CLAUDE.md.skillhub-backup-*"))
            codex_backups = list(codex_config.parent.glob("AGENTS.md.skillhub-backup-*"))
            self.assertEqual(len(claude_backups), 1)
            self.assertEqual(len(codex_backups), 1)
            self.assertEqual(claude_backups[0].read_text(), "old claude\n")
            self.assertEqual(codex_backups[0].read_text(), "old codex\n")


class FixtureHubTests(unittest.TestCase):
    """Tests that mutate Hub content run against a disposable copy of the Hub."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="skillhub-fixture-")
        self.hub = Path(self.tmp.name) / "hub"
        for name in ("bin", "profiles", "skills", "global-skills", "sources"):
            shutil.copytree(HUB / name, self.hub / name, symlinks=True)
        shutil.copy2(HUB / "catalog.toml", self.hub / "catalog.toml")
        shutil.copy2(HUB / "LICENSE", self.hub / "LICENSE")
        self.cli = self.hub / "bin" / "skillhub"
        self.project = Path(self.tmp.name) / "project"
        self.project.mkdir()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def hub_run(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run([str(self.cli), *args], text=True, capture_output=True, check=check)

    def test_status_detects_profile_change_and_hub_update(self) -> None:
        self.hub_run("install", "--project", str(self.project), "--profile", "android-app")
        self.assertEqual(self.hub_run("status", str(self.project)).returncode, 0)

        profile = self.hub / "profiles/android-app.toml"
        profile.write_text(profile.read_text().replace("skills = []", 'skills = ["edge-to-edge"]', 1))
        skill = self.hub / "skills/android-cli/SKILL.md"
        skill.write_text(skill.read_text() + "\nupdated in hub\n")

        status = self.hub_run("status", str(self.project), check=False)
        self.assertEqual(status.returncode, 1)
        self.assertIn("edge-to-edge", status.stdout)
        self.assertIn("not installed", status.stdout)
        self.assertIn("claude=outdated", status.stdout)

        self.hub_run("sync", str(self.project))
        self.assertEqual(self.hub_run("status", str(self.project)).returncode, 0)
        self.assertIn("updated in hub", (self.project / ".claude/skills/android-cli/SKILL.md").read_text())

    def test_verify_rejects_broken_skill_metadata(self) -> None:
        (self.hub / "skills/android-cli/SKILL.md").write_text("no frontmatter here\n")
        result = self.hub_run("verify", check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("android-cli: missing YAML frontmatter", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
