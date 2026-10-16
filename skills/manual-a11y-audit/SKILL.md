---
name: manual-a11y-audit
description: Heuristic audit playbook, user-testing approach, and issue-logging conventions for mobile accessibility. Use this before every major release or at least quarterly on the main flows.
---

# Manual Accessibility Audit

## Instructions

Automated checks cover the mechanics; manual audits cover *experience*. This skill is the playbook for a repeatable audit you can run in a day per feature.

### 1. Scope the Audit

- Pick **one primary user flow** (onboarding, checkout, core task).
- Define success: "a blind user can complete checkout without sighted help in under 3 minutes".
- Test on **real hardware**, not only simulators. A wired keyboard + a real switch + TalkBack on a mid-range Android device.

### 2. Environments to Test

Run the flow once under each of the following configurations. Log every issue as you go.

| # | Configuration |
|---|---|
| 1 | Default |
| 2 | VoiceOver on (iOS) |
| 3 | TalkBack on (Android) |
| 4 | Dynamic Type = Accessibility XXL / Font scale largest |
| 5 | Dark mode |
| 6 | Increase Contrast / High Contrast Text |
| 7 | Reduce Motion enabled |
| 8 | External Bluetooth keyboard only (no touch) |
| 9 | Switch Control / Switch Access (single-switch auto scan) |
| 10 | Voice Control / Voice Access |
| 11 | RTL locale (Arabic or Hebrew test build) |
| 12 | Slow 3G + flaky network (to observe focus after loading) |

### 3. Heuristics Checklist (Per Screen)

**Perceivable**

- [ ] Every image/icon has a label or is hidden.
- [ ] Contrast passes 4.5:1 (text) and 3:1 (UI).
- [ ] No info conveyed by color alone.
- [ ] Text reflows at 200% without loss.

**Operable**

- [ ] Every action reachable without gesture.
- [ ] Touch targets >= 44/48.
- [ ] Keyboard Tab traversal reaches every control.
- [ ] Visible focus indicator, 3:1 contrast.
- [ ] Escape / back always closes modals.

**Understandable**

- [ ] Labels describe purpose, not appearance.
- [ ] Errors state what's wrong + how to fix.
- [ ] Navigation consistent across screens.

**Robust**

- [ ] VoiceOver + TalkBack announce role + state + value correctly.
- [ ] Live regions fire at the right moments.
- [ ] No AT crashes on complex screens.

### 4. Scripted Walkthroughs

For each primary flow, write a short script:

```text
Scenario: Screen reader checkout (iOS, VoiceOver)
Given the cart has 2 items
When I swipe from the top of the cart screen
Then I hear "Cart. Heading." as the first focusable element
 And each item reads "<Title>, <Quantity>, <Price>"
 And the Checkout button is reachable within 6 right-swipes
 And tapping it announces "Payment. Heading."
```

Run the script literally. Any deviation is a bug.

### 5. Logging Issues

Use a consistent template — paste into the tracker verbatim.

```text
Title: [A11Y][iOS][VoiceOver] Cart quantity not announced on increment

Severity: Blocker | Major | Minor | Cosmetic
Affected AT: VoiceOver on iOS 18, Dynamic Type XL
Device: iPhone 15, iOS 18.1
Flow: Cart → Increment quantity

Steps:
1. Enable VoiceOver
2. Navigate to cart with 1 item
3. Swipe right until "Increase quantity" is focused
4. Double-tap to activate

Expected: VoiceOver announces the new quantity, e.g. "2".
Actual:   Focus remains; nothing is announced.

WCAG:    4.1.3 Status Messages (AA)
Fix:     Wrap quantity Text with accessibilityLiveRegion(.polite)
         or post announcement via UIAccessibility.post.
Evidence: screen_recording.mov (attached)
```

Include WCAG reference and a concrete fix suggestion — this keeps the ticket actionable.

### 6. User Testing

Heuristics plus real users:

- Recruit at least 2–3 participants per release using AT you have not tested internally (e.g., switch user, low-vision user).
- Pay participants at market rate (e.g., Fable, AccessWorks networks).
- Observe; do not help. Record (with consent) for the team to rewatch.
- Triangulate: if one participant struggles, investigate. If two do, it's a blocker.

### 7. Prioritization

- **Blocker**: the flow cannot be completed with the AT. Fix before release.
- **Major**: flow completes but with significant friction or confusion. Fix within the release train.
- **Minor**: friction, easily recovered. Fix in next cycle.
- **Cosmetic**: a11y polish (redundant label, etc.). Backlog.

### 8. Rotating Audit Cadence

- New feature: audit before release.
- Core flows: audit quarterly against the full matrix above.
- OS upgrade (iOS / Android major): re-audit known-affected screens within a week of developer preview.

### 9. Accessibility Review in PR

Beyond tickets, add an "A11y" line to every PR description:

```text
### A11y
- VoiceOver: read on iOS 18 Simulator, focus order correct.
- TalkBack: verified on Pixel 7, Android 14.
- Dynamic Type XXL: no clipping.
- Reduce Motion: transitions crossfade.
- Remaining gaps: none / #1234.
```

### 10. Dashboard and Trends

Track:

- Open a11y bugs by severity and age.
- Automated violations per build.
- % of features with a manual audit in last 90 days.

Publish weekly. Regression trends are easier to argue than individual tickets.

### 11. Common Pitfalls

- "It works in Simulator" — many AT bugs appear only on real devices.
- Testing only with VoiceOver on iOS — TalkBack behaves differently.
- Skipping the large Dynamic Type pass.
- Auditing only happy paths — errors and empty states are where a11y breaks.
- Reporting issues without reproduction steps or a WCAG mapping.

## Checklist

- [ ] Each release-critical flow audited on both iOS and Android with AT.
- [ ] All 12 environments in §2 exercised for at least one flow.
- [ ] Issues logged with severity, WCAG ref, and fix suggestion.
- [ ] User testing scheduled with AT users at least once per quarter.
- [ ] PR template includes an A11y section.
- [ ] Dashboard tracks open a11y debt and trends.
