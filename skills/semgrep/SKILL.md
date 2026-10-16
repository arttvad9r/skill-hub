---
name: semgrep
description: Use Semgrep Community Edition as optional static-analysis evidence during an explicit security or bug-pattern scan. Use when the user asks for static analysis, Semgrep, a security scan, or a repeatable pattern check. Do not require or install Semgrep silently.
---

# Semgrep scan workflow

Semgrep is an optional scanner, not the security model. First understand the repository and choose the narrowest useful scan.

## Procedure

1. Check whether `semgrep` is already available. Do not modify the project or install global software without authorization.
2. Prefer repository-provided Semgrep configuration when present.
3. Otherwise use a maintained upstream ruleset appropriate to the explicit task; `semgrep --config=auto` is the broad default documented by Semgrep Community Edition.
4. For security-focused review, a relevant registry ruleset such as `p/security-audit` may be used when its current license/usage terms fit the user's context.
5. Scope scans to the repository or affected paths; respect generated/vendor exclusions and inspect skipped-file output.
6. Save machine-readable output only when it materially helps triage; do not commit scan artifacts unless the project convention requires it.
7. Triage each meaningful finding against real code flow. Mark false positives explicitly; do not equate a clean scan with absence of vulnerabilities.
8. After a fix, rerun the narrow finding/affected scan and the project's normal tests.

If Semgrep is unavailable and installing it is out of scope, continue with manual `code-security` review and report that static scanning was not executed.
