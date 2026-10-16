---
name: automated-a11y-tools
description: Automated accessibility tooling — Accessibility Scanner (Android), Accessibility Inspector + XCUIAccessibilityAudit (iOS), axe-core Flutter and RN, Espresso a11y checks. Use this to wire a11y checks into CI.
---

# Automated Accessibility Tools

## Instructions

Automated tools catch maybe 30% of real accessibility issues — but that 30% is the cheapest to fix, and catching regressions in CI is priceless. Run them on every PR.

### 1. Android — Accessibility Scanner

A Google-published Play Store app that audits any screen you capture. Good for manual QA.

```text
Install: Play Store → "Accessibility Scanner"
Run:     Enable in Settings → Accessibility → Installed apps → Scanner
         Tap the floating ✓ button, then Scan, Record, or Snapshot.
```

Flags: touch-target size, contrast, content descriptions, duplicate labels, redundant text.

### 2. Android — Espresso AccessibilityChecks

Wire into every UI test:

```kotlin
@BeforeClass @JvmStatic
fun enableA11yChecks() {
    AccessibilityChecks.enable()
        .setRunChecksFromRootView(true)
        .setSuppressingResultMatcher(
            allOf(
                matchesCheckNames(`is`("TouchTargetSizeCheck")),
                matchesViews(withId(R.id.custom_chip)) // document exceptions
            )
        )
}
```

In Compose tests:

```kotlin
@Before fun enable() {
    composeTestRule.enableAccessibilityChecks()
}

@Test fun loginScreenIsAccessible() {
    composeTestRule.setContent { LoginScreen() }
    composeTestRule.onRoot().assertIsDisplayed()
    // Accessibility checks run automatically at the end of each operation
}
```

### 3. iOS — Accessibility Inspector (Xcode)

Open with `Xcode → Open Developer Tool → Accessibility Inspector`. Point it at the Simulator or device. Use:

- **Inspection**: hover to inspect label/trait/value.
- **Audit**: runs checks for contrast, hit area, missing descriptions, dynamic-type clipping.

### 4. iOS — XCUIAccessibilityAudit (Xcode 15+)

Run audits inside XCUITests and fail the build on violations.

```swift
func testLoginAccessibility() throws {
    let app = XCUIApplication()
    app.launch()

    try app.performAccessibilityAudit(for: [.contrast, .dynamicType, .elementDetection, .hitRegion]) { issue in
        // Return true to ignore a known issue.
        return issue.auditType == .hitRegion && issue.element?.label == "decorative"
    }
}
```

Audit types: `.contrast`, `.dynamicType`, `.elementDetection`, `.hitRegion`, `.sufficientElementDescription`, `.parentChild`, `.trait`, `.textClipped`, `.action`.

### 5. Flutter — `flutter_test` + axe

Enable semantics and use the test matcher:

```dart
testWidgets('LoginScreen is accessible', (tester) async {
  final handle = tester.ensureSemantics();
  await tester.pumpWidget(const MyApp(home: LoginScreen()));

  await expectLater(tester, meetsGuideline(androidTapTargetGuideline));
  await expectLater(tester, meetsGuideline(iOSTapTargetGuideline));
  await expectLater(tester, meetsGuideline(textContrastGuideline));
  await expectLater(tester, meetsGuideline(labeledTapTargetGuideline));

  handle.dispose();
});
```

For deeper audits add `axe_flutter_tester`:

```dart
await AxeFlutterTester(tester).checkForAccessibilityIssues();
```

### 6. React Native — @axe-core/react-native

```tsx
import axe from '@axe-core/react-native';

if (__DEV__) {
  axe.runA11yCheck().then(results => console.warn(results.violations));
}
```

For Jest + `@testing-library/react-native`:

```tsx
import { render } from '@testing-library/react-native';
import { toHaveAccessibleName, toHaveAccessibilityValue } from '@testing-library/jest-native';

expect.extend({ toHaveAccessibleName, toHaveAccessibilityValue });

test('submit button has accessible name', () => {
  const { getByRole } = render(<LoginScreen />);
  expect(getByRole('button', { name: /sign in/i })).toHaveAccessibleName('Sign in');
});
```

### 7. Static Analysis

- Android lint rules: `MissingContentDescription`, `ContentDescription`, `UseCompatTextViewDrawableApi`. Promote to error:

```groovy
android {
    lint {
        error += ["ContentDescription", "MissingContentDescription", "ClickableViewAccessibility"]
    }
}
```

- SwiftLint + custom rules can flag `accessibilityLabel` missing on `Image` / `Button`.
- Dart analyzer: `dart_code_metrics` has a rule to require semantics on icons.

### 8. CI Wiring

Sample GitHub Actions step for Android:

```yaml
- name: Run instrumentation tests with a11y
  uses: reactivecircus/android-emulator-runner@v2
  with:
    api-level: 34
    script: ./gradlew connectedDebugAndroidTest
```

For iOS:

```yaml
- run: xcodebuild test -scheme App -destination 'platform=iOS Simulator,name=iPhone 15'
```

Fail the build on any unsuppressed a11y violation. Maintain a *suppression file* with justifications, reviewed quarterly.

### 9. Reporting

- Publish audit HTML reports as CI artifacts.
- Track a11y-violation count per build; treat regressions like test failures.
- Keep a per-screen baseline so new violations are flagged immediately.

### 10. Limitations

Automated tools **cannot** catch:

- Whether a label is meaningful ("Button 1" passes missing-label).
- Whether focus order is logical.
- Whether live-region announcements happen at the right time.
- Whether gesture alternatives exist.
- Whether the experience is actually usable.

Always combine with manual audits (see `manual-a11y-audit` skill).

### 11. Common Pitfalls

- Running axe only in dev; never in CI → drift.
- Suppressing violations without tracking them.
- Tools against Simulator only; real devices behave differently.
- Ignoring tool "Warning" severity — many are actual bugs.
- Running audit on a single screen instead of sampling across flows.

## Checklist

- [ ] CI runs Espresso / XCUI / Flutter a11y matchers on every PR.
- [ ] Android `lint.error += [...]` enforces a11y-related rules.
- [ ] iOS `performAccessibilityAudit` enabled for critical flows.
- [ ] Suppressions are file-backed and justified.
- [ ] Baseline tracked over time; new violations fail the build.
- [ ] Manual audit scheduled alongside automated coverage.
