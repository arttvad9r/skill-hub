---
name: wcag-2-2-for-mobile
description: WCAG 2.2 success criteria translated to mobile platforms — gestures, inputs, orientation, focus, and target size. Use this when scoping accessibility acceptance criteria for a mobile feature.
---

# WCAG 2.2 for Mobile

## Instructions

WCAG 2.2 was written for the web, but every Level A/AA success criterion has a mobile counterpart. Apply the criteria below; deviate only with a documented reason.

### 1. Non-Text Content (1.1.1, Level A)

- Every image, icon button, or visual indicator needs a text alternative.
- Decorative-only content must be hidden from assistive tech.

```swift
// iOS — purely decorative
Image("hero-swirl").accessibilityHidden(true)
```

```kotlin
// Android View
imageView.importantForAccessibility = View.IMPORTANT_FOR_ACCESSIBILITY_NO
```

### 2. Info and Relationships (1.3.1, Level A)

- Headings, lists, and groups must be expressed through semantics, not just visual styling.
- iOS: `.accessibilityAddTraits(.isHeader)`; Compose: `Modifier.semantics { heading() }`; Flutter: `Semantics(header: true)`; RN: `accessibilityRole="header"`.

### 3. Meaningful Sequence (1.3.2, Level A)

Reading order must match the visual/logical order. Override traversal when layouts reorder children (e.g., a floating header rendered after the list in the tree).

```swift
VStack {
    content
}.accessibilityElements(children: .contain)
 .accessibilitySortPriority(1)
```

### 4. Use of Color (1.4.1, Level A)

Color cannot be the only indicator. Pair required-field red with an asterisk and "required"; pair error red with an icon and text.

### 5. Contrast (Minimum) (1.4.3, Level AA)

- Text: 4.5:1 normal, 3:1 large (>= 18pt or 14pt bold).
- Non-text UI and icons: 3:1 (1.4.11).
- Verify in both light and dark themes.

### 6. Resize Text / Text Scaling (1.4.4, Level AA)

Layouts must reflow at 200% text without loss of content or functionality. On mobile this means honoring Dynamic Type / font scale up to the system's largest setting.

```dart
// Flutter — never clamp below 1.0
MediaQuery(
  data: MediaQuery.of(context).copyWith(
    textScaler: MediaQuery.textScalerOf(context).clamp(minScaleFactor: 1.0),
  ),
  child: child,
)
```

### 7. Reflow (1.4.10, Level AA)

Content must work in portrait **and** landscape without requiring two-dimensional scrolling (except for content that inherently requires it: maps, tables).

### 8. Non-Text Contrast (1.4.11, Level AA)

Interactive component boundaries, icon strokes, and focus indicators must meet 3:1 against adjacent colors.

### 9. Keyboard / Hardware Input (2.1.1, Level A)

Every action must be reachable via keyboard, D-pad, or switch. On iOS this means Full Keyboard Access; on Android, D-pad traversal.

### 10. No Keyboard Trap (2.1.2, Level A)

Focus must be able to leave every component, including custom modals. Dismiss must always be reachable.

### 11. Timing Adjustable (2.2.1, Level A)

For auto-dismissing toasts, time-limited forms, or OTP screens: allow extend, pause, or disable — or make the timeout at least 20 hours.

### 12. Three Flashes or Below (2.3.1, Level A)

Animations and video must not flash more than 3 times per second.

### 13. Focus Visible (2.4.7, Level AA)

Hardware keyboard / switch focus must be visually indicated. On iOS this is automatic with Full Keyboard Access; on Android use `android:focusableInTouchMode="false"` + selector drawables with focused state.

### 14. Focus Not Obscured (Minimum) (2.4.11, Level AA — new in 2.2)

When focus moves, the focused element must not be fully hidden behind a sticky header, keyboard, or bottom sheet. Scroll it into view.

```kotlin
// Compose — bring focused element into view
Modifier.bringIntoViewRequester(bringIntoViewRequester)
```

### 15. Target Size (Minimum) (2.5.8, Level AA — new in 2.2)

Pointer targets must be at least **24 CSS px**; on mobile we hold the stricter Apple (44pt) / Material (48dp) baseline. Inline text links are exempt; "essential" targets (e.g., map pins) are exempt.

### 16. Dragging Movements (2.5.7, Level AA — new in 2.2)

Any function that uses dragging must offer a single-pointer alternative. Provide tap buttons for reorder, stepper buttons for sliders.

```tsx
// RN slider with stepper alternatives
<View accessibilityRole="adjustable"
      accessibilityValue={{ min, max, now: value }}
      onAccessibilityAction={(e) => {
        if (e.nativeEvent.actionName === 'increment') setValue(v => v + 1);
        if (e.nativeEvent.actionName === 'decrement') setValue(v => v - 1);
      }}
      accessibilityActions={[{ name: 'increment' }, { name: 'decrement' }]} />
```

### 17. Consistent Help (3.2.6, Level A — new in 2.2)

If you offer contact/help, place it in the same location across screens.

### 18. Accessible Authentication (Minimum) (3.3.8, Level AA — new in 2.2)

Do not rely on cognitive function tests (memorizing, transcribing) with no alternative. Allow password managers (do not disable paste), biometric fallback, or OTP copy.

### 19. Redundant Entry (3.3.7, Level A — new in 2.2)

Don't make users re-enter information they already provided within the same session (e.g., shipping = billing checkbox).

### 20. Status Messages (4.1.3, Level AA)

Non-modal status updates (toasts, inline success/error) must be announced without stealing focus.

```kotlin
// View system
statusView.accessibilityLiveRegion = View.ACCESSIBILITY_LIVE_REGION_POLITE
```

```swift
// iOS
UIAccessibility.post(notification: .announcement, argument: "Saved")
```

## Checklist

- [ ] Contrast verified in light and dark themes (1.4.3 / 1.4.11).
- [ ] Layout reflows at 200% text and in landscape (1.4.4 / 1.4.10).
- [ ] Every drag gesture has a tap/stepper alternative (2.5.7).
- [ ] All targets meet 44pt / 48dp (2.5.8).
- [ ] Focus visible and not obscured by sticky chrome (2.4.7 / 2.4.11).
- [ ] Auth flow supports paste / biometric / OTP copy (3.3.8).
- [ ] Status messages use live regions / announcements (4.1.3).
- [ ] No content flashes more than 3 times/second (2.3.1).
