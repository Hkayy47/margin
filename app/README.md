# Margin app (Android)

Expo SDK 57 **dev build** (Expo Go can't load VisionCamera's native code), TypeScript, VisionCamera 5.

Right now it's the M0 "hello camera": a live preview and a **Check** button that takes a full-resolution still and shows its size and capture time.

## Get it on your phone

Pick one.

**A. Cloud build (no Android Studio needed)**

```sh
npm install
npx eas-cli@latest login          # free Expo account
npx eas-cli@latest build --profile development --platform android
```

Open the link it prints on your phone, install the APK, then on the laptop run `npx expo start` and open the project from the app (same Wi-Fi).

**B. Local build (Android Studio + USB debugging)**

```sh
npm install
npx expo run:android              # builds, installs and launches on the phone plugged in over USB
```

## Checks

```sh
npx tsc --noEmit
npx expo-doctor
```
