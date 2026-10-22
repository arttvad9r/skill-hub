---
name: motion-production
description: Plan, direct, build, and verify polished motion work without over-animating it. Use for motion graphics, product videos, animated explainers, title sequences, data motion, 3D motion, or any multi-scene animation where the agent must choose a visual direction, storyboard the beats, route to the right implementation skill, and inspect the rendered result.
---

# Motion production

Treat motion as a communication system, not decoration. Decide what must move, why it moves, and what the viewer should notice before choosing tools or effects.

## 1. Define the deliverable

Resolve only the constraints that change the work:

- purpose and audience;
- target surface or platform;
- aspect ratio and approximate duration;
- source assets, brand rules, real product UI/data, and references;
- whether audio, captions, interaction, or a rendered video is actually required.

Derive resolution, frame rate, codec, and export settings from the destination. Do not default every job to 1080p60 or any other fixed preset.

If the request is exploratory, keep the first pass cheap and editable. If the user asked for a finished video, the rendered artifact is part of the task.

## 2. Find the visual idea before coding

Write one short direction that names:

- the visual hierarchy: what is primary, supporting, and background;
- the motion character: restrained, energetic, mechanical, organic, editorial, cinematic, etc.;
- the pacing: where to hold, accelerate, reveal, and resolve;
- the recurring visual language: one or two signature transitions, camera behaviors, or type treatments.

Prefer one coherent idea over a collection of effects. Do not force camera movement, parallax, depth of field, motion blur, particles, gradients, bounce, or sound merely because the tooling can produce them.

Create alternatives only for high-impact or genuinely uncertain moments. Do not generate several variants for every scene by default.

## 3. Decompose references instead of copying them

When references exist, extract reusable structure:

- shot length and rhythm;
- hierarchy and composition;
- movement path, scale, camera, and depth;
- typography behavior;
- transition logic;
- synchronization with narration, music, or sound effects;
- how the reference establishes and resolves attention.

Rebuild the underlying motion logic in the project's own visual language. Never copy protected brand assets, UI, or distinctive creative material merely to match a reference.

## 4. Storyboard the beats

For multi-scene work, create a compact beat plan before implementation. Each beat should answer:

1. What information lands here?
2. What is the focal element?
3. What enters, changes, or exits?
4. How does this beat hand attention to the next one?
5. How long must the viewer have to read or understand it?

Use real product recordings, screenshots, copy, and data when available. Do not invent product labels, metrics, features, or UI merely to fill a scene.

## 5. Route to the narrowest implementation skill

Use the specialist that owns the problem instead of mixing several animation systems. Apply a named specialist when it is installed in the active profile; otherwise use the project's current stack and documentation rather than pretending the skill is available:

- Interactive web/UI motion: `animate`; review with `review-animations`; use `fixing-motion-performance` for jank or rendering-cost problems.
- Whole-interface motion audit: `improve-animations`; opportunity finding: `find-animation-opportunities`.
- Remotion video: `remotion-production`; use `snapcn` for reusable video primitives.
- Product/launch/video archetypes: `remotion-product-demo`, `remotion-launch-video`, `remotion-motion-graphics`, `remotion-kinetic-typography`, `remotion-logo-animation`, or `remotion-explainer-video` when the trigger matches.
- Data-led motion: `animated-infographic`, `chart-animation`, or `presentation-video`.
- Real-time 3D/WebGL: `threejs-animation`, `shader-glsl`, or `particle-system`.
- Mathematical explanation: `manim`.

Stay inside the project's existing stack when it already solves the task well. A new motion library is a cost, not an automatic upgrade.

## 6. Build for deterministic playback

For rendered video, every visual state must be reproducible from the frame or timeline. Avoid wall-clock timers, unseeded randomness, and animation systems whose internal clocks can drift from the renderer.

For interactive motion, prioritize interruption, input latency, reduced-motion behavior, and consistency with the rest of the product.

Use sound only when it improves rhythm, feedback, comprehension, or emotional intent. Do not add background music or sound effects as a mandatory polish layer.

## 7. Review the artifact, not only the code

The first working build is a review candidate, not proof of quality.

For rendered motion:

1. Render representative frames at the start, key beats, transitions, and ending.
2. Inspect a contact sheet or the frames themselves for hierarchy, cropping, safe areas, typography, continuity, and factual accuracy.
3. Preview the motion at normal speed and inspect any suspicious transition frame-by-frame.
4. Fix the issues.
5. Re-render the affected frames or sequence.
6. For a requested final deliverable, encode the final media and verify that the encoded file plays and has the intended dimensions, duration, frame rate, audio, and captions.

For interactive motion, exercise the real interaction repeatedly, including interruption/reversal, keyboard or touch behavior where relevant, reduced motion, and a performance-sensitive path.

Never call a motion task finished solely because it typechecks, builds, or renders once.

## 8. Final report

Keep the handoff short:

- what was created or changed;
- what was previewed/rendered and actually inspected;
- what destination/output settings were used and why;
- any aspect that could not be verified.

Do not claim visual QA if you only inspected source code.