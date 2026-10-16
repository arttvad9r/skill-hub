---
name: touch-targets
description: Minimum touch-target sizes, hit-slop, and spacing on iOS, Android, Flutter, and React Native. Use this when designing icon buttons, toolbars, list actions, or anything smaller than a full-width row.
---

# Touch Targets

## Instructions

Controls that are too small or too close together fail motor-impaired users and anyone on the move. Platform minimums are non-negotiable.

### 1. Minimums

| Platform | Minimum |
|---|---|
| iOS (HIG) | **44 × 44 pt** |
| Android (Material) | **48 × 48 dp** |
| WCAG 2.2 (2.5.8 AA) | 24 CSS px minimum — mobile holds the stricter platform baseline |

Spacing between adjacent targets: **>= 8 pt / dp** to prevent mis-taps.

### 2. Make the Hit Area Larger Than the Visual

The icon can be 20–24 pt; the *tappable area* must be 44/48.

SwiftUI:

```swift
Button(action: delete) {
    Image(systemName: "trash")
        .font(.system(size: 20))
        .frame(width: 44, height: 44)    // enlarged hit area
        .contentShape(Rectangle())
}
```

UIKit:

```swift
// Increase hit area without changing visual bounds
extension UIButton {
    override open func point(inside p: CGPoint, with e: UIEvent?) -> Bool {
        bounds.insetBy(dx: -10, dy: -10).contains(p)
    }
}
```

### 3. Android — Views and Compose

Views:

```xml
<ImageButton
    android:layout_width="48dp"
    android:layout_height="48dp"
    android:background="?attr/selectableItemBackgroundBorderless"
    android:src="@drawable/ic_trash"
    android:contentDescription="@string/a11y_delete" />
```

Also enable minimum target enforcement (Android 12+):

```kotlin
button.minimumWidth = resources.getDimensionPixelSize(R.dimen.a11y_target_min)
button.minimumHeight = resources.getDimensionPixelSize(R.dimen.a11y_target_min)
```

Compose:

```kotlin
IconButton(
    onClick = ::delete,
    modifier = Modifier.minimumInteractiveComponentSize() // 48dp guaranteed
) {
    Icon(Icons.Outlined.Delete, contentDescription = stringResource(R.string.a11y_delete))
}
```

`IconButton`, `Checkbox`, `RadioButton`, etc. in Material3 already enforce 48dp via `LocalMinimumInteractiveComponentSize`. Don't disable it.

### 4. Flutter

`IconButton` defaults to 48dp. For custom widgets, use `BoxConstraints` and `MaterialTapTargetSize`:

```dart
IconButton(
  icon: const Icon(Icons.delete_outline),
  tooltip: 'Delete',
  onPressed: _delete,
  constraints: const BoxConstraints.tightFor(width: 48, height: 48),
)

// Or globally
ThemeData(materialTapTargetSize: MaterialTapTargetSize.padded)
```

For `GestureDetector`, wrap or pad to 48:

```dart
GestureDetector(
  onTap: _handle,
  behavior: HitTestBehavior.opaque,
  child: SizedBox(width: 48, height: 48, child: Center(child: icon)),
)
```

### 5. React Native

```tsx
<Pressable
  accessibilityRole="button"
  accessibilityLabel="Delete"
  onPress={onDelete}
  hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
  style={{ width: 44, height: 44, alignItems: 'center', justifyContent: 'center' }}>
  <TrashIcon size={20} />
</Pressable>
```

- `hitSlop` extends the tappable area without changing layout.
- Still give the view a 44pt frame so focus rings and ripples make sense.

### 6. Spacing in Toolbars / Row Actions

Aim for **>= 8pt** gap between adjacent targets. If icons are shoulder-to-shoulder, either:

- Increase padding between them, or
- Collapse into an overflow menu.

Swipe-action row (iOS list):

```swift
.swipeActions(edge: .trailing) {
    Button("Delete", role: .destructive) { delete() }
    Button("Archive") { archive() }
}
```

These are ergonomic, but *also* expose the same actions via `.accessibilityAction(named:)` so AT and motor-impaired users without gestures can reach them.

### 7. Exceptions

WCAG 2.5.8 exempts:

- Inline text links within sentences.
- Targets whose size is determined by the user-agent (native map pins, rendered-only-at-zoom items).
- Essential targets (small map clusters when spacing them out would change meaning).

Even for exceptions, provide a way to activate them via a larger alternative (tap and show a picker, zoom to disambiguate).

### 8. Testing

- Android Accessibility Scanner flags touch targets under 48dp.
- Xcode Accessibility Inspector → Audit reports "Hit area is too small".
- Manually test with a stylus and with a fingertip.
- Verify at scale factor 1.5 where text/icon may grow but hit area stays fixed.

### 9. Common Pitfalls

- `Image` with a tap gesture but no padding/frame — 24pt icon = too small.
- Chip rows at 32dp height.
- Close ("×") button in a modal at 24 × 24.
- Bottom sheet grabber with tiny tap area.
- Segmented controls squeezed into < 40dp height.

## Checklist

- [ ] All icon buttons measured at >= 44pt / 48dp frame.
- [ ] Adjacent targets separated by >= 8pt gap.
- [ ] `hitSlop` / `minimumInteractiveComponentSize` used where the visual is smaller.
- [ ] Close, dismiss, and destructive buttons meet minimums even in compact toolbars.
- [ ] Swipe-only actions duplicated in an accessible menu.
- [ ] Scanner / Inspector audit clean for target-size warnings.
