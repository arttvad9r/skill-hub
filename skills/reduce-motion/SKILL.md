---
name: reduce-motion
description: Detecting and honoring the user's reduce motion preference on iOS, Android, Flutter, and React Native. Use this when building transitions, parallax, hero animations, or autoplay.
---

# Reduce Motion

## Instructions

Some users experience nausea or vertigo from screen motion (vestibular disorders). Every OS ships a system toggle. Honor it for non-essential motion; keep essential feedback (progress indicator).

### 1. Detecting the Setting

**iOS (UIKit):**

```swift
UIAccessibility.isReduceMotionEnabled

NotificationCenter.default.addObserver(
    forName: UIAccessibility.reduceMotionStatusDidChangeNotification,
    object: nil, queue: .main
) { _ in /* update state */ }
```

**iOS (SwiftUI):**

```swift
@Environment(\.accessibilityReduceMotion) private var reduceMotion

.animation(reduceMotion ? nil : .spring(), value: offset)
```

**Android (API 33+):**

```kotlin
val am = context.getSystemService(AccessibilityManager::class.java)
val reduced = am.isEnabled &&
    Settings.Global.getFloat(contentResolver,
        Settings.Global.TRANSITION_ANIMATION_SCALE, 1f) == 0f
```

A simpler heuristic used across libraries:

```kotlin
fun areAnimationsDisabled(context: Context): Boolean {
    return Settings.Global.getFloat(
        context.contentResolver, Settings.Global.ANIMATOR_DURATION_SCALE, 1f
    ) == 0f
}
```

**Jetpack Compose:**

```kotlin
val reduce = LocalAccessibilityManager.current?.run {
    // API 33+: expose via custom CompositionLocal backed by AccessibilityManager
    false
} ?: areAnimationsDisabled(LocalContext.current)

val anim: AnimationSpec<Float> = if (reduce) snap() else spring()
```

**Flutter:**

```dart
final disableAnimations = MediaQuery.disableAnimationsOf(context);

AnimatedContainer(
  duration: disableAnimations ? Duration.zero : const Duration(milliseconds: 300),
  curve: Curves.easeOut,
  // ...
)
```

**React Native:**

```tsx
import { AccessibilityInfo } from 'react-native';

const [reduce, setReduce] = useState(false);
useEffect(() => {
  AccessibilityInfo.isReduceMotionEnabled().then(setReduce);
  const sub = AccessibilityInfo.addEventListener('reduceMotionChanged', setReduce);
  return () => sub.remove();
}, []);
```

Reanimated helper:

```tsx
import { useReducedMotion } from 'react-native-reanimated';
const reduce = useReducedMotion();
```

### 2. What To Disable or Replace

When reduce motion is on:

- **Disable** parallax on cards, hero scroll effects, and decorative wobble.
- **Replace** slide/zoom transitions with **crossfade** (WCAG-compatible, no translation).
- **Shorten** durations — keep timing for feedback (e.g., button press) but prefer < 100ms.
- **Stop autoplaying** video, carousels, and Lottie backgrounds. Provide a play control.
- **Skip** large scale/translate transforms; keep opacity changes.

### 3. Hero / Shared-Element Transitions

SwiftUI example — crossfade fallback:

```swift
if reduceMotion {
    detail.transition(.opacity)
} else {
    detail.transition(.asymmetric(insertion: .move(edge: .trailing),
                                  removal: .opacity))
}
```

Compose:

```kotlin
val enter = if (reduce) fadeIn() else slideInHorizontally() + fadeIn()
AnimatedContent(target = screen, transitionSpec = { enter togetherWith fadeOut() }) { /* ... */ }
```

Flutter navigation:

```dart
MaterialPageRoute(
  builder: (_) => const DetailPage(),
  allowSnapshotting: !disableAnimations,
  // wrap with PageRouteBuilder for fade transition when reduced
)
```

### 4. Skeletons and Loaders

- Replace shimmer/pulse with a static placeholder + a subtle opacity breathe (< 0.2 delta).
- Progress spinners are "essential" motion — keep them. Use `@Environment(\.accessibilityReduceMotion)` to swap large marketing loaders for a plain `ProgressView`.

### 5. Vestibular Red Flags

Avoid, or provide reduce-motion fallback, for:

- Parallax with scroll parallax factor > 0.2.
- Full-screen page-flip or 3D rotation.
- Auto-scrolling carousels (also a WCAG 2.2.2 issue).
- Particle effects, confetti without user trigger.
- Background videos on splash / home.

### 6. Flashing Content

Regardless of the user's preference, never exceed **3 flashes per second** (WCAG 2.3.1). Even one large red flash can trigger photosensitive seizures.

### 7. In-App Override

If your brand requires motion-rich content, add an in-app "Reduce animations" toggle that mirrors the system flag and is also respected by your code path. Default = system value.

### 8. Testing

- iOS: Settings → Accessibility → Motion → Reduce Motion (and separately Prefer Cross-Fade Transitions).
- Android: Developer options → `Window animation scale`, `Transition animation scale`, `Animator duration scale` → Off. Also Settings → Accessibility → *Remove animations* on Android 12+.
- Flutter: `flutter test --platform chrome --dart-define=flutter.inspector.structuredErrors=true` + wrap app with MediaQuery disabling animations.
- RN: Jest + mock `AccessibilityInfo.isReduceMotionEnabled`.

### 9. Common Pitfalls

- Applying reduce-motion only to one animation out of ten.
- Shortening duration but keeping 300px translate — still nauseating.
- Using a third-party animation lib that ignores the flag; check its docs.
- Replacing animation with a pop (instant change) when crossfade would feel less jarring.
- Autoplay carousels with no pause control.

## Checklist

- [ ] Reduce-motion flag read once, exposed app-wide (env/provider/hook).
- [ ] All non-essential transitions degrade to crossfade or instant.
- [ ] Parallax, wobble, and decorative motion disabled when flag is on.
- [ ] Autoplay video / carousels offer pause and respect the flag.
- [ ] No content flashes > 3x/sec in any 1s window.
- [ ] In-app toggle mirrors system setting (optional but recommended).
- [ ] Tested with reduce motion on, animator scale 0, and Flutter `disableAnimations`.
