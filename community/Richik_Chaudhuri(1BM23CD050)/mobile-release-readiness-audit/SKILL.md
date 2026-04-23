---
name: mobile-release-readiness-audit
description: Audits mobile app codebases for pre-release readiness across iOS (Swift/SwiftUI/UIKit), Android (Kotlin/Jetpack Compose), Flutter (Dart), and React Native. Produces a ship / ship-with-caveats / block verdict backed by findings in six layers — privacy & permissions, accessibility, localization, crash-prone code, store metadata, and release-build hygiene. Use when given a mobile app repo (or parts of one) and asked to review, audit, pre-flight, check if ready to ship, prepare for App Store or Play Store submission, run a release checklist, do an accessibility or privacy compliance review, or diagnose a likely store rejection. Also use when user mentions TestFlight, beta submission, privacy manifest, PrivacyInfo.xcprivacy, Data Safety form, ATT prompt, content rating, age rating, export compliance, Info.plist audit, AndroidManifest audit, or "why will this get rejected".
---

# Mobile Release Readiness Audit

This skill is a **pre-ship audit engine** for mobile apps. It is NOT a code formatter, NOT a
test runner, and NOT a generic linter. It inspects a mobile codebase the way a senior mobile
release manager would on the last day before submission — catching the specific, rejection-prone,
user-visible failure modes that generic LLM suggestions miss.

When this skill activates, your job is to:

1. Identify the platform(s) in play — iOS native, Android native, Flutter, React Native, or hybrid.
2. Run the six-layer audit below. Do not skip layers even if one looks clean.
3. Assign each layer a verdict: **PASS**, **WARN**, or **FAIL**, with evidence (file:line or snippet).
4. Produce an overall release verdict using the decision rules at the end.
5. Output the structured report in the format shown in the final section.

Operate like a reviewer, not a cheerleader. If you cannot determine something from the material
given, say **UNKNOWN — need X** rather than guessing. A false PASS is worse than a WARN.

---

## Layer 1 — Privacy & Permissions (the #1 rejection reason in 2024+)

Answers: "Will the store reject this for privacy reasons, and does the manifest match reality?"

**iOS checks:**
- `PrivacyInfo.xcprivacy` exists. Required since May 2024 for apps using "required reason" APIs:
  `UserDefaults`, file timestamps (`creationDate`, `modificationDate`), `systemBootTime`,
  disk-space APIs (`volumeAvailableCapacity`), and active-keyboards query. Missing manifest or
  missing entry → App Store Connect auto-reject with `ITMS-91053`.
- Every `NS*UsageDescription` key in `Info.plist` corresponds to an actual API call in code —
  **and vice versa**. Unused descriptions are suspicious; missing ones are an instant reject.
- Usage descriptions are specific and user-facing. Generic strings like "This app needs camera
  access" or `"$(PRODUCT_NAME) needs…"` are rejected.
- ATT prompt (`requestTrackingAuthorization`) fires BEFORE any tracking SDK initialises,
  not after.
- If Facebook, Adjust, AppsFlyer, or Branch SDK is present, `NSUserTrackingUsageDescription`
  must exist.
- `ITSAppUsesNonExemptEncryption` declared in `Info.plist` if the app uses HTTPS or any crypto
  (else every TestFlight build prompts the dev).

**Android checks:**
- `targetSdkVersion >= 34` (Play Store hard cutoff as of Aug 2024 for updates).
- Dangerous permissions (`CAMERA`, `RECORD_AUDIO`, `ACCESS_FINE_LOCATION`,
  `ACCESS_BACKGROUND_LOCATION`, `READ_MEDIA_IMAGES`, `POST_NOTIFICATIONS`, `BLUETOOTH_SCAN`,
  `BLUETOOTH_CONNECT`) have a runtime prompt with rationale.
- Foreground service types declared in manifest AND matching runtime permission requested
  (API 34+): `location`, `camera`, `mediaPlayback`, `microphone`, `dataSync`, etc.
- Play Console Data Safety form matches SDKs present. If you see Firebase Analytics,
  Crashlytics, AdMob, Facebook SDK, Adjust, Sentry, or Bugsnag in `build.gradle`, the form
  must disclose the matching categories.
- High-risk permissions that need justification or will be rejected: `QUERY_ALL_PACKAGES`,
  `MANAGE_EXTERNAL_STORAGE`, `SYSTEM_ALERT_WINDOW`.

**Flutter / React Native:**
- Inspect the final built `Info.plist` / `AndroidManifest.xml`, not just source — plugins like
  `image_picker`, `geolocator`, `firebase_messaging`, `permission_handler` auto-inject
  permissions the developer may not have written.
- `firebase_messaging` on Android 13+ auto-adds `POST_NOTIFICATIONS` → must be requested
  at runtime.

---

## Layer 2 — Accessibility Coverage

Answers: "Can a user on VoiceOver / TalkBack actually use this app?"

Score 0–10. Below 5 = **FAIL**. 5–7 = **WARN**. 8+ = **PASS**.

