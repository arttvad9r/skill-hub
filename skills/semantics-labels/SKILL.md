---
name: semantics-labels
description: Cross-platform semantics — labels, roles, values, and states across iOS, Android, Flutter, and React Native. Use this to keep screen-reader behavior consistent across platforms.
---

# Semantics and Labels (Cross-Platform)

## Instructions

Screen readers consume four pieces of metadata for each element: **label, role, value, state**. Each platform names them differently; this skill maps them so you stay consistent.

### 1. The Four Pieces

| Concept | iOS (SwiftUI / UIKit) | Android (Compose / View) | Flutter | React Native |
|---|---|---|---|---|
| Label | `.accessibilityLabel` / `accessibilityLabel` | `contentDescription` | `Semantics(label:)` | `accessibilityLabel` |
| Role  | `.accessibilityAddTraits` / `accessibilityTraits` | `semantics { role = Role.X }` / `setAccessibilityDelegate` | `Semantics(button:/header:/image:)` | `accessibilityRole` |
| Value | `.accessibilityValue` / `accessibilityValue` | `stateDescription` / `AccessibilityNodeInfo.setText` | `Semantics(value:)` | `accessibilityValue` |
| State | traits: `.isSelected`, `.isAdjustable` | `selected = true`, `disabled()` | `Semantics(selected:, enabled:, toggled:)` | `accessibilityState={{ selected, disabled, checked }}` |

### 2. Labels — Rules That Hold Everywhere

- Describe **purpose**, not appearance. "Delete" not "Red trash icon".
- Do **not** include the role ("Delete button") — the platform announces the role.
- Keep it short; put extra context in hint / `accessibilityHint` / `Semantics(hint:)`.
- Localize every label. Never ship English strings in a localized app.

### 3. Example: Same Button on Four Platforms

SwiftUI:

```swift
Button(action: delete) { Image(systemName: "trash") }
    .accessibilityLabel("Delete")
    .accessibilityHint("Removes the selected message")
```

Jetpack Compose:

```kotlin
IconButton(
    onClick = ::delete,
    modifier = Modifier.semantics {
        role = Role.Button
        onClick(label = stringResource(R.string.a11y_delete)) { delete(); true }
    }
) { Icon(Icons.Outlined.Delete, contentDescription = null) }
```

Flutter:

```dart
Semantics(
  button: true,
  label: 'Delete',
  hint: 'Removes the selected message',
  onTap: _delete,
  child: IconButton(icon: const Icon(Icons.delete_outline), onPressed: _delete),
)
```

React Native:

```tsx
<Pressable
  accessibilityRole="button"
  accessibilityLabel="Delete"
  accessibilityHint="Removes the selected message"
  onPress={onDelete}>
  <TrashIcon />
</Pressable>
```

### 4. Stateful Controls (toggle, checkbox, tab)

Always expose current state as *value* or via a state flag. Do not bake it into the label ("Dark mode On") because the user cannot tell when it changes.

SwiftUI:

```swift
.accessibilityLabel("Dark mode")
.accessibilityValue(isOn ? "On" : "Off")
.accessibilityAddTraits(isOn ? [.isButton, .isSelected] : .isButton)
```

Compose:

```kotlin
Modifier.semantics {
    role = Role.Switch
    stateDescription = if (isOn) "On" else "Off"
    toggleableState = if (isOn) ToggleableState.On else ToggleableState.Off
}
```

Flutter:

```dart
Semantics(toggled: isOn, label: 'Dark mode', child: switchWidget);
```

React Native:

```tsx
<Pressable
  accessibilityRole="switch"
  accessibilityLabel="Dark mode"
  accessibilityState={{ checked: isOn }}
  onPress={toggle} />
```

### 5. Grouping Cells

Aim for **one focus stop per semantic unit** (row, card, list item). Read out the full content; expose row actions via platform action APIs.

SwiftUI: `.accessibilityElement(children: .combine)` + `.accessibilityAction(named:)`.

Compose: `Modifier.semantics(mergeDescendants = true) { contentDescription = "..."; customActions = [...] }`.

Flutter: `Semantics(container: true, child: MergeSemantics(child: ...))`.

RN: `accessible={true}` on the row + `accessibilityActions` + `onAccessibilityAction`.

### 6. Headings and Landmarks

Marking section headings enables rotor / heading navigation.

```swift
Text("Inbox").accessibilityAddTraits(.isHeader)
```

```kotlin
Text("Inbox", modifier = Modifier.semantics { heading() })
```

```dart
Semantics(header: true, child: Text('Inbox'));
```

```tsx
<Text accessibilityRole="header">Inbox</Text>
```

### 7. Hidden and Decorative

Hide anything that does not add information.

| Platform | Hide subtree |
|---|---|
| SwiftUI | `.accessibilityHidden(true)` |
| UIKit | `isAccessibilityElement = false` + `accessibilityElementsHidden = true` |
| Compose | `Modifier.clearAndSetSemantics { }` or `semantics { invisibleToUser() }` |
| View | `importantForAccessibility = IMPORTANT_FOR_ACCESSIBILITY_NO` |
| Flutter | `ExcludeSemantics(child: ...)` |
| RN | `accessibilityElementsHidden={true}` (iOS) + `importantForAccessibility="no-hide-descendants"` (Android) |

### 8. Localization

- Put every label in string resources (`Localizable.strings`, `strings.xml`, `arb`, `i18n` JSON).
- Never concatenate translated fragments to form a label — sentence order differs by locale.
- Include contextual notes for translators ("Used as icon label for a delete action").

### 9. Common Pitfalls

- One label on container **and** on children → double announcement.
- Using the same label for multiple items on screen (e.g., every row labeled "Row").
- Putting state in the label instead of the value → changes are silent.
- Forgetting to expose role on custom `TouchableOpacity` / `GestureDetector`.
- Relying on `accessibilityHint` for required info — the user may have hints off.

## Checklist

- [ ] Every interactive element exposes label + role.
- [ ] Stateful controls expose current state via value/state, not label.
- [ ] Decorative content is hidden with the platform's exclude API.
- [ ] List items group to a single focus stop with custom actions for secondary gestures.
- [ ] Headings marked so rotor navigation works.
- [ ] All labels localized and reviewed by translators with context.
