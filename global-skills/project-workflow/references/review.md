# Review

Use this mode when judging an existing diff, branch, PR, or completed implementation. Review is evidence gathering, not another implementation pass. Do not modify code unless the user asks for fixes after the findings.

## 1. Establish the review boundary

Identify the base and changed surface: working tree, merge base, commit range, branch, or explicit files. Read only the requirements, specs, ADRs, and project instructions relevant to that surface.

## 2. Review on separate axes

Keep these questions distinct so one cannot hide the other:

- **Intent/spec:** Does the change implement the requested behavior completely, without contradictions or unrequested scope?
- **Engineering quality:** Is the implementation correct, maintainable, secure enough for its risk, consistent with repository conventions, and covered by appropriate verification?

For a large diff, independent read-only passes or subagents can review these axes in parallel. For a small diff, review directly. Never let multiple agents edit the same working tree concurrently.

## 3. Use fresh context when it materially helps

For medium/high-risk changes, repeated failed fixes, or substantial uncertainty, prefer an independent reviewer with fresh context when one is available and the extra cost is justified. Give the reviewer the intended outcome, acceptance criteria, changed surface, and verification evidence; avoid priming them with the implementer's defense of the approach.

Keep this pass read-only. Verify findings before acting on them. Do not spend an independent review on trivial low-risk edits.

After roughly two or three meaningful review/fix cycles, persistent serious findings are a signal to reconsider the approach or assumptions rather than continuing an endless patch loop.

## 4. Verify findings

Trace each potential issue to concrete code and, when practical, reproduce it with a focused test, build, static check, or executable scenario. Do not report hypothetical style preferences as defects.

Prioritize findings by user impact and risk:

- **Critical:** data loss, serious security/safety issue, unusable core behavior.
- **High:** requested behavior is wrong or a likely production regression.
- **Medium:** meaningful edge-case, maintainability, performance, or reliability problem.
- **Low:** worthwhile cleanup that does not materially affect correctness.

## 5. Report findings first

For each finding, give the severity, location, concrete failure/risk, and the smallest credible correction. If no material finding exists, say so and state what was actually checked and what remains unverified.