**H1 — Interactive elements have labels (2 pts)**
Every icon-only `Button` / `IconButton` / `GestureDetector` / `Pressable` must have an
`accessibilityLabel` / `contentDescription` / `Semantics(label:)` / `tooltip`.

**H2 — Decorative images explicitly excluded (1 pt)**
SwiftUI: `.accessibilityHidden(true)`. Compose: `contentDescription = null` (paired with
clear semantics). Flutter: `ExcludeSemantics`. RN: `accessibilityElementsHidden` +
`importantForAccessibility="no"`.

**H3 — Minimum touch targets (1 pt)**
iOS HIG: 44×44pt. Material: 48×48dp. Flag any icon-only tappable below these.

**H4 — Dynamic Type / font scaling (2 pts)**
- iOS good: `.font(.body)`. Bad: `UIFont.systemFont(ofSize: 14)`.
- Android good: `sp` units, `MaterialTheme.typography.*`. Bad: `dp` on text.
- Flutter good: `Theme.of(context).textTheme.*`. Bad: `TextStyle(fontSize: 14)` on body
  wrapped in fixed-height containers.
- RN: `allowFontScaling={false}` is a red flag on body text.

**H5 — Contrast (2 pts)**
WCAG AA: ≥4.5:1 for normal text, ≥3:1 for large text and UI components. Common violations:
grey text `#999`/`#AAA` on white (~2.8:1), placeholder text at 50% opacity.

**H6 — Focus management (2 pts)**
Modals and sheets move focus on open and restore on close. Loading states announce
themselves. Grouped form controls use `accessibilityElement(children:)` / `mergeDescendants`.

---

## Layer 3 — Localization & Internationalization

Answers: "Will this break for a user in French, German, Arabic, or Japanese?"

- **No hardcoded user-facing strings** in UI files. Every literal in `Text(...)`, `UILabel`,
  `TextView`, `<Text>` comes from a resource file (`Localizable.strings`, `strings.xml`,
  `.arb`, i18n JSON).
- **Layout is not LTR-assumed.** No hardcoded `.leading` → `.left` mapping, no `marginLeft`
  instead of `marginStart`. Back chevrons, date pickers, progress bars mirror correctly.
- **Plurals use plural APIs** — stringsdict (iOS), plurals.xml (Android), ICU message format.
  Never `"You have \(n) items"` — it's wrong for every language except English.
- **Dates, numbers, currency formatted via locale APIs**, not string interpolation.
- **No ASCII string-length assumptions.** German compound words overflow fixed-width
  containers. Flag `Text(...).frame(width: 100)` style clamps on translatable strings.

---

## Layer 4 — Crash-Prone Code Patterns

Answers: "What's likely to take a crash log on day one?"

**Swift:**
- Force unwraps (`!`) on optionals from network, user input, file IO, dictionary access.
- `try!` on Codable decoding of network data — one schema drift and every user crashes.
- Implicitly unwrapped optionals (`var foo: Foo!`) outside UIKit outlets.
- `fatalError("not implemented")` / `preconditionFailure` on any reachable path.
- Synchronous network calls on the main queue.
- `Array.first!` / `items[0]` on collections that can be empty.

**Kotlin:**
- `!!` on intent extras, bundle values, JSON fields, `findViewById`.
- Unchecked casts (`as SomeType` without `as?`).
- `GlobalScope.launch` without a `CoroutineExceptionHandler`.
- `runBlocking` on the main thread or inside a coroutine scope.
- Unclosed `Cursor`, `InputStream`, `MediaPlayer`, `Camera` — use `.use { }`.

**Dart / Flutter:**
- `BuildContext` used after an `await` without an `if (!mounted) return` guard.
- `late` fields read before initialisation.
- `.first` / `.single` on iterables that can be empty.
- Unawaited `Future`s — missing `await` or `.catchError`.
- `as List` / `as Map` casts on unchecked JSON.

**React Native:**
- No error boundaries around feature screens — one bad render = white screen.
- `AsyncStorage.getItem` results passed to `JSON.parse` without null check.
- `new Date(maybeUndefined)` producing `Invalid Date` that propagates through formatters.
- `FlatList` with non-stable `keyExtractor` → re-render loops and OOM on long lists.

---

## Layer 5 — Store Metadata & Asset Compliance

Answers: "Does the submission package pass the store's mechanical checks?"

**Character limits:**
| Field | App Store | Play Store |
|---|---|---|
| App name / title | 30 | 30 |
| Subtitle / short desc | 30 | 80 |
| Full description | 4,000 | 4,000 |
| Release notes | 4,000 | 500 |

**Icons & screenshots:**
- iOS app icon: 1024×1024 PNG, **no alpha channel**, no rounded corners.
- Play high-res icon: 512×512 PNG 32-bit, no alpha padding.
- Play feature graphic: 1024×500 JPEG or 24-bit PNG.
- iOS screenshots required for 6.9″ (1290×2796 or 1320×2868) AND 6.7″ (1290×2796).
  iPad Pro 12.9″ (2048×2732) required if app supports iPad. Minimum 3 per size, max 10.
