---
name: focus-order
description: Controlling traversal order for screen readers, keyboards, and switches — custom focus, focus traps, and focus restoration. Use this when the visual layout diverges from the document order or when building overlays and dialogs.
---

# Focus Order

## Instructions

Focus order determines *what the user lands on next*. It applies to screen readers (swipe right), keyboards (Tab), D-pads (arrow keys), and switches. By default it follows the render tree. Override deliberately when the tree and visual order disagree.

### 1. Default Order

Every platform walks the tree in source order. A floating action button rendered at the end of the tree is read last, even if visually it's in the top-right. Check your render order before reaching for overrides.

### 2. iOS — SwiftUI and UIKit

SwiftUI:

```swift
VStack {
    TextField("Email", text: $email).accessibilitySortPriority(2)
    TextField("Password", text: $password).accessibilitySortPriority(1)
    Button("Sign in", action: submit).accessibilitySortPriority(0)
}
.accessibilityElement(children: .contain)
```

Higher priority is visited **first**. Use sparingly — usually a single `.accessibilityElement(children: .contain)` with correct layout is enough.

UIKit:

```swift
container.accessibilityElements = [title, emailField, passwordField, submitButton]
```

Setting `accessibilityElements` fully controls order and hides any unlisted subviews from VoiceOver.

### 3. Android — Views and Compose

Views:

```xml
<Button
    android:id="@+id/save"
    android:accessibilityTraversalBefore="@id/cancel" />
```

Compose:

```kotlin
Column(Modifier.semantics { isTraversalGroup = true }) {
    Text("Heading", Modifier.semantics { traversalIndex = 0f })
    Button(onClick = {}, Modifier.semantics { traversalIndex = 2f }) { Text("Save") }
    Button(onClick = {}, Modifier.semantics { traversalIndex = 1f }) { Text("Cancel") }
}
```

`traversalIndex` is a float; lower values visited first (requires Compose 1.5+ and `isTraversalGroup`).

### 4. Flutter

```dart
FocusTraversalGroup(
  policy: OrderedTraversalPolicy(),
  child: Column(children: [
    FocusTraversalOrder(order: const NumericFocusOrder(1), child: emailField),
    FocusTraversalOrder(order: const NumericFocusOrder(2), child: passwordField),
    FocusTraversalOrder(order: const NumericFocusOrder(3), child: submitButton),
  ]),
)
```

For Semantics order:

```dart
Semantics(
  sortKey: const OrdinalSortKey(1.0),
  child: heading,
)
```

All children within the same `container: true` parent are sorted by their `sortKey`.

### 5. React Native

RN follows document order; override via `accessibilityElementsHidden` (iOS) and `importantForAccessibility` (Android) to skip, or by physically reordering in JSX.

iOS-only prop:

```tsx
<View accessibilityElementsHidden={!isVisible} importantForAccessibility={isVisible ? 'auto' : 'no-hide-descendants'}>
  {/* ... */}
</View>
```

For keyboard/TV focus, use the Focus system on Android TV (`nextFocusDown`, etc.) or `onStartShouldSetResponder` patterns.

### 6. Focus Traps (Modals, Drawers, Sheets)

When an overlay opens, focus must:

1. Move **into** the overlay (first focusable element).
2. **Stay** inside the overlay until dismissed.
3. **Return** to the invoking element on dismiss.

SwiftUI:

```swift
@FocusState private var focused: Bool

.sheet(isPresented: $showSheet) {
    VStack {
        TextField("Note", text: $note).focused($focused)
        Button("Close") { showSheet = false }
    }
    .onAppear { focused = true }
}
```

Also set `.accessibilityViewIsModal` on the container so VoiceOver cannot escape into the background.

UIKit: set `accessibilityViewIsModal = true` on the presented view; post `.screenChanged` with the first focusable element.

Compose:

```kotlin
ModalBottomSheet(onDismissRequest = onClose) {
    val fr = remember { FocusRequester() }
    LaunchedEffect(Unit) { fr.requestFocus() }
    Column(Modifier.focusRequester(fr).focusGroup()) {
        TextField(...)
        Button(onClick = onClose) { Text("Close") }
    }
}
```

Use `Modifier.semantics { isTraversalGroup = true }` on the sheet content to keep TalkBack within it.

Flutter:

```dart
showDialog(
  context: context,
  useRootNavigator: true,
  barrierDismissible: false,
  builder: (_) => Semantics(
    scopesRoute: true,
    explicitChildNodes: true,
    namesRoute: true,
    label: 'Confirm delete',
    child: const ConfirmDialog(),
  ),
)
```

`scopesRoute + namesRoute` triggers TalkBack/VoiceOver route-entered announcement and scopes focus.

### 7. Focus Restoration

After dismissing a dialog or completing a flow, restore focus to the triggering element — otherwise the reader jumps to the top of the screen.

SwiftUI:

```swift
@FocusState private var invokeFocus: Bool

Button("Open") { showSheet = true }.focused($invokeFocus)

.sheet(isPresented: $showSheet, onDismiss: { invokeFocus = true }) { /* ... */ }
```

Compose: use `FocusRequester` for the trigger and re-request on dismiss.

### 8. Skip Links / Skip to Content

On long headers or tab bars, offer a "Skip to content" action when the screen reader enters the screen. Compose:

```kotlin
Modifier.semantics {
    customActions = listOf(CustomAccessibilityAction("Skip to content") {
        contentFocusRequester.requestFocus(); true
    })
}
```

### 9. Traversal Groups

Group related items so the user can navigate *between* groups quickly (using the rotor on iOS, the heading jump on Android).

- SwiftUI: `.accessibilityElement(children: .contain)` with a group label.
- Compose: `Modifier.semantics { isTraversalGroup = true; contentDescription = "..." }`.
- Flutter: `Semantics(container: true, explicitChildNodes: true, label: "...")`.

### 10. Common Pitfalls

- Overlays that don't set `isModal` → reader drops into the dim layer below.
- Focus not returning to trigger on dismiss → user re-orients from scratch.
- Fighting default order with many `sortPriority`/`traversalIndex` tweaks instead of fixing layout.
- Floating action button read last because of render order.
- Dialog without a focus requester → focus stuck on the previous screen's control.

## Checklist

- [ ] Visual and a11y order agree (verified with VoiceOver/TalkBack).
- [ ] Modals set `isModal` / `scopesRoute` and trap focus inside.
- [ ] First focus moves into the modal on open.
- [ ] Focus returns to the invoking element on dismiss.
- [ ] Long headers offer a skip-to-content action.
- [ ] Order overrides (`sortPriority`, `traversalIndex`) justified per use.
