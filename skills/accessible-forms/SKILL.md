---
name: accessible-forms
description: Labels, errors, grouping, and autofill for mobile forms. Use this when building any screen that collects user input — login, signup, checkout, profile editing.
---

# Accessible Forms

## Instructions

Forms are where accessibility bugs cost users real money (unfinished checkouts, locked-out accounts). Every input must be labeled, every error actionable, every grouping meaningful.

### 1. Every Input Has a Visible Label

A placeholder is **not** a label:

- Placeholders disappear on focus, leaving nothing for users to reference.
- Placeholders usually fail contrast (deliberately gray).
- Screen readers may or may not announce them.

SwiftUI:

```swift
VStack(alignment: .leading, spacing: 6) {
    Text("Email").font(.subheadline)
    TextField("you@example.com", text: $email)
        .textFieldStyle(.roundedBorder)
        .textContentType(.emailAddress)
        .keyboardType(.emailAddress)
        .autocorrectionDisabled()
        .textInputAutocapitalization(.never)
        .accessibilityLabel("Email")
}
```

UIKit — associate via `accessibilityLabel` or use `UITextField.label` pattern:

```swift
emailField.accessibilityLabel = "Email"
emailField.textContentType = .emailAddress
emailField.keyboardType = .emailAddress
```

Compose:

```kotlin
Column(Modifier.fillMaxWidth()) {
    Text("Email", style = MaterialTheme.typography.labelLarge)
    OutlinedTextField(
        value = email,
        onValueChange = onChange,
        placeholder = { Text("you@example.com") },
        keyboardOptions = KeyboardOptions(
            keyboardType = KeyboardType.Email,
            imeAction = ImeAction.Next,
            autoCorrectEnabled = false,
        ),
        modifier = Modifier.semantics { contentDescription = "Email" }
    )
}
```

Flutter:

```dart
TextFormField(
  decoration: const InputDecoration(labelText: 'Email', hintText: 'you@example.com'),
  keyboardType: TextInputType.emailAddress,
  autofillHints: const [AutofillHints.email],
)
```

React Native:

```tsx
<View>
  <Text nativeID="emailLabel">Email</Text>
  <TextInput
    accessibilityLabel="Email"
    accessibilityLabelledBy="emailLabel"
    keyboardType="email-address"
    textContentType="emailAddress"
    autoCapitalize="none"
    autoComplete="email" />
</View>
```

### 2. Autofill Hints

Every input whose value is known to the OS should declare its content type so the OS offers autofill.

| Field | iOS `textContentType` | Android `autofillHints` / Compose `AutofillType` | Flutter `AutofillHints` | RN `textContentType` + `autoComplete` |
|---|---|---|---|---|
| Email | `.emailAddress` | `AutofillType.EmailAddress` | `email` | `emailAddress` / `email` |
| Password (login) | `.password` | `AutofillType.Password` | `password` | `password` / `password` |
| New password | `.newPassword` | `AutofillType.NewPassword` | `newPassword` | `newPassword` / `password-new` |
| OTP | `.oneTimeCode` | `AutofillType.SmsOtpCode` | `oneTimeCode` | `oneTimeCode` / `sms-otp` |
| Name | `.name` | `AutofillType.PersonFullName` | `name` | `name` / `name` |
| Street | `.fullStreetAddress` | `AutofillType.PostalAddress` | `streetAddressLine1` | `fullStreetAddress` / `street-address` |

### 3. Grouping and Field Sets

Related fields (address lines, card details) should announce as a group.

SwiftUI:

```swift
VStack {
    Text("Billing address").accessibilityAddTraits(.isHeader)
    TextField("Street", text: $street)
    TextField("City", text: $city)
}
.accessibilityElement(children: .contain)
.accessibilityLabel("Billing address")
```

Compose:

```kotlin
Column(Modifier.semantics { isTraversalGroup = true }) {
    Text("Billing address", Modifier.semantics { heading() })
    // fields
}
```

### 4. Error States

- Announce errors to the screen reader when they appear (live region).
- Place the error text next to the field *and* reference it from the field.
- Keep focus inside the erroring field after submit fails; don't reset to top.

UIKit:

```swift
emailField.accessibilityLabel = "Email. Error: must include @."
errorLabel.accessibilityLiveRegion = .polite // via category
UIAccessibility.post(notification: .announcement,
                     argument: "Email is invalid. Please include @.")
```

Compose:

```kotlin
OutlinedTextField(
    value = email,
    onValueChange = onChange,
    isError = !isValid,
    supportingText = {
        if (!isValid) {
            Text(
                "Enter a valid email",
                modifier = Modifier.semantics { liveRegion = LiveRegionMode.Polite }
            )
        }
    }
)
```

Flutter:

```dart
TextFormField(
  decoration: InputDecoration(
    labelText: 'Email',
    errorText: error, // announced on change via SemanticsService
  ),
  validator: (v) => isValid(v) ? null : 'Enter a valid email',
)

// For explicit announcements
SemanticsService.announce('Email is invalid', TextDirection.ltr);
```

RN:

```tsx
<Text
  accessibilityLiveRegion="polite"
  accessibilityRole="alert"
  style={styles.error}>
  {error}
</Text>
```

### 5. Required vs Optional

- Mark required fields explicitly: visible asterisk and text "required" in the a11y label.
- Prefer marking the few **optional** fields if most are required ("Phone (optional)").

```swift
.accessibilityLabel("Email, required")
```

### 6. Submit Button State

- Disable the submit button only while the request is in flight, not while the form is incomplete (gives better feedback — user presses and hears what's missing).
- If disabled, expose state and reason:

```kotlin
Button(
    onClick = submit,
    enabled = !loading,
    modifier = Modifier.semantics {
        if (loading) stateDescription = "Submitting"
    }
) { Text("Sign in") }
```

- After submit, announce success / error and move focus to a meaningful destination (success screen heading, error summary, or first invalid field).

### 7. Keyboard Navigation

Chain fields via `imeAction` / `returnKeyType` / `textInputAction` so Tab or Return advances to the next field.

```dart
TextFormField(textInputAction: TextInputAction.next, onFieldSubmitted: (_) => nextFocus());
```

### 8. Don't Break Paste

Some apps block paste into password or OTP fields "for security". That violates WCAG 3.3.8 (Accessible Authentication) and locks out password managers.

- Always allow paste.
- For OTPs, use `textContentType = .oneTimeCode` / `autofillHints = oneTimeCode` so the OS can offer autofill from SMS.

### 9. Sensitive Inputs

- Password fields: provide a show/hide eye button with `accessibilityLabel = "Show password"` / `"Hide password"`.
- Don't clear the password field after a failed login — screen-reader users lose their place.

### 10. Common Pitfalls

- Placeholder-as-label.
- No `textContentType` / `autofillHints`.
- Error shown only in red color.
- Focus jumps to top on submit error.
- Submit button disabled with no explanation.
- OTP field that blocks paste.
- "Confirm password" field with no `newPassword` hint.

## Checklist

- [ ] Every input has a visible label and an accessible label.
- [ ] Autofill hints set for email, password, name, address, OTP, etc.
- [ ] Errors announced via live region and not color-only.
- [ ] Focus remains on the erroring field after failed submit.
- [ ] Required fields labeled explicitly.
- [ ] Password fields allow paste and have show/hide toggle.
- [ ] Related fields grouped with a heading.
- [ ] Keyboard chain advances through fields with Next/Done.