- Play screenshots: 2–8 per form factor, min 320px, max 3840px, aspect between 16:9 and 9:16.

**Mandatory:**
- Privacy Policy URL — live, HTTPS, reachable, matches actual data collection.
- Content rating / age rating — not "draft".
- Demo account credentials in App Review info if there's any login wall.
- Export compliance declared (iOS `ITSAppUsesNonExemptEncryption`; Play export section).
- Data Safety (Play) / Privacy Nutrition Label (iOS) matches SDKs in build.

**Rejection triggers (instant):**
- Emoji in name or subtitle
- Price or ranking claims ("#1 app!", "Free for a limited time")
- Mentioning other platforms ("Also on Android!")
- Keyword stuffing in Play description
- Name containing "beta", "demo", "test"

---

## Layer 6 — Release Build Hygiene

Answers: "Is this actually a release build, or a dev build with a version bump?"

- **No `print` / `console.log` / `Log.d`** in hot paths (render loops, network interceptors).
- **No leftover `TODO`, `FIXME`, `HACK`** on lines touching auth, payments, or data upload.
  Severity by file — TODO in `PaymentProcessor.swift` is ship-blocking; TODO in a utility
  is a WARN.
- **No committed secrets** — `.env` files, `GoogleService-Info.plist` with prod keys,
  hardcoded API base URLs pointing at staging, commented-out credentials.
- **No `NSAllowsArbitraryLoads`** (iOS ATS) or `usesCleartextTraffic="true"` (Android)
  unless scoped to a specific justified domain.
- **Proguard / R8 rules** present for reflection-heavy libs (Gson, Retrofit, Room, Hilt) on
  Android release build.
- **Version code + version name incremented** beyond the last published build.
- **Signing config is release**, not debug. `applicationId` does not end in `.debug`.
- **Third-party SDKs fresh** — any SDK >12 months behind its latest release is a WARN.
  Any SDK version with a known CVE is a FAIL.

---

## Decision Rules — Overall Verdict

Apply in order. First matching rule wins.

**1. BLOCK** (do not submit) if ANY of:
- Layer 1 (Privacy) = FAIL
- Missing privacy policy URL or missing required screenshots
- Any secret / prod API key committed in plaintext
- Any SDK with a known CVE
- Any reachable `fatalError` / `throw UnimplementedError` on the happy path

**2. SHIP WITH CAVEATS** if:
- 1–2 layers are WARN, none are FAIL
- Only cosmetic or localization-edge-case issues remain

**3. SHIP** only if all six layers are PASS or at most one is a minor WARN with a
documented follow-up.

Never downgrade a FAIL to a WARN for narrative convenience. The user asked for an audit,
not a morale boost.

---

## Output Format

```markdown
# Mobile Release Readiness Audit — <App Name>

**Verdict:** BLOCK | SHIP WITH CAVEATS | SHIP
**Platform(s):** iOS | Android | Flutter | React Native
**Audited against:** <date / commit SHA / package version>

## Top 3 Ship-Blockers

1. <highest-severity finding — one sentence + file:line>
2. <second>
3. <third>

(If SHIP, this section reads: "None — see layer notes for follow-ups.")

## Layer-by-Layer Findings

### Layer 1 — Privacy & Permissions: [PASS | WARN | FAIL]
- **Finding:** <one-sentence summary>
- **Evidence:** `path/to/file.swift:42` — <quoted snippet>
- **Fix:** <concrete next step, not generic advice>

### Layer 2 — Accessibility Coverage: [PASS | WARN | FAIL] (score X/10)
...

### Layer 3 — Localization & i18n: [PASS | WARN | FAIL]
...

### Layer 4 — Crash-Prone Code Patterns: [PASS | WARN | FAIL]
...

### Layer 5 — Store Metadata & Assets: [PASS | WARN | FAIL]
...

### Layer 6 — Release Build Hygiene: [PASS | WARN | FAIL]
...

## Unknowns — Could Not Verify

- <what was missing, e.g. "No Info.plist shared — could not confirm ATT prompt copy">
- <what would unblock, e.g. "Share `ios/Runner/Info.plist`">

## Recommended Fix Order

1. Everything under BLOCK or FAIL, in severity order.
2. WARN items that affect every non-English user.
3. WARN items that affect accessibility.
4. Hygiene WARNs.
```

---

## Anti-Patterns — What NOT to Do

- Do not suggest generic "improve error handling" fixes. Name the file and the pattern.
- Do not rewrite the codebase. The output is a diagnostic report, not a refactor PR.
- Do not claim a layer is PASS based on absence of evidence. If you didn't see the relevant
  files, mark it UNKNOWN.
- Do not recommend disabling a rejection-risk feature just to pass audit — fix it properly
  or mark it as a caveat.
- Do not invent file paths. Quote what you saw; if you didn't see it, ask for it.
- Do not pad the report with praise for what's already good unless asked — the user wants
  problems surfaced.
