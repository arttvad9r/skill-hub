---
name: animation-accessibility
description: Safe animation patterns — vestibular triggers, parallax, autoplay, flashing thresholds, and user controls. Use this when specifying motion-heavy UI like onboarding, marketing screens, and media players.
---

# Animation Accessibility

## Instructions

Motion communicates change, hierarchy, and delight. When used carelessly it causes nausea, seizures, or distraction that makes content unreadable. Build motion with safety defaults.

### 1. Vestibular Triggers to Avoid

- **Parallax scrolling** with factor > 0.2 or when multiple layers move at different rates.
- **Zoom into content** on transition (iOS stock zoom transition without crossfade).
- **3D rotation / perspective flips**.
- **Autoplay** video or animation that the user did not initiate.
- **Auto-scrolling** carousels.

Provide reduce-motion fallbacks (see the `reduce-motion` skill) and a per-feature user control where motion is central.

### 2. Flashing (WCAG 2.3.1 / 2.3.2)

Content must not flash more than **three times per second** in any one-second window. Applies to:

- Flash messages (error toasts blinking).
- Countdown timers pulsing red.
- Loading animations with high-contrast strobing.

Measure with a simple FPS/alpha-delta check:

```kotlin
// flashes/sec sanity check during animation test
val frames = captureFrames(durationMs = 1000)
val highContrastTransitions = frames.zipWithNext { a, b ->
    contrast(a.dominantColor, b.dominantColor) > 3.0
}.count { it }
assert(highContrastTransitions <= 3)
```

### 3. Autoplay Media

Stock rules:

- Video/audio that starts automatically and plays longer than 5 seconds must have a pause/stop control (WCAG 2.2.2).
- Muted autoplay is still motion — honor reduce motion.
- Provide captions for any video with speech (WCAG 1.2.2).

Example (SwiftUI):

```swift
Video(url: url)
    .onAppear { if reduceMotion { player.pause() } else { player.play() } }
    .overlay(alignment: .bottomTrailing) {
        Button(isPlaying ? "Pause" : "Play") { isPlaying.toggle() }
            .accessibilityLabel(isPlaying ? "Pause video" : "Play video")
    }
```

### 4. Carousels

- Never autoplay without an obvious pause button.
- Every slide must be reachable without gesture (tap or explicit next/prev buttons).
- Announce slide changes via live region (polite).

```tsx
// RN
<View accessibilityRole="tablist">
  <View accessibilityRole="tab" accessibilityState={{ selected: i === 0 }} />
  {/* ... */}
</View>
```

### 5. Hero / Shared-Element Transitions

- Keep translation distance small (< 30% of screen) and duration < 400ms.
- Always pair with opacity so the element crossfades rather than flying in.
- Respect reduce motion by falling back to fade.
- Do not trap focus during a transition; screen readers should re-announce the new pane title.

### 6. Entrance / Exit Animations

- Stagger cascades with < 60ms delay; anything longer feels slow and can disorient.
- Avoid simultaneous rotation + scale + translate. One or two axes max.
- Avoid "bounce" that overshoots > 10%.

Compose:

```kotlin
val spec = if (reduce) tween(0) else spring(stiffness = Spring.StiffnessMediumLow)
Modifier.animateContentSize(animationSpec = spec)
```

### 7. Loading States

- Prefer determinate progress (with `accessibilityValue` percentage) over spinners.
- Skeletons should animate at low amplitude (opacity 0.4 → 0.7) and low frequency (< 1 Hz).
- Expose "Loading" to AT via a live region or `accessibilityLabel = "Loading"`.

Flutter:

```dart
Semantics(
  label: 'Loading results',
  liveRegion: true,
  child: const CircularProgressIndicator(),
)
```

### 8. Lottie / Rive / Video-as-UI

- Provide a first-frame static image fallback for reduce motion.
- Make sure captions or accessibility label summarizes what the animation conveys ("Success").
- Avoid > 60fps flashes with high-contrast color swaps.

### 9. User Controls

For motion-heavy experiences (games, AR, onboarding), add an in-app setting:

- "Reduce animations" — default to system.
- "Disable parallax".
- "Disable autoplay video".

Persist it per-user and expose it to AT (labels, state values).

### 10. Testing

- Toggle system reduce motion on every target device.
- Record a screen capture and step frame-by-frame through any flash-prone sequence.
- Run Accessibility Inspector Audit (iOS) — it flags rapid content changes.
- On Android, enable *Developer Options → Show surface updates* to spot hidden flashing.

### 11. Common Pitfalls

- Adding a "nice" parallax header in a scroll-heavy feed; vestibular users report it immediately.
- Autoplay ad-like banners on login screens.
- Hero image zoom-and-blur transitions that ignore reduce motion.
- Skeleton shimmer at 2 Hz — flashing risk and distracting.
- Using a custom spring with damping < 0.3 (bouncy overshoot).

## Checklist

- [ ] No animation flashes more than 3 times/second.
- [ ] Parallax, autoplay, and large transforms respect reduce motion.
- [ ] Autoplay media has a reachable pause control.
- [ ] Hero transitions crossfade when reduce motion is on.
- [ ] Loading states expose progress to AT.
- [ ] Motion-heavy features have per-feature toggles.
- [ ] Screen recordings reviewed frame-by-frame for flashing.
