---
name: keyboard-and-hardware-input
description: Keyboard, D-pad, and hardware-switch support on iOS (Full Keyboard Access), Android, Flutter, and React Native. Use this when building screens that must be usable without touch.
---

# Keyboard and Hardware Input

## Instructions

Many users navigate mobile apps with an external Bluetooth keyboard, a hardware switch, a game controller, or Android TV / CarPlay surfaces. Touch is not the only input.

### 1. iOS — Full Keyboard Access

iOS 14+ has Full Keyboard Access (FKA). Users navigate with Tab, arrow keys, Space, Return, and Esc. You need to:

- Make every interactive element focusable (native controls are by default).
- Provide a visible focus ring (system-drawn for native controls; custom for custom views).
- Support shortcuts (`Command`, `Return`, `Esc`).

SwiftUI:

```swift
@FocusState private var focus: Field?

TextField("Email", text: $email)
    .focused($focus, equals: .email)
    .onSubmit { focus = .password }
    .submitLabel(.next)

Button("Save", action: save)
    .keyboardShortcut(.defaultAction) // Return
```

UIKit:

```swift
override var canBecomeFirstResponder: Bool { true }

override var keyCommands: [UIKeyCommand]? {
    [
        UIKeyCommand(title: "Close", action: #selector(close), input: UIKeyCommand.inputEscape),
        UIKeyCommand(title: "Save",  action: #selector(save),  input: "\r", modifierFlags: .command),
    ]
}
```

Custom focusable view:

```swift
class CardView: UIView {
    override var canBecomeFocused: Bool { true }
    override func didUpdateFocus(in context: UIFocusUpdateContext, with coordinator: UIFocusAnimationCoordinator) {
        coordinator.addCoordinatedAnimations {
            self.layer.borderWidth = self.isFocused ? 2 : 0
            self.layer.borderColor = UIColor.accent.cgColor
        }
    }
}
```

### 2. Android — Keyboard, D-pad, TV

Every `View` / composable that is interactive must be `focusable`. Traversal order follows the tree unless overridden.

Views:

```xml
<Button
    android:focusable="true"
    android:focusableInTouchMode="false"
    android:nextFocusRight="@id/saveButton"
    android:background="@drawable/btn_selector" />
```

`btn_selector.xml` should include a `state_focused="true"` variant with a clear outline (3:1 contrast).

Compose:

```kotlin
val focusRequester = remember { FocusRequester() }

Button(
    onClick = ::save,
    modifier = Modifier
        .focusRequester(focusRequester)
        .onFocusChanged { state -> /* update visuals */ }
        .focusable()
) { Text("Save") }

// Jump focus
LaunchedEffect(Unit) { focusRequester.requestFocus() }
```

Use `Modifier.focusProperties { next = nextRef; down = downRef }` to customize D-pad order.

Global keyboard shortcuts — override `onKeyShortcut` in the Activity.

### 3. Flutter

Flutter has a full focus + shortcuts system.

```dart
Shortcuts(
  shortcuts: const {
    SingleActivator(LogicalKeyboardKey.keyS, control: true): SaveIntent(),
    SingleActivator(LogicalKeyboardKey.escape): CloseIntent(),
  },
  child: Actions(
    actions: {
      SaveIntent: CallbackAction<SaveIntent>(onInvoke: (_) => _save()),
      CloseIntent: CallbackAction<CloseIntent>(onInvoke: (_) => Navigator.pop(context)),
    },
    child: Focus(
      autofocus: true,
      child: FocusTraversalGroup(
        policy: OrderedTraversalPolicy(),
        child: FormUI(),
      ),
    ),
  ),
)
```

Use `FocusableActionDetector` for custom widgets to get hover / focus states and actions in one place.

### 4. React Native

RN keyboard support varies by platform. On iOS, native components respond to FKA. On Android TV / tvOS, use the `tvOS`/`android-tv` focus system.

```tsx
<Pressable
  focusable
  accessibilityRole="button"
  accessibilityLabel="Save"
  onFocus={() => setFocused(true)}
  onBlur={() => setFocused(false)}
  style={[styles.btn, focused && styles.btnFocused]}
  onPress={save} />
```

For external keyboards on iOS, `Pressable` triggers on Return/Space when focused. Provide `onKeyPress` on `TextInput` to handle Tab / Esc if you intercept them.

### 5. Focus Order

Follow reading order (top-to-bottom, start-to-end). When custom layouts break this:

- SwiftUI: `.accessibilitySortPriority(_:)`.
- UIKit: `accessibilityElements = [...]`.
- Compose: `Modifier.focusProperties { next = ...; previous = ... }` or wrap in `FocusRestorer`.
- Flutter: `FocusTraversalOrder(order: NumericFocusOrder(1.0), child: ...)`.

### 6. Escape and Back

- Every modal/dialog must close on `Esc` (hardware back on Android).
- Loss of the dismiss path is a common bug with custom overlays.

```kotlin
// Compose dialog
if (visible) {
    BackHandler(enabled = true) { onDismiss() }
    Dialog(onDismissRequest = onDismiss) { /* ... */ }
}
```

### 7. Visible Focus Indicator (WCAG 2.4.7)

- Use a ring, not color change alone. Minimum 2dp / 2pt stroke, contrast >= 3:1.
- Do not remove the native focus ring without replacing it.
- Ensure the ring is not clipped by parent `overflow`/`clipsToBounds`.

### 8. Shortcuts

Expose them where users can discover them:

- iOS: long-press Command key shows the shortcuts overlay — register all `UIKeyCommand`s with discoverable titles.
- Android: `Ctrl+/` shows keyboard shortcuts — override `onProvideKeyboardShortcuts`.
- In-app: a help screen listing shortcuts.

### 9. Game Controllers / D-pad

On Android TV and Play Games:

- D-pad events come as `KEYCODE_DPAD_*`. Let the focus system handle them; don't intercept unless necessary.
- Provide A/B button mappings via `onKeyEvent` (KEYCODE_BUTTON_A = primary action, BUTTON_B = back).

### 10. Common Pitfalls

- Custom `TouchableOpacity` / `GestureDetector` with no `focusable` — unreachable by keyboard.
- Modal overlay that traps focus but has no Esc/back dismissal.
- Focus ring removed in favor of a subtle color change that fails 3:1.
- Long forms without `nextFocus` chaining — each field submit dismisses keyboard.
- D-pad skipping over items because a transparent parent steals focus.

## Checklist

- [ ] Every interactive element reachable by Tab / arrow / D-pad.
- [ ] Visible focus ring, >= 3:1 contrast, not clipped.
- [ ] Modals close on Esc / hardware back.
- [ ] Return / Enter activates the default action; Space activates focused button.
- [ ] `Cmd+S` / `Ctrl+S` or equivalent for save-like actions in productivity apps.
- [ ] Focus order matches visual order; overrides where layout diverges.
- [ ] Tested with external Bluetooth keyboard on iOS and Android.
