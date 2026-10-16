---
name: rtl-support
description: Right-to-left (RTL) layout mirroring, bidirectional text, numerals, and accessibility implications on iOS, Android, Flutter, and React Native. Use this when supporting Arabic, Hebrew, Urdu, or Farsi locales.
---

# RTL Support

## Instructions

RTL isn't "flip everything horizontally". It's an i18n + a11y concern touching layout, gestures, icons, numerals, and screen-reader reading order.

### 1. Use Logical (Start/End), Not Physical (Left/Right)

iOS — use leading/trailing, never left/right:

```swift
HStack {
    Image(systemName: "chevron.forward") // auto-mirrors
    Text("Settings")
}
.padding(.leading, 16)   // flips in RTL
```

Android Views — `paddingStart` / `marginStart`, not `paddingLeft`:

```xml
<TextView
    android:paddingStart="16dp"
    android:paddingEnd="8dp"
    android:drawableStart="@drawable/ic_lock"
    android:layoutDirection="locale" />
```

Enable at manifest level:

```xml
<application android:supportsRtl="true" ... />
```

Compose:

```kotlin
Row(modifier = Modifier.padding(start = 16.dp, end = 8.dp)) { /* ... */ }
// Compose uses LayoutDirection from the system; Modifier.padding(start=...) flips correctly.
```

Flutter:

```dart
Padding(
  padding: const EdgeInsetsDirectional.only(start: 16, end: 8),
  child: Row(children: [BackIcon(), Text('Settings')]),
)
```

Use `EdgeInsetsDirectional` and `AlignmentDirectional`, not `EdgeInsets` with `left`/`right` values.

React Native — use `start`/`end`:

```tsx
<View style={{ paddingStart: 16, paddingEnd: 8, flexDirection: 'row' }} />
```

Enable at runtime:

```tsx
import { I18nManager } from 'react-native';
I18nManager.forceRTL(true); // persists; reload required
```

### 2. Icons That Mirror vs Don't

Mirror (direction-indicating):

- Back arrow, forward chevron.
- Undo/redo.
- Progress bars, stepper indicators.
- Reply / reply-all / forward.
- Breadcrumbs.

Do **not** mirror (semantic, direction-agnostic):

- Play / pause / stop.
- Camera, phone, check, close.
- Clocks, media progress (time flows the same).
- Charts with universal X-axis conventions.

Platform guidance:

- iOS SF Symbols: use `.forward` / `.backward` variants which auto-mirror.
- Android vector drawables: `android:autoMirrored="true"`.
- Flutter: `Icon(Icons.arrow_back)` auto-mirrors in RTL; custom icons use `Directionality.of(context)` to flip.
- RN: wrap custom icons in `<View style={{ transform: [{ scaleX: I18nManager.isRTL ? -1 : 1 }] }}>` only when semantically correct.

### 3. Text Alignment

- Default to **start** alignment; right-align only for numeric columns and timestamps where it aids scanning.
- Mixed LTR content inside an RTL string (names, URLs) should use Unicode bidi marks (`\u200F` RLM, `\u200E` LRM) if rendering breaks.

### 4. Numerals and Dates

- Arabic locales may use Eastern Arabic digits (٠-٩); Hebrew uses Western digits. Respect the locale.
- Use platform formatters:

```swift
// iOS
let f = NumberFormatter(); f.locale = Locale(identifier: "ar"); f.string(from: 1234)
```

```kotlin
NumberFormat.getInstance(Locale("ar")).format(1234)
```

```dart
NumberFormat.decimalPattern('ar').format(1234);
```

- Do not hard-code digit characters in code.

### 5. Phone Numbers, URLs, Times

- Always treat these as LTR within an RTL paragraph. Wrap with LRM (`\u200E`) or use `Directionality(textDirection: TextDirection.ltr, child: ...)` in Flutter, `<bdi>` semantics equivalent in others.

### 6. Reading Order for AT

Screen readers in RTL swipe right-to-left. Your tree order stays the same in code; only the visual and AT traversal flip. If you use manual `accessibilityElements` / `sortKey`, double-check traversal in RTL screenshots.

- iOS: VoiceOver's swipe direction flips automatically.
- Android: TalkBack reads start-to-end, which is right-to-left in RTL.
- Validate with explicit RTL emulator locale.

### 7. Gestures

- Swipe-to-dismiss and swipe-to-archive flip sides. Preserve "primary action on trailing edge".
- Edge back-swipe (iOS) works on either edge automatically; custom swipes must honor `layoutDirection`.

### 8. Images and Media

- Screenshots marketing illustrations often contain chrome (UI in English) — prepare RTL variants or avoid baking UI into images.
- Charts with directional progression (left → right growth) need mirroring or a legend clarifying direction.

### 9. Testing

- Force RTL without changing language: iOS `UIView.appearance().semanticContentAttribute = .forceRightToLeft`, Android developer options → "Force RTL layout direction", RN `I18nManager.forceRTL(true)`, Flutter `MaterialApp(locale: const Locale('ar'))` + pseudo-locale.
- Enable Arabic test locale with pseudo-translations ("[!! العربية text !!]") to surface hard-coded strings.
- Run the full audit suite (see `manual-a11y-audit`) in RTL mode at least once per release.

### 10. Accessibility Implications

- Labels concatenated from LTR fragments ("Delete" + " " + item name) may read in the wrong order. Prefer a single localized format string with placeholders.
- Icon button labels that assume left/right direction ("Next" icon labeled "Right arrow") must change label too.
- Focus order following visual order in RTL: ensure custom `sortPriority` / `traversalIndex` doesn't assume LTR.

### 11. Common Pitfalls

- Using `padding(.left, ...)` or `marginLeft` — never flips.
- Custom drawables without `autoMirrored="true"`.
- Back arrow that doesn't mirror (users assume the button goes "back" in their reading direction).
- Hard-coded digit characters.
- Text alignment `textAlign: TextAlign.left` — breaks in RTL; use `TextAlign.start`.
- Toast / snackbar with fixed `Alignment.bottomLeft`.
- Strings built by concatenation: `"Hello, " + name + "!"` — use templated resources.

## Checklist

- [ ] All padding/margin/alignment use start/end, not left/right.
- [ ] Directional icons mirror; semantic icons don't.
- [ ] Back / forward / reply chevrons flip automatically.
- [ ] Numerals and dates formatted via locale-aware APIs.
- [ ] Phone, URL, time strings wrapped LTR inside RTL paragraphs.
- [ ] Screen reader traversal verified in RTL emulator.
- [ ] Full a11y audit executed in at least one RTL locale.
- [ ] Localized strings use placeholders, not concatenation.
