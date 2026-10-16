---
name: voiceover
description: iOS VoiceOver essentials — accessibility traits, labels/values/hints, custom elements, accessibilityElements order, and rotor support. Use this when building or auditing iOS UI for screen-reader users.
---

# VoiceOver (iOS)

## Instructions

VoiceOver exposes the accessibility tree built from `UIAccessibility` / SwiftUI modifiers. Your job is to expose accurate **label, value, traits, hint** for every interactive element and to control reading order when the visual tree diverges from logical order.

### 1. Label, Value, Hint, Traits

```swift
// UIKit
deleteButton.isAccessibilityElement = true
deleteButton.accessibilityLabel = "Delete message"        // WHAT it is
deleteButton.accessibilityValue = nil                      // CURRENT state (for stateful things)
deleteButton.accessibilityHint = "Removes the selected message"   // OPTIONAL extra context
deleteButton.accessibilityTraits = .button
```

```swift
// SwiftUI
Button(action: delete) {
    Image(systemName: "trash")
}
.accessibilityLabel("Delete message")
.accessibilityHint("Removes the selected message")
// traits inferred for Button; override via .accessibilityAddTraits / .accessibilityRemoveTraits
```

Rules:

- **Label** names the element. No role word ("button", "image") — VoiceOver reads the trait.
- **Value** is the current setting (slider %, switch on/off, progress, current selection).
- **Hint** is optional and can be disabled by the user; never put required info there.
- **Traits** convey role: `.button`, `.link`, `.header`, `.image`, `.selected`, `.adjustable`, `.updatesFrequently`, `.causesPageTurn`, `.playsSound`, `.searchField`.

### 2. Stateful Controls

```swift
struct A11ySwitch: View {
    @Binding var isOn: Bool
    var body: some View {
        Button { isOn.toggle() } label: { SwitchVisual(on: isOn) }
            .accessibilityLabel("Dark mode")
            .accessibilityValue(isOn ? "On" : "Off")
            .accessibilityAddTraits(isOn ? [.isButton, .isSelected] : .isButton)
    }
}
```

For custom sliders use `.accessibilityAdjustableAction`:

```swift
Capsule()
    .accessibilityElement(children: .ignore)
    .accessibilityLabel("Volume")
    .accessibilityValue("\(Int(volume * 100)) percent")
    .accessibilityAddTraits(.isAdjustable)
    .accessibilityAdjustableAction { direction in
        switch direction {
        case .increment: volume = min(1, volume + 0.05)
        case .decrement: volume = max(0, volume - 0.05)
        @unknown default: break
        }
    }
```

### 3. Reading Order with `accessibilityElements`

When a view's visual order differs from its subview order (overlays, z-indexed cards), set the order explicitly.

```swift
// UIKit
containerView.accessibilityElements = [title, body, primaryCta, secondaryCta]
```

```swift
// SwiftUI — contain children as a single element or order them
VStack { header; body; footer }
    .accessibilityElement(children: .contain)
```

`children: .combine` merges child labels into one focus stop. `children: .contain` preserves them but groups. `children: .ignore` hides children so only the container is focusable.

### 4. Grouping List Cells

Each row should be a single focus stop that announces the whole row.

```swift
HStack {
    Avatar(user)
    VStack(alignment: .leading) { Text(title); Text(subtitle) }
    Spacer()
    Text(timestamp)
}
.accessibilityElement(children: .combine)
.accessibilityLabel("\(title), \(subtitle), \(timestamp)")
.accessibilityAddTraits(.isButton)
.accessibilityAction { openConversation() }
```

### 5. Rotor Support

The VoiceOver rotor lets users jump by element type (headings, links, form fields, custom categories).

```swift
.accessibilityRotor("Unread messages") {
    ForEach(unread) { msg in
        AccessibilityRotorEntry(msg.title, id: msg.id)
    }
}
```

Use `.accessibilityAddTraits(.isHeader)` or UIKit `accessibilityTraits.insert(.header)` so headings appear in the default Headings rotor.

### 6. Custom Actions

```swift
MessageRow()
    .accessibilityAction(named: "Archive") { archive() }
    .accessibilityAction(named: "Report")  { report()  }
```

These appear in the VoiceOver actions rotor and remove the need for swipe gestures.

### 7. Announcements and Notifications

```swift
UIAccessibility.post(notification: .announcement, argument: "Saved")
UIAccessibility.post(notification: .screenChanged, argument: firstElement) // moves focus
UIAccessibility.post(notification: .layoutChanged, argument: newElement)   // no full screen change
```

Prefer in-tree live behavior (updating a visible label whose container has `updatesFrequently`) over one-shot announcements when possible.

### 8. Hiding and Isolating

- `.accessibilityHidden(true)` removes the subtree from the a11y tree.
- `.accessibilityElementsHidden(true)` (UIKit `accessibilityElementsHidden`) hides *children* but keeps the container focusable.
- For modal presentation, mark background content with `.accessibility(addTraits: .isModal)` (or UIKit `accessibilityViewIsModal = true`) so VoiceOver cannot escape into underlying content.

### 9. Common Pitfalls

- Labeling an icon with its shape ("Magnifying glass") instead of its action ("Search").
- Including "button" / "image" in the label — VoiceOver announces it from traits, resulting in "Search button button".
- Forgetting `.accessibilityValue` on stateful controls → user hears the label but not whether it's on.
- Not marking modal overlays → VoiceOver swipes into the dimmed content behind a sheet.
- Using tap gestures on plain `Text` without `.accessibilityAddTraits(.isButton)`.

## Checklist

- [ ] Every interactive element has label + trait; stateful ones also have value.
- [ ] No role words in labels ("button", "image").
- [ ] Custom controls expose `.accessibilityAdjustableAction` where appropriate.
- [ ] List rows combine children into one focus stop.
- [ ] Overlays set `accessibilityViewIsModal` / `.isModal`.
- [ ] Headings expose the `.isHeader` trait.
- [ ] Custom row actions available via the actions rotor.
- [ ] Verified on a device with VoiceOver at largest Dynamic Type.
