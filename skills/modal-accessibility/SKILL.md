---
name: modal-accessibility
description: Accessible dialogs, bottom sheets, and popovers — announcing, trapping focus, handling dismiss, and returning focus. Use this when adding modal UI to any platform.
---

# Modal Accessibility

## Instructions

Modals (alerts, action sheets, bottom sheets, popovers) are the single worst source of accessibility bugs on mobile because they change focus context. Get them right.

### 1. Announce the Modal

When a modal opens, the screen reader should announce its title and role.

- iOS: set `.navigationTitle(...)` or post `.screenChanged` with the title element.
- UIKit: `UIAccessibility.post(notification: .screenChanged, argument: dialogTitleLabel)`.
- Compose: `Dialog` / `ModalBottomSheet` with content marked `heading()`; TalkBack announces on appearance.
- Flutter: `Semantics(scopesRoute: true, namesRoute: true, label: 'Delete item')`.
- RN: `<Modal>` with `accessibilityViewIsModal` (iOS) + first focusable receives focus.

### 2. Trap Focus

Focus must not escape into the content behind.

iOS:

```swift
.sheet(isPresented: $show) {
    Content()
        .accessibilityAddTraits(.isModal)  // isModal = true in older APIs
}
```

UIKit:

```swift
dialogView.accessibilityViewIsModal = true
```

Compose — use `ModalBottomSheet` (built-in trap) or mark your overlay container:

```kotlin
Box(
    modifier = Modifier
        .fillMaxSize()
        .semantics { isTraversalGroup = true; paneTitle = "Filters" }
) { /* ... */ }
```

Flutter: `showDialog` already scopes focus; for custom overlays:

```dart
Semantics(
  scopesRoute: true,
  explicitChildNodes: true,
  namesRoute: true,
  label: 'Filters',
  child: content,
)
```

RN iOS:

```tsx
<Modal visible={show} onRequestClose={onClose} presentationStyle="pageSheet">
  <View accessibilityViewIsModal>{/* ... */}</View>
</Modal>
```

On Android, RN's `<Modal>` handles back button. Also set `importantForAccessibility="no-hide-descendants"` on the underlying root while modal is up (or wrap with `<Modal>` which manages this).

### 3. Move Focus Into the Modal

On open, focus the first interactive element (or the title heading if read-only).

SwiftUI:

```swift
@FocusState private var firstFocus: Bool
Content().onAppear { firstFocus = true }
TextField("Name", text: $name).focused($firstFocus)
```

Compose:

```kotlin
val fr = remember { FocusRequester() }
LaunchedEffect(Unit) { fr.requestFocus() }
TextField(..., modifier = Modifier.focusRequester(fr))
```

Flutter:

```dart
late final FocusNode _first;
@override void initState() { super.initState(); _first = FocusNode()..requestFocus(); }
```

### 4. Dismiss Must Be Reachable

- Provide a visible close button (minimum 44/48).
- Support Esc / hardware back.
- Allow tap-outside **only if** a visible close also exists (tap-outside isn't discoverable).

```kotlin
// Compose
BackHandler(enabled = isOpen) { onDismiss() }

AlertDialog(
    onDismissRequest = onDismiss,
    confirmButton = { TextButton(onClick = onConfirm) { Text("Delete") } },
    dismissButton = { TextButton(onClick = onDismiss) { Text("Cancel") } },
    // Close (X) in title if applicable
)
```

### 5. Return Focus After Dismiss

```swift
.sheet(isPresented: $show, onDismiss: { triggerFocus = true }) { /* ... */ }
Button("Open", action: { show = true }).focused($triggerFocus)
```

Compose — remember the triggering `FocusRequester` and re-request in `onDismiss`.

Flutter — await `showDialog` then `FocusScope.of(context).requestFocus(triggerNode)`.

### 6. Action Sheets and Popovers

Treat them as modals. Announce title, trap focus, provide Cancel/close. On iOS, `ConfirmationDialog` (SwiftUI) and `UIAlertController` handle this for free — just provide titles and actions.

### 7. Destructive Actions

- Ensure destructive buttons have `role: .destructive` (SwiftUI), `ButtonDefaults.filledTonalButtonColors(Color.Red)` is **not** enough — set `semantics { role = Role.Button; stateDescription = "Destructive" }` or use platform style.
- Require confirmation for irreversible actions.
- Don't position destructive and default actions adjacently without spacing.

### 8. Bottom Sheets

- Provide a visible drag handle *and* a close button. The drag handle alone is not accessible.
- Expose drag-to-expand as a custom action: "Expand", "Collapse".
- Announce pane change when the sheet expands.

```kotlin
ModalBottomSheet(
    onDismissRequest = onDismiss,
    dragHandle = {
        BottomSheetDefaults.DragHandle(
            modifier = Modifier.semantics {
                contentDescription = "Drag handle"
                role = Role.Button
                customActions = listOf(CustomAccessibilityAction("Close") { onDismiss(); true })
            }
        )
    }
) { /* ... */ }
```

### 9. Non-modal Popovers / Toasts

- Toasts are announced via live region; they should **not** steal focus.
- Popovers anchored to a trigger should return focus to the trigger on dismiss.

### 10. Common Pitfalls

- No close button, only tap-outside dismiss.
- Focus stays on the background button after the dialog opens.
- Dialog title not marked as heading → no announcement.
- Bottom sheet with drag-only expand.
- Dismiss gesture (swipe down) with no tap alternative.
- Focus doesn't return on dismiss → reader at top of screen.

## Checklist

- [ ] Modal title is announced on appearance.
- [ ] Focus moves into the modal (first control or heading).
- [ ] Focus trapped inside the modal (`isModal` / `scopesRoute`).
- [ ] Visible close button >= 44/48.
- [ ] Esc / hardware back dismisses.
- [ ] Focus returns to the invoking element on close.
- [ ] Destructive actions confirmed and correctly labeled.
- [ ] Bottom-sheet expand/collapse accessible without drag.
