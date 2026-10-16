---
name: android-emu
description: Use when Android work needs emulator lifecycle, ADB, APK installation, instrumentation tests, screenshots, UI interaction, or device-specific verification. Prefer an existing project or machine lease helper when available, target an emulator explicitly, and never use a physical device without explicit user authorization.
---

# Android emulator workflow

Use the project's existing device workflow first. The goal is deterministic device ownership and explicit targeting, not a particular emulator brand or local fleet.

## 1. Discover the local workflow

Check project instructions and available tools before starting a device.

- If an `android-emu` helper exists, use `android-emu status` and `android-emu claim [AVD...]`; it is authoritative for shared-machine ownership.
- Otherwise use the Android tooling already configured by the project to list existing AVDs/running emulators. Do not create an AVD, install a new system image, or change a shared baseline merely to unblock a task unless the user explicitly asked for that setup work.
- Do not assume an AVD name, API level, screen size, or snapshot exists.

## 2. Target exactly one device

Capture the selected emulator serial and pass it explicitly to every device-sensitive command. Do not rely on an implicit default when multiple devices are visible.

```bash
adb -s emulator-NNNN shell ...
ANDROID_SERIAL=emulator-NNNN ./gradlew :app:connectedDebugAndroidTest
```

A physical device is never a silent fallback. Use one only when the user explicitly authorizes that device for the task.

## 3. Verify the real behavior

Use the narrowest real scenario that proves the changed Android behavior: instrumentation, install/launch, screenshot, UI interaction, permissions/lifecycle, or another device-visible check. A successful build alone does not prove runtime UI or platform behavior.

## 4. Release shared resources

If a lease/helper was used, release it when device work ends, including after failures:

```bash
android-emu release
```

Do not leave a shared emulator reserved for a hypothetical later task.
