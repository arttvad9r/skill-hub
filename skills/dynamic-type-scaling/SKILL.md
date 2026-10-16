---
name: dynamic-type-scaling
description: Honoring user font-scale preferences on iOS, Android (Views and Compose), Flutter, and React Native. Use this when building text-heavy screens or component libraries.
---

# Dynamic Type and Font Scaling

## Instructions

Users can set their system font 1.5–2x larger than default. Apps that clamp or ignore this scale are the #1 source of real-world accessibility complaints.

### 1. iOS — Dynamic Type

Use text styles, not point sizes.

UIKit:

```swift
let label = UILabel()
label.font = UIFont.preferredFont(forTextStyle: .body)
label.adjustsFontForContentSizeCategory = true
label.numberOfLines = 0
```

SwiftUI:

```swift
Text("Welcome")
    .font(.title2)
    .dynamicTypeSize(.small ... .accessibility5) // cap only if truly necessary
```

- Prefer `.body`, `.headline`, `.callout`, `.footnote` over `.system(size:)`.
- `adjustsFontForContentSizeCategory = true` on every label, text field, button title.
- Use `UIFontMetrics(forTextStyle:).scaledValue(for:)` for layout metrics that should scale too (icon size, row height).

### 2. Android Views — `sp`

- All text sizes in `sp` (scale-independent pixels), all other dimensions in `dp`.
- Never use `px` for text. Never use `dp` for text except inside a WebView or Canvas where scaling is applied manually.

```xml
<TextView
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:text="@string/welcome"
    android:textAppearance="?attr/textAppearanceBodyLarge" />
```

- Prefer Material type scale (`?attr/textAppearanceBodyLarge`, `titleMedium`, etc.) so sizes come from the theme.

### 3. Jetpack Compose — `fontScale`

Compose text already scales with `LocalDensity.fontScale`. Don't fight it.

```kotlin
Text(
    text = "Welcome",
    style = MaterialTheme.typography.titleLarge,
)
```

If you accept a `TextUnit`, use `sp`:

```kotlin
Text("Subtitle", fontSize = 14.sp) // NOT .dp
```

To test different scales:

```kotlin
CompositionLocalProvider(LocalDensity provides Density(
    density = LocalDensity.current.density,
    fontScale = 1.5f
)) { App() }
```

Preview helper:

```kotlin
@Preview(fontScale = 1.5f, showBackground = true)
@Composable fun PreviewLargeFont() { /* ... */ }
```

### 4. Flutter — `TextScaler`

Flutter 3.16+ uses `TextScaler` (replacing deprecated `textScaleFactor`).

```dart
final scaler = MediaQuery.textScalerOf(context);
final scaled = scaler.scale(16.0); // use for icon sizes, row heights

Text(
  'Welcome',
  style: Theme.of(context).textTheme.titleLarge, // scales automatically
)
```

Never force `TextScaler.linear(1.0)` globally. If you must clamp:

```dart
MediaQuery(
  data: MediaQuery.of(context).copyWith(
    textScaler: MediaQuery.textScalerOf(context)
        .clamp(minScaleFactor: 1.0, maxScaleFactor: 1.8),
  ),
  child: child,
)
```

Wrap long strings in `Flexible`/`Expanded` so they wrap instead of overflow.

### 5. React Native — `allowFontScaling`

Default is `true` — keep it.

```tsx
<Text style={{ fontSize: 16, lineHeight: 22 }}>
  Welcome
</Text>
```

Never do:

```tsx
<Text allowFontScaling={false}>Welcome</Text>   // BAD globally
Text.defaultProps = { allowFontScaling: false } // BAD globally
```

If you must cap (e.g., for pixel-perfect brand headers):

```tsx
<Text maxFontSizeMultiplier={1.8}>Brand headline</Text>
```

For icons inside buttons, scale manually using `PixelRatio.getFontScale()`:

```tsx
import { PixelRatio } from 'react-native';
const iconSize = 20 * Math.min(PixelRatio.getFontScale(), 1.8);
```

### 6. Layout Rules for Scalable Text

- Never fix a text container's height in `dp`/`pt`/`px`. Use `wrap_content` / intrinsic size.
- Use `minimumScaleFactor` sparingly — shrinking text fails WCAG 1.4.4.
- Prefer vertical stacking over horizontal for label-value pairs when font scale > 1.3.
- Truncating is acceptable only for preview text that has a "see more" affordance.

### 7. Testing Large Sizes

- iOS Simulator: Features → Toggle Accessibility Inspector → Dynamic Type slider; or Settings → Accessibility → Display & Text Size → Larger Text.
- Android Emulator: Settings → Display → Display size and text → Font size (largest). Also test *Display size* (density scaling).
- Flutter: wrap root with `MediaQuery(..., textScaler: TextScaler.linear(2.0))` in a debug build.
- RN: enable system large text; also write Jest snapshot with `PixelRatio` mocked.

### 8. Common Pitfalls

- Clamping font scale to 1.0 "because the design breaks". Fix the design.
- Using `fontSize` for numerical metrics (avatar diameter) — use text-style-relative sizing.
- `SingleLine = true` on labels that contain translated content — truncation.
- Hard-coded row heights in lists; switch to intrinsic + `padding`.
- Passing `dp` or `px` to a `TextView` via code.

## Checklist

- [ ] All text uses scaled units (`sp`, `.preferredFont`, `TextScaler`, RN default).
- [ ] No `allowFontScaling={false}` globally; caps justified per-case.
- [ ] Screens tested at largest accessible Dynamic Type / font scale.
- [ ] Icons and row heights scale proportionally where appropriate.
- [ ] No horizontal clipping / truncation of essential content at 200%.
- [ ] Previews / snapshots exist at an enlarged font scale (1.5x+).
