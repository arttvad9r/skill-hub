---
name: talkback
description: Android TalkBack essentials — semantics, importantForAccessibility, live regions, custom actions, and Jetpack Compose semantics blocks. Use this when building or auditing Android UI for screen-reader users.
---

# TalkBack (Android)

## Instructions

TalkBack is Android's built-in screen reader. It consumes the accessibility tree exposed by views and Compose semantics. Your job is to make that tree correct, minimal, and grouped.

### 1. Content Descriptions (Views)

```kotlin
// Icon button — label describes the action, not the icon.
imageButton.contentDescription = getString(R.string.a11y_delete_message)

// Decorative image — hide it.
decorativeImage.importantForAccessibility =
    View.IMPORTANT_FOR_ACCESSIBILITY_NO

// Container whose children already describe it — don't announce it again.
card.importantForAccessibility =
    View.IMPORTANT_FOR_ACCESSIBILITY_NO_HIDE_DESCENDANTS // only when replacing children
```

Rules:

- Labels describe purpose, not appearance. "Delete message" not "Red trash can".
- Do **not** include the role in the label ("Delete message button") — TalkBack adds that.
- Never put the same information in label *and* children visible to the reader (duplicate announcement).

### 2. Jetpack Compose Semantics

```kotlin
@Composable
fun LikeButton(liked: Boolean, onToggle: () -> Unit) {
    IconButton(
        onClick = onToggle,
        modifier = Modifier.semantics {
            role = Role.Switch
            stateDescription = if (liked) "Liked" else "Not liked"
            onClick(label = "Toggle like") { onToggle(); true }
        }
    ) {
        Icon(
            imageVector = if (liked) Icons.Filled.Favorite else Icons.Outlined.FavoriteBorder,
            contentDescription = null, // parent exposes semantics
        )
    }
}
```

Common semantics properties:

- `contentDescription` — accessible name.
- `stateDescription` — current state ("Liked", "Expanded").
- `role` — `Role.Button`, `Role.Switch`, `Role.Checkbox`, `Role.RadioButton`, `Role.Image`, `Role.Tab`, `Role.DropdownList`.
- `heading()` — marks a header for rotor navigation.
- `selected = true` — for tab / item state.
- `disabled()` — exposes disabled state.
- `liveRegion = LiveRegionMode.Polite` — announce changes.

### 3. Grouping Children

By default Compose merges semantics of a leaf composable's children. Use `Modifier.semantics(mergeDescendants = true) { ... }` on a card to make TalkBack treat it as a single focusable unit.

```kotlin
Row(
    modifier = Modifier
        .clickable(onClick = onClick)
        .semantics(mergeDescendants = true) {
            contentDescription = "$title, $subtitle, $timestamp"
        }
) {
    Avatar(user)
    Column {
        Text(title)
        Text(subtitle)
        Text(timestamp)
    }
}
```

For Views, use `ViewGroup.isScreenReaderFocusable = true` or set `accessibilityTraversalBefore / After` to control order.

### 4. Live Regions

Use live regions for dynamic content that should be announced without stealing focus (validation errors, search result counts, status toasts).

```kotlin
// View
resultCountView.accessibilityLiveRegion =
    View.ACCESSIBILITY_LIVE_REGION_POLITE

// Compose
Text(
    text = "$count results",
    modifier = Modifier.semantics { liveRegion = LiveRegionMode.Polite }
)
```

Polite = announced when TalkBack is idle. Assertive = interrupts the current announcement (use sparingly, e.g., for critical errors).

### 5. Custom Actions

Expose secondary actions without requiring swipe gestures.

```kotlin
// View
ViewCompat.addAccessibilityAction(messageRow, "Archive") { _, _ ->
    archive(); true
}

// Compose
Modifier.semantics {
    customActions = listOf(
        CustomAccessibilityAction("Archive") { archive(); true },
        CustomAccessibilityAction("Report") { report(); true },
    )
}
```

TalkBack users open these via the local context menu (swipe up then right).

### 6. Announcements

Prefer live regions over ad-hoc announcements. When you truly need a one-shot announcement:

```kotlin
view.announceForAccessibility("Message sent")
```

Compose equivalent — use a live region composable or the experimental `LocalAccessibilityManager`.

### 7. Heading and Pane Titles

```kotlin
// View
ViewCompat.setAccessibilityHeading(titleView, true)
ViewCompat.setAccessibilityPaneTitle(rootView, "Inbox")

// Compose
Text("Inbox", modifier = Modifier.semantics { heading() })
```

Pane titles announce when a pane appears (useful for dialogs and shared-element transitions).

### 8. Common Pitfalls

- Setting `contentDescription` on a container **and** its children → double announcement.
- Putting role words in labels ("Settings button").
- Using `Modifier.clickable` without an explicit `onClickLabel` (TalkBack says "double tap to activate" with no verb).
- Hiding loading spinners from TalkBack but leaving them on screen — users don't know the app is busy.
- Forgetting to clear semantics on a recycled view/composable when state changes.

## Checklist

- [ ] Every `clickable`/`IconButton` has a label that states the action.
- [ ] Decorative icons are `null`/`IMPORTANT_FOR_ACCESSIBILITY_NO`.
- [ ] Row/card containers merge children semantics where it improves flow.
- [ ] Dynamic content uses `liveRegion` / `accessibilityLiveRegion`.
- [ ] Custom row actions exposed via `CustomAccessibilityAction`.
- [ ] Headings marked with `heading()` or `setAccessibilityHeading`.
- [ ] Verified on a real device with TalkBack enabled at default and large font scale.
