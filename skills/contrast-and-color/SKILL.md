---
name: contrast-and-color
description: WCAG contrast ratios, non-text contrast, and color-blind-safe patterns for mobile UI. Use this when designing palettes, tokens, or auditing a screen for color accessibility.
---

# Contrast and Color

## Instructions

Contrast failures are the single most common accessibility bug in mobile apps. Treat color decisions as engineering decisions with measurable acceptance criteria.

### 1. Contrast Ratios (WCAG 2.2 AA)

| Content | Minimum ratio |
|---|---|
| Body text (< 18pt regular, < 14pt bold) | **4.5:1** |
| Large text (>= 18pt regular or >= 14pt bold) | **3:1** |
| Icon / graphical UI component | **3:1** (1.4.11) |
| Focus indicator outline | **3:1** vs adjacent colors |
| Disabled states | Exempt from 1.4.3 but still should aim for 3:1 where possible |

For AAA (optional), raise body text to 7:1 and large text to 4.5:1.

### 2. Measuring Contrast at the Token Level

Do the math once, at the design-token layer; do not eyeball it per screen.

```kotlin
// utility — WCAG relative luminance
fun luminance(c: Color): Double {
    fun ch(x: Float): Double {
        val v = x.toDouble()
        return if (v <= 0.03928) v / 12.92 else Math.pow((v + 0.055) / 1.055, 2.4)
    }
    return 0.2126 * ch(c.red) + 0.7152 * ch(c.green) + 0.0722 * ch(c.blue)
}

fun contrast(a: Color, b: Color): Double {
    val la = luminance(a); val lb = luminance(b)
    val (hi, lo) = if (la > lb) la to lb else lb to la
    return (hi + 0.05) / (lo + 0.05)
}

require(contrast(Tokens.onSurface, Tokens.surface) >= 4.5)
```

Add a unit test that fails if a token pair drops below threshold.

### 3. Do Not Rely on Color Alone (WCAG 1.4.1)

Pair color with a second cue:

- Form errors → red border **and** error icon **and** text.
- Required fields → asterisk *with* the text "required" (visually hidden or in label).
- Status chips → color **and** icon (check / warn / info).
- Graphs → color **and** pattern (dash, dots) **and** direct labels.

SwiftUI status chip:

```swift
Label {
    Text("Payment failed")
} icon: {
    Image(systemName: "exclamationmark.octagon.fill")
}
.foregroundStyle(.red)
.accessibilityLabel("Error. Payment failed.")
```

### 4. Color-Blind-Safe Palettes

Roughly 1 in 12 men and 1 in 200 women have some color vision deficiency (CVD). The three concerns:

- **Red/green** (protanopia, deuteranopia) — most common. Never rely on red-vs-green alone (profit vs loss, pass vs fail).
- **Blue/yellow** (tritanopia) — rarer.
- **Full achromatopsia** — treat the UI as if it were grayscale.

Safe strategies:

- Differentiate by **hue + lightness + icon/pattern**, not hue alone.
- Prefer palettes with monotonic luminance (e.g., ColorBrewer qualitative / sequential).
- Validate with simulators (Sim Daltonism, Chrome DevTools Rendering panel).

### 5. Disabled and Placeholder Text

Low-contrast disabled text is tempting visually but confuses everyone.

- Keep disabled text at >= 3:1 where possible.
- Use a secondary cue (icon, "(disabled)" suffix in a11y label) so users relying on AT know.
- Placeholder text is **not** a substitute for a label. And it must meet contrast too.

### 6. Focus and Selection Indicators (1.4.11 / 2.4.11)

Focus outlines, selection highlights, and progress bars must contrast 3:1 against the surrounding color — in **both** themes.

```swift
// SwiftUI
.overlay(
    RoundedRectangle(cornerRadius: 8)
        .stroke(isFocused ? Color.accentColor : .clear, lineWidth: 2)
)
```

```kotlin
// Compose
Modifier.border(
    width = 2.dp,
    color = if (isFocused) MaterialTheme.colorScheme.primary else Color.Transparent,
    shape = RoundedCornerShape(8.dp)
)
```

### 7. Dark Mode Pitfalls

- Pure `#000` backgrounds with pure `#FFF` text create "halation" for astigmatism users. Prefer `#121212` with `#E6E6E6`.
- Elevation shifts must still provide 3:1 boundary contrast.
- Verify brand accent colors in dark; many fail 3:1 against `#121212`.

### 8. High Contrast System Settings

Honor user overrides:

- iOS: `UIAccessibility.isDarkerSystemColorsEnabled` (Increase Contrast). Provide a higher-contrast variant of your token set.
- Android: `Settings.Secure.high_text_contrast_enabled` — rendered automatically by the system for text, but still test custom drawables.

```swift
@Environment(\.accessibilityShowButtonShapes) private var showButtonShapes
// render bordered buttons when true
```

### 9. Tools

- **Stark**, **Figma Contrast**, **Able** plugins at design time.
- **Accessibility Inspector** (macOS) → Audit tab → contrast warnings.
- **Accessibility Scanner** (Android) flags low-contrast views.
- **Chrome DevTools Rendering** — simulate CVD when viewing mobile web views.
- Token-level unit tests (see §2).

### 10. Common Pitfalls

- Hero marketing screens with light text on photo backgrounds — add a scrim or read-gradient.
- Gradients crossing contrast thresholds mid-element — sample at the text bounding box, not the average.
- Gray-on-gray secondary metadata that fails at 4.5:1.
- Focus rings removed for "aesthetics".
- Using `Color.red` semantic meaning without a non-color backup.

## Checklist

- [ ] Token pairs verified at 4.5:1 / 3:1 via automated test.
- [ ] No info conveyed by color alone.
- [ ] Disabled states still readable or clearly marked in AT.
- [ ] Focus indicators meet 3:1 in light and dark themes.
- [ ] Dark-mode palette avoids pure black + pure white.
- [ ] CVD simulation passes for critical flows (checkout, error states, charts).
- [ ] High-contrast system toggle tested on iOS and Android.
