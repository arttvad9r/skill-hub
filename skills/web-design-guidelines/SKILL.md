---
name: web-design-guidelines
description: Audit web UI for accessibility, interaction, content, forms, motion, layout, and interface-quality issues using Vercel's current public Web Interface Guidelines as an external reference. Use for final UI/UX review of web pages or components.
---

# Web interface audit

Use the current public Web Interface Guidelines maintained by Vercel as an external reference; this skill does not vendor or reproduce those guidelines.

Canonical source:

```text
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

## Workflow

1. Inspect the files/components and the real user-visible flow being reviewed.
2. Fetch the current canonical guideline source when network access is available. If it is unavailable, say so instead of pretending a cached rule set is current.
3. Apply only rules relevant to the reviewed surface. Prioritize accessibility, input/interaction correctness, responsive behavior, forms, navigation, content clarity, performance-sensitive UI behavior, and motion preferences.
4. Verify findings against the actual code and, where practical, the rendered interface. Do not report generic style preferences as defects.
5. Report findings first with severity, file/location, concrete user impact, and the smallest credible fix.
6. If no material issue is found, state what was checked and what could not be verified.

The external guideline content remains subject to its publisher's terms; only this wrapper is part of Skill Hub.
