---
name: input-validation-a11y
description: Announcing validation results, shaping error messages, and recovering focus. Use this when implementing client-side validation or async server-side errors in forms.
---

# Input Validation Accessibility

## Instructions

Validation is the most frequent reason a user hears silence from the screen reader while the UI lights up red. Make validation visible *and* audible, and make recovery obvious.

### 1. When to Validate

- **On blur** for per-field format errors (invalid email, bad phone).
- **On submit** for completeness ("Name required", "Accept terms required").
- **Live as-you-type** only for password strength meters and character counts — always additive, never blocking.

Avoid validating on every keystroke — the stream of announcements is unusable with VoiceOver / TalkBack.

### 2. Error Message Rules

- Say *what* is wrong and *how* to fix it: "Enter a valid email address, for example name@example.com".
- Avoid vague messages: "Invalid input", "Try again".
- Use the field label: "Email is required" (not "This field is required").
- Keep it short — screen readers read it verbatim.

### 3. Live Region Announcements

When an error appears, announce it automatically without stealing focus.

iOS (SwiftUI):

```swift
Text(error ?? "")
    .foregroundStyle(.red)
    .accessibilityHidden(error == nil)
    .onChange(of: error) { _, new in
        if let msg = new { UIAccessibility.post(notification: .announcement, argument: msg) }
    }
```

UIKit — set the error label's accessibility trait:

```swift
errorLabel.accessibilityTraits = .staticText
errorLabel.text = message
UIAccessibility.post(notification: .announcement, argument: message)
```

Compose:

```kotlin
if (error != null) {
    Text(
        text = error,
        color = MaterialTheme.colorScheme.error,
        modifier = Modifier.semantics { liveRegion = LiveRegionMode.Assertive }
    )
}
```

Flutter:

```dart
SemanticsService.announce('Email is required', Directionality.of(context));
```

RN:

```tsx
<Text
  accessibilityRole="alert"
  accessibilityLiveRegion="assertive"
  style={styles.error}>{error}</Text>
```

Use **polite** for non-blocking warnings (password strength moving to "weak"), **assertive** for blocking errors only.

### 4. Associating Errors With Fields

Screen readers should read the error as part of the field.

UIKit:

```swift
emailField.accessibilityLabel = "Email"
emailField.accessibilityValue = email
emailField.accessibilityHint = error ?? ""
```

Better — use a combined label so the reader announces "Email, required. Error: must include @":

```swift
emailField.accessibilityLabel = "Email, required. \(error.map { "Error: \($0)" } ?? "")"
```

Compose:

```kotlin
OutlinedTextField(
    value = email,
    onValueChange = ::onChange,
    label = { Text("Email") },
    isError = error != null,
    supportingText = { if (error != null) Text(error) },
    modifier = Modifier.semantics {
        if (error != null) this.error(error)
    }
)
```

The `error(...)` semantics property tells TalkBack the field is invalid and reads the message.

Flutter — `TextFormField` already sets semantics when `errorText` is non-null.

RN:

```tsx
<TextInput
  accessibilityLabel="Email"
  accessibilityInvalid={!!error}
  aria-errormessage="emailError" /* web */ />
<Text nativeID="emailError" accessibilityLiveRegion="polite">{error}</Text>
```

### 5. Error Summary on Submit

For long forms (signup, checkout), show a summary at the top on submit failure and move focus there, or to the first invalid field.

```swift
// SwiftUI
if !errors.isEmpty {
    VStack(alignment: .leading) {
        Text("Please fix the following:").font(.headline)
        ForEach(errors) { err in
            Button(err.message) { focus = err.field } // jump to field
        }
    }
    .accessibilityElement(children: .contain)
    .accessibilityAddTraits(.isHeader)
    .onAppear { announceScreenChange() }
}
```

Move focus to the summary heading so the reader picks it up.

### 6. Async / Server-Side Errors

- Network errors: "Couldn't sign in. Check your connection and try again." — actionable, no jargon.
- Server validation: map codes to human text, reuse the same a11y pattern (live region + field association).
- Don't lose the user's input on network failure.

### 7. Success States

Also announce success so AT users know the flow moved forward.

```kotlin
Snackbar(
    modifier = Modifier.semantics { liveRegion = LiveRegionMode.Polite }
) { Text("Profile saved") }
```

### 8. Password Strength Meters

- Announce strength changes via a **polite** live region only when the bucket changes (weak → medium → strong), not on every keystroke.
- Provide text alongside the visual bar (never bar-only).

### 9. Character Counters

For length-limited fields, expose the counter via `accessibilityValue` and update live as typing progresses — but throttle to announce every 10 characters or on pause, not every keystroke.

```dart
TextField(
  maxLength: 280,
  decoration: InputDecoration(counterText: '$length of 280'),
)
```

### 10. Common Pitfalls

- Red border only, no text.
- Error text present but not announced.
- Focus jumps to top on submit instead of to the summary or first error.
- Live region re-announces every keystroke.
- Error message contains the wrong field name.
- Success banner never announced; AT user doesn't know the save worked.
- Server error returns HTTP status code to the user ("Error 422").

## Checklist

- [ ] Each error paired with an explanation and a recovery hint.
- [ ] Errors announced via live region (polite or assertive as appropriate).
- [ ] Field's a11y state set to invalid / `error()` while message is present.
- [ ] On submit failure, focus moves to summary or first invalid field.
- [ ] Success states announced politely.
- [ ] Character counters / password meters announce on bucket change, not per key.
- [ ] User's input preserved on network errors.
