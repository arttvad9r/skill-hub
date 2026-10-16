---
name: switch-and-voice-control
description: Supporting iOS Switch Control + Voice Control, Android Switch Access + Voice Access, and AssistiveTouch. Use this when building any interactive UI, especially custom gestures, drag-and-drop, or non-standard controls.
---

# Switch Control, Voice Control, and AssistiveTouch

## Instructions

Users with motor impairments often rely on one or two physical switches, voice commands, or AssistiveTouch. These technologies read the same accessibility tree as screen readers, plus a few extra metadata fields.

### 1. How Each AT Works

- **iOS Switch Control**: scans the UI, highlighting focusable elements. User presses a switch to activate the highlighted item.
- **iOS Voice Control**: overlays numbered labels on every actionable element; user says "Tap 7" or "Tap Save".
- **Android Switch Access**: similar to iOS Switch Control, scanning by rows/columns.
- **Android Voice Access**: says "Click 3" or "Click Save"; also supports dictation.
- **iOS AssistiveTouch**: floating menu + eye/joystick input. Behaves like touch but needs predictable targets.

All rely on the standard accessibility tree. If VoiceOver / TalkBack can see it, these mostly can too.

### 2. Give Every Actionable Element an Accessible Name

Voice Control and Voice Access use the label to match spoken commands.

```swift
// SwiftUI — without a label, Voice Control shows only a number
Button(action: save) { Image(systemName: "square.and.arrow.down") }
    .accessibilityLabel("Save")
```

```kotlin
IconButton(
    onClick = ::save,
    modifier = Modifier.semantics { contentDescription = "Save" }
) { Icon(Icons.Outlined.Save, contentDescription = null) }
```

Without a label, the user must identify the button by its auto-assigned number — fine as fallback, bad as default.

### 3. Avoid Gesture-Only Interactions

Switch and Voice users cannot pinch, long-press, or drag reliably. Provide explicit alternatives:

- **Drag to reorder**: add "Move up" / "Move down" buttons or custom accessibility actions.
- **Swipe to delete**: add a delete button accessible via action rotor.
- **Pinch zoom**: provide `+`/`-` buttons.
- **Long press menus**: expose the menu via a visible "more" (⋯) button.

Example (SwiftUI) — reorder with custom actions:

```swift
ForEach(items) { item in
    ItemRow(item)
        .accessibilityAction(named: "Move up")   { move(item, .up) }
        .accessibilityAction(named: "Move down") { move(item, .down) }
}
```

Example (Compose):

```kotlin
Modifier.semantics {
    customActions = listOf(
        CustomAccessibilityAction("Move up")   { move(item, Direction.Up); true },
        CustomAccessibilityAction("Move down") { move(item, Direction.Down); true },
    )
}
```

### 4. Predictable Layout for Scanning

Switch Control scans in reading order. Break layouts into **scan groups**:

- SwiftUI: `.accessibilityElement(children: .contain)` + `.accessibilityLabel` to summarize group purpose.
- UIKit: `accessibilityContainerType = .semanticGroup`.
- Compose: `Modifier.semantics(mergeDescendants = true) { isTraversalGroup = true }`.

This lets a switch user skip whole sections quickly.

### 5. Voice Control Command Hints

On iOS, users can say the element's label directly. Keep labels short and speakable:

- "Save" — good.
- "Save your changes and continue" — long, hard to say reliably.
- "✓" — system can't vocalize; always provide a text label.

For common destinations, set a shorter `accessibilityUserInputLabels` list (iOS 14+):

```swift
Button("Send message", action: send)
    .accessibilityInputLabels(["Send", "Reply", "Post"])
```

### 6. Voice Access (Android) Numbers and Labels

On Android, Voice Access also scrapes `contentDescription`. To customize the spoken name without changing the a11y label, use `setAccessibilityPaneTitle` on groups and `stateDescription` to avoid verbose readouts.

### 7. AssistiveTouch

AssistiveTouch simulates taps, drags, and multi-finger gestures through a floating menu. Your UI already works with it if:

- Touch targets meet 44/48 minimums.
- There is no time-limited gesture (e.g., flick-to-dismiss with a 300ms window).
- Every hover/long-press interaction has a tap alternative.

Example — dismiss that works with AssistiveTouch:

```dart
// Flutter — support both drag-to-dismiss and a tap button
Stack(
  children: [
    Dismissible(...),
    Positioned(
      top: 8, right: 8,
      child: IconButton(
        icon: const Icon(Icons.close),
        tooltip: 'Close',
        onPressed: () => Navigator.pop(context),
      ),
    ),
  ],
)
```

### 8. Dwell Control and Eye Tracking

iOS AssistiveTouch and Android Voice Access both offer dwell control. The user hovers a pointer and it clicks after a duration. Requirements:

- Large, well-separated targets (same as motor guidelines).
- No hover-triggered side effects that commit destructive actions.
- Confirmation dialogs for destructive actions (delete, send payment).

### 9. Testing

- iOS: Settings → Accessibility → Switch Control / Voice Control / AssistiveTouch. Walk through a primary flow using only a single switch (Auto Scanning mode).
- Android: Settings → Accessibility → Switch Access / Voice Access.
- Record a video of the walkthrough for UX review.

### 10. Common Pitfalls

- Custom sliders with drag-only interaction → no Voice/Switch alternative.
- Undocumented gestures (e.g., 3-finger swipe to undo) with no button equivalent.
- Time-sensitive prompts (< 5s to confirm) that a switch user can't reach in time.
- Carousels auto-advancing while a switch user is still scanning the first slide.
- Buttons labeled with emoji/symbol only.

## Checklist

- [ ] Every actionable element has a short, speakable accessible name.
- [ ] Drag, swipe, pinch, and long-press have tap/button alternatives.
- [ ] Scan groups used so switch users can skip sections.
- [ ] No destructive action triggered by hover/dwell alone.
- [ ] Time limits are adjustable or >= 20 hours.
- [ ] Tested end-to-end with Switch Control and Voice Control / Voice Access.
