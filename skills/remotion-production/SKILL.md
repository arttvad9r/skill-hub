---
name: remotion-production
description: Build and verify Remotion video work using the current official Remotion Agent Skills as an external reference rather than a vendored snapshot. Use for Remotion project setup, compositions, media handling, Studio preview, rendering, captions, maps, or upgrades; pair with snapcn when reusable video primitives fit.
---

# Remotion production

Use the current public Remotion Agent Skills as the technical authority. Skill Hub intentionally does not vendor their text because the upstream skills repository does not currently publish explicit redistribution terms.

Canonical source:

```text
https://github.com/remotion-dev/skills/tree/main/skills/remotion-best-practices
```

Start with the current router:

```text
https://raw.githubusercontent.com/remotion-dev/skills/main/skills/remotion-best-practices/SKILL.md
```

## Workflow

1. Inspect the existing project, package versions, compositions, assets, and local instructions before changing anything. Preserve user edits and existing conventions.
2. Fetch the current official router when network access is available. Follow only the references relevant to the task instead of loading the whole skill tree.
3. For new or edited compositions, use the current official create and markup guidance. For rendering, media inspection, captions, Studio, maps, SaaS, or upgrades, load the matching official reference from the same repository.
4. Prefer the project's installed Remotion APIs and version-compatible patterns. Do not assume an API from memory when the installed version or current docs can answer it.
5. Use `snapcn` when an existing component or workflow fits the requested shot. Do not rebuild a complex cursor, device frame, terminal, kinetic title, or similar primitive merely to avoid a reusable component.
6. Keep rendered motion deterministic: derive visual state from the frame/timeline, seed randomness, and avoid wall-clock timers or browser animation loops that can drift from the renderer.
7. Preview the real composition while iterating when a browser/Studio is available. If the user asked for a finished media file, render it; if they asked only for source or an interactive draft, do not spend time on a final encode unnecessarily.
8. Verify the actual output. Inspect representative stills and transitions before the final encode, then verify the encoded file's dimensions, duration, frame rate, audio/captions, and playback when those are part of the deliverable.

## Official references

Use the matching current file under:

```text
https://github.com/remotion-dev/skills/tree/main/skills/remotion-best-practices/
```

Important sections include:

- `remotion-create/REFERENCE.md` — project/composition creation;
- `remotion-markup/REFERENCE.md` — React/Remotion markup, timing, transitions, media, effects, fonts, 3D, audio, SFX, voiceover;
- `remotion-multimedia/REFERENCE.md` — media metadata and browser media tasks;
- `remotion-render/REFERENCE.md` — rendering/export;
- `remotion-captions/REFERENCE.md` — captions and transcription;
- `remotion-studio/REFERENCE.md` — Studio workflow;
- `remotion-maps/REFERENCE.md` — maps and geographic motion;
- `remotion-saas/REFERENCE.md` — Player/rendering services and Remotion-powered apps;
- `remotion-docs/REFERENCE.md` — current API documentation lookup;
- `remotion-upgrade/REFERENCE.md` — version upgrades.

If network access is unavailable, work from the project's installed Remotion version and local docs/types. Say that the current upstream skill could not be checked rather than pretending a cached rule is current.

## Boundaries

- `motion-production` owns creative direction, story beats, routing, and final visual QA.
- This skill owns Remotion-specific implementation and current upstream guidance.
- `snapcn` owns its component catalog and component-specific behavior.
- Specialist workflow skills such as `remotion-product-demo` own their narrow archetype.

Do not duplicate these layers into competing local rules.