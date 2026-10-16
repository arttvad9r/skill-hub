---
name: dark-mode-a11y
description: Accessibility pitfalls specific to dark themes — contrast, elevation, pure black, and system overrides. Use this when designing dark theme palettes or auditing parity between themes.
---

# Dark Mode Accessibility

## Instructions

Dark mode is not "invert the light palette". It has its own contrast, elevation, and perception rules. Audit both themes with the same rigor.

### 1. Avoid Pure Black Backgrounds

- Pure `#000000` with pure `#FFFFFF` text causes halation (glow) for astigmatism users and after-images at high brightness.
- Material recommends `#121212` as the base dark surface. Apple system background in dark is `#1C1C1E` / `#000` on OLED only for certain surfaces.
- Reserve true black for system chrome (status bar background merges with OLED) — not for content.

### 2. Contrast Still Applies

Re-run WCAG contrast checks in dark mode. Do not assume parity.

```swift
// SwiftUI — named asset with light + dark variants
Text("Heading").foregroundStyle(Color("TextPrimary"))
```

```kotlin
// Compose — use MaterialTheme tokens, don't hardcode
Text("Heading", color = MaterialTheme.colorScheme.onSurface)
```

```dart
Text('Heading', style: TextStyle(color: Theme.of(context).colorScheme.onSurface));
```

Add unit tests that verify both light and dark token pairs meet 4.5:1 / 3:1.

### 3. Elevation via Lightness, Not Shadow

In dark themes, shadows disappear. Material 3 conveys elevation by tinting surfaces lighter (surface container levels). Make sure each elevation step maintains 3:1 boundary contrast against its parent.

```kotlin
Surface(tonalElevation = 3.dp) { /* stands out in dark */ }
```

### 4. Brand Accent Colors

Many brand accents (saturated reds, blues) that work on white fail 4.5:1 on dark `#121212`. Provide a brighter "on dark" variant:

```xml
<!-- colors.xml -->
<color name="brand_primary_light">#1E88E5</color>
<color name="brand_primary_dark">#82B1FF</color>
```

Material tooling (HCT / tone) can generate compliant variants automatically.

### 5. Images and Illustrations

- Avoid transparent PNGs designed for white backgrounds — they become low-contrast silhouettes on dark.
- Provide dark-mode asset variants (`Assets.xcassets` appearance "Any/Dark", Android `drawable-night/`).
- SVG/vector illustrations: parameterize fill colors via theme tokens.

### 6. Code Blocks, Charts, Data Viz

- Re-pick chart palettes for dark mode; bright saturated colors clash.
- Keep syntax-highlight themes at 4.5:1 for every token color, not only the default text.
- Grid lines should use `onSurface.withAlpha(0.12)`–`0.24` — enough to read but not distract.

### 7. Honor System Overrides

- iOS "Increase Contrast" → `UIAccessibility.isDarkerSystemColorsEnabled` (env `\.colorSchemeContrast`). Provide higher-contrast token variants.

```swift
@Environment(\.colorSchemeContrast) private var contrast

var textColor: Color {
    contrast == .increased ? Color("TextPrimaryHC") : Color("TextPrimary")
}
```

- Android "High contrast text" → system draws an outline around text; avoid custom shadows that conflict.
- Do **not** force a theme. Respect the user's system setting unless you also offer an in-app override.

### 8. Selection and Focus Indicators

Focus rings that worked on light often vanish on dark. Use the accent with increased alpha or a lighter shade:

```kotlin
val focusColor = if (isSystemInDarkTheme())
    MaterialTheme.colorScheme.primary.copy(alpha = 1f)
else
    MaterialTheme.colorScheme.primary
```

### 9. Status Bar / System Bar Contrast

- iOS: set `preferredStatusBarStyle` / SwiftUI `statusBarHidden(false)` + `toolbarColorScheme(.dark/.light, for: .statusBar)`.
- Android: use `WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = !darkTheme`.
- RN: `<StatusBar barStyle={darkTheme ? 'light-content' : 'dark-content'} />`.
- Flutter: `SystemChrome.setSystemUIOverlayStyle(...)` matched to theme.

### 10. Common Pitfalls

- Shipping one theme and scaling opacity to fake the other.
- Using `MaterialTheme.colorScheme.onSurface` in light + `Color.White` in dark (inconsistency) — always go via tokens.
- OLED "true black" mode with white text on a dimmed display — halation.
- Dark-mode previews missing from component libraries.
- Brand red errors on dark surface failing 4.5:1.

## Checklist

- [ ] Base dark surface is not pure `#000` for long-form content.
- [ ] All text / icon contrast verified in dark theme, including brand accents.
- [ ] Elevation uses tonal surfaces, boundaries readable at 3:1.
- [ ] Image/illustration assets have dark variants.
- [ ] `colorSchemeContrast` / Increase Contrast honored with higher-contrast tokens.
- [ ] Focus/selection indicators remain visible in dark.
- [ ] Status bar icon color matches theme.
- [ ] Component previews include both themes.
