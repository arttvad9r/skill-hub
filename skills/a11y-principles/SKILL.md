---
name: a11y-principles
description: POUR (Perceivable, Operable, Understandable, Robust) principles translated to mobile contexts. Use this when kicking off a new feature or doing an accessibility triage of an existing screen.
---

# Mobile Accessibility Principles (POUR)

## Instructions

Use POUR as the *mental model* behind every accessibility decision. Each principle maps to concrete mobile constraints and platform APIs.

### 1. Perceivable

Users must be able to perceive the information on screen through at least one of their senses.

- Provide text alternatives for non-text content (icons, images, charts).
- Do not rely on color alone — pair with icon, text, or shape.
- Honor Dynamic Type / font scale so content remains readable.
- Respect dark mode and high-contrast settings.

iOS (SwiftUI):

```swift
Image(systemName: "exclamationmark.triangle.fill")
    .foregroundStyle(.red)
    .accessibilityLabel("Warning")                 // text alternative
    .accessibilityAddTraits(.isImage)
```

Android (Jetpack Compose):

```kotlin
Icon(
    imageVector = Icons.Filled.Warning,
    contentDescription = stringResource(R.string.a11y_warning),
    tint = MaterialTheme.colorScheme.error,
)
```

### 2. Operable

All functionality must be reachable and usable by whatever input method the user relies on: touch, screen reader, switch, keyboard, voice.

- Minimum touch target: 44x44 pt iOS, 48x48 dp Android.
- Every gesture (drag, pinch, swipe) needs a single-tap alternative.
- Keyboard / D-pad / switch traversal must reach every actionable element.
- No time-limited interactions without extension or pause.

Flutter:

```dart
Semantics(
  button: true,
  label: 'Delete item',
  onTap: _delete,
  child: IconButton(
    iconSize: 24,
    constraints: const BoxConstraints.tightFor(width: 48, height: 48), // 48dp target
    icon: const Icon(Icons.delete_outline),
    onPressed: _delete,
  ),
)
```

React Native:

```tsx
<Pressable
  accessibilityRole="button"
  accessibilityLabel="Delete item"
  hitSlop={8}
  style={{ minWidth: 48, minHeight: 48, alignItems: 'center', justifyContent: 'center' }}
  onPress={onDelete}>
  <TrashIcon />
</Pressable>
```

### 3. Understandable

Content and UI must be understandable. This is where mobile teams most often fail — cryptic labels, jargon, or error messages without recovery.

- Use plain language for labels, hints, and errors.
- Keep navigation predictable across screens (same icon -> same destination).
- Errors state *what* is wrong and *how* to fix it.
- Announce state changes via live regions, not only visually.

Android (View):

```kotlin
errorText.apply {
    text = getString(R.string.email_invalid_with_hint)
    accessibilityLiveRegion = View.ACCESSIBILITY_LIVE_REGION_POLITE
}
```

### 4. Robust

Content must work reliably across assistive technologies and OS versions.

- Prefer native controls — they inherit correct roles, states, and gestures for free.
- When building custom controls, explicitly declare role, state, value.
- Test on **real** devices with VoiceOver and TalkBack, not only simulators.
- Re-test after OS upgrades; accessibility behavior changes between versions.

SwiftUI custom toggle (robust role exposure):

```swift
struct A11yToggle: View {
    @Binding var isOn: Bool
    var body: some View {
        Button(action: { isOn.toggle() }) {
            Capsule().fill(isOn ? .green : .gray).frame(width: 44, height: 24)
        }
        .accessibilityAddTraits(isOn ? [.isButton, .isSelected] : .isButton)
        .accessibilityValue(isOn ? "On" : "Off")
        .accessibilityLabel("Notifications")
    }
}
```

### 5. Applying POUR in Practice

For every new component, ask:

1. **P** — Can every piece of information be perceived without sight, without color, at 200% text?
2. **O** — Can every action be performed by VoiceOver, TalkBack, switch, keyboard, voice?
3. **U** — Does the label say *what it does*, not *what it looks like*? Is the error recoverable?
4. **R** — Does it expose role + state + value through the platform a11y API?

If any answer is "no", the component is not ready to ship.

## Checklist

- [ ] Every image/icon has a label or is marked decorative.
- [ ] No information is conveyed by color alone.
- [ ] Touch targets meet 44pt / 48dp minimums.
- [ ] Every gesture has a tap alternative.
- [ ] Reading order matches visual order.
- [ ] Errors are announced to AT, not only shown.
- [ ] Component works with VoiceOver **and** TalkBack on a physical device.
- [ ] Component passes at 200% Dynamic Type and in dark mode.
