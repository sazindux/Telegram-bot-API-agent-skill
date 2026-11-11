# Telegram Mini Apps (`window.Telegram.WebApp`) Deep Dive (`references/mini-apps.md`)

- **Source:** [Telegram Mini Apps Documentation](https://core.telegram.org/bots/webapps), [Web Events (MTProto Bridge)](https://core.telegram.org/api/web-events), [Telegram Serverless](https://core.telegram.org/bots/serverless)
- **Verified Against:** **Bot API 10.4** (November 9, 2026; checked November 11, 2026)

---

## 1. SDK Connection & Origin Hardening (Bot API 10.2+)

Include the official SDK in `<head>` before any other script:
```html
<script src="https://telegram.org/js/telegram-web-app.js?65"></script>
```
- **Origin Hardening (Enforced July 20, 2026 — Bot API 10.2):** Telegram disallows calling Mini App methods from origins different from the original Mini App domain configured in `@BotFather`. Navigating to an external domain inside the Mini App WebView will lose access to `Telegram.WebApp` bridge methods unless opted out in `@BotFather` Mini App settings.

---

## 2. All 8 Mini App Launch Modes & Context Capabilities

Source: [core.telegram.org/bots/webapps#implementing-mini-apps](https://core.telegram.org/bots/webapps#implementing-mini-apps)

| Launch Mode | How It Is Opened | `initData` Has `query_id`? | How Data Is Returned to Bot |
|---|---|---|---|
| **1. Keyboard Button (`KeyboardButton.web_app`)** | From a `ReplyKeyboardMarkup` button in private chat | No | `Telegram.WebApp.sendData(str)` (up to **4,096 bytes**; sends `Message.web_app_data` and closes Mini App). |
| **2. Inline Button (`InlineKeyboardButton.web_app`)** | From an inline button under a message | **Yes** | Backend calls `answerWebAppQuery(web_app_query_id, result)` or `api.*` directly using verified `initData.user.id`. |
| **3. Menu Button (`MenuButtonWebApp`)** | From the chat input bar Menu Button (`setChatMenuButton`) | **Yes** | Same as Inline Button (`answerWebAppQuery` or direct Bot API calls). |
| **4. Main Mini App (`t.me/<bot>?startapp=<param>`)** | Profile "Launch App" button or direct link (`&mode=compact` optional) | No (`chat_instance` & `chat_type` present) | Backend API calls (`fetch` or `Telegram.WebApp.Serverless.call`), `shareMessage(prepared_id)`, or `switchInlineQuery`. |
| **5. Direct Link (`t.me/<bot>/<appname>?startapp=<param>`)** | Named short-name link in any chat (`&mode=compact` optional; opens fullscreen height by default since 7.6) | No (`chat_instance` & `chat_type` present) | Backend API calls, `shareMessage(prepared_id)`, or `switchInlineQuery`. |
| **6. Inline Mode (`InlineQueryResultsButton.web_app`)** | "Switch to Mini App" button above inline query results | No | Calls `Telegram.WebApp.switchInlineQuery(query, choose_chat_types)` to return to inline mode. |
| **7. Attachment Menu** | From the paperclip attachment menu in any chat | **Yes** | `answerWebAppQuery` or backend API calls. |
| **8. Chat Join Request (`sendChatJoinRequestWebApp` — Bot API 10.1+)** | Sent by a Guard Bot when a user requests to join a chat | Has `chat_join_request_query_id` | Backend calls `answerChatJoinRequestQuery(chat_join_request_query_id, approve)` (**Bot API 10.1+**). |

> **Start Parameter Rule:** `startapp` query parameters (`A-Z`, `a-z`, `0-9`, `_`, `-`, up to 512 chars) are passed to `Telegram.WebApp.initDataUnsafe.start_param` and the URL query parameter `tgWebAppStartParam`.

---

## 3. Validating `initData` (HMAC-SHA256 & Ed25519 Third-Party Validation)

**NEVER trust `Telegram.WebApp.initDataUnsafe` on your backend.** Always send the raw `Telegram.WebApp.initData` query string to your server and verify its cryptographic signature ([core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app](https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app)).

### Method A: Bot Backend Validation (HMAC-SHA256 with Bot Token)
1. Parse `initData` as URL query parameters (`URLSearchParams`).
2. Extract `hash` and remove `hash` from the parameter pairs.
3. Sort remaining `key=value` pairs alphabetically by `key` and join with `\n` (`data_check_string`).
4. Compute `secret_key = HMAC_SHA256(key = "WebAppData", data = bot_token)`. *(Note: `"WebAppData"` is the HMAC key and `bot_token` is the message!)*
5. Compute `calculated_hash = hex(HMAC_SHA256(key = secret_key, data = data_check_string))`.
6. Compare `calculated_hash` with `hash` using a constant-time comparison, and verify `Date.now()/1000 - Number(auth_date) < 86400` to prevent replay attacks.

### Method B: Third-Party Validation Without Bot Token (Ed25519 — Bot API 8.0+)
Third parties (analytics, SDKs, Mini App builders) can verify `initData` without the bot token using the `signature` field in `initData`:
1. Parse `initData`, remove **both** `hash` and `signature`, sort remaining `key=value` pairs alphabetically, and join with `\n`.
2. Prepend `<bot_id>:WebAppData\n` to form `data_check_string`:
   ```text
   <bot_id>:WebAppData
   auth_date=...
   query_id=...
   user=...
   ```
3. Verify the base64url-decoded `signature` against `data_check_string` using **Ed25519** and Telegram's official public key:
   - **Production Public Key:** `e7bf03a2fa4602af4580703d88dda5bb59f32ed8b02a56c187fe7d34caed242d`
   - **Test Environment Public Key:** `40055058a4ee38156a06562e52eece92a771bcd8346a8c4615cb7376eddf72ec`

---

## 4. `window.Telegram.WebApp` Properties & Sub-Objects (Bot API 10.4)

| Property / Sub-Object | Type | Introduced | Description |
|---|---|---|---|
| `initData` | `String` | 6.0 | Raw signed query string for server verification. |
| `initDataUnsafe` | `WebAppInitData` | 6.0 | Parsed object (`query_id`, `chat_join_request_query_id` [10.1], `user`, `receiver`, `chat`, `chat_type`, `chat_instance`, `start_param`, `can_send_after`, `auth_date`, `hash`, `signature` [8.0]). |
| `version` / `platform` | `String` | 6.0 / 6.4 | Bot API version in client & platform (`ios`, `android`, `tdesktop`, `weba`, `webk`, `macos`). |
| `colorScheme` | `String` | 6.0 | `"light"` or `"dark"` (`var(--tg-color-scheme)`). |
| `themeParams` | `ThemeParams` | 6.0–7.10 | `bg_color`, `text_color`, `hint_color`, `link_color`, `button_color`, `button_text_color`, `secondary_bg_color` [6.1], `header_bg_color` [7.0], `bottom_bar_bg_color` [7.10], `accent_text_color` [7.0], `section_bg_color` [7.0], `section_header_text_color` [7.0], `section_separator_color` [7.6], `subtitle_text_color` [7.0], `destructive_text_color` [7.0]. |
| `isActive` / `isExpanded` / `isFullscreen` | `Boolean` | 8.0 / 6.0 / 8.0 | Active state (not minimized), expanded state, fullscreen state. |
| `viewportHeight` / `viewportStableHeight` | `Float` | 6.0 | Visible height in px (`var(--tg-viewport-height)`, `var(--tg-viewport-stable-height)`). Pin bottom UI using `viewportStableHeight`. |
| `safeAreaInset` / `contentSafeAreaInset` | `Object` | **8.0** | `{top, bottom, left, right}` for device notch/home indicator (`safeAreaInset`) and Telegram UI controls (`contentSafeAreaInset`). Also exposed as CSS variables `--tg-safe-area-inset-*` and `--tg-content-safe-area-inset-*`. |
| `BackButton` | `BackButton` | 6.1 | `isVisible`, `onClick(cb)`, `offClick(cb)`, `show()`, `hide()`. |
| `MainButton` / `SecondaryButton` | `BottomButton` | 6.0 / **7.10** | `type`, `text`, `color`, `textColor`, `isVisible`, `isActive`, `isProgressVisible`, `hasShineEffect` [7.10], `position` (`"left"\|"right"\|"top"\|"bottom"`, SecondaryButton only [7.10]), `iconCustomEmojiId` [**9.5**], `setText()`, `onClick()`, `show()`, `hide()`, `enable()`, `disable()`, `showProgress()`, `hideProgress()`, `setParams(params)`. |
| `SettingsButton` | `SettingsButton` | 7.0 | `isVisible`, `onClick(cb)`, `offClick(cb)`, `show()`, `hide()`. |
| `HapticFeedback` | `HapticFeedback` | 6.1 | `impactOccurred("light"\|"medium"\|"heavy"\|"rigid"\|"soft")`, `notificationOccurred("error"\|"success"\|"warning")`, `selectionChanged()`. |
| `CloudStorage` | `CloudStorage` | 6.9 | Server-synced key-value store (up to **1,024 keys** per user, key `1–128` chars, value `0–4,096` chars): `setItem`, `getItem`, `getItems`, `removeItem`, `removeItems`, `getKeys`. |
| `DeviceStorage` | `DeviceStorage` | **9.0** | Persistent on-device local storage per user & Mini App (up to **5 MB** per user): `setItem(key, value, cb)`, `getItem(key, cb)`, `removeItem(key, cb)`, `clear(cb)`. |
| `SecureStorage` | `SecureStorage` | **9.0** | Encrypted iOS Keychain / Android Keystore storage for secrets/tokens (up to **10 items** per user): `setItem(key, value, cb)`, `getItem(key, cb)`, `restoreItem(key, cb)`, `removeItem(key, cb)`, `clear(cb)`. |
| `BiometricManager` | `BiometricManager` | 7.2 | `isInited`, `isBiometricAvailable`, `biometricType` (`"finger"\|"face"\|"unknown"`), `isAccessRequested`, `isAccessGranted`, `isBiometricTokenSaved`, `deviceId`, `init(cb)`, `requestAccess(params, cb)`, `authenticate(params, cb)`, `updateBiometricToken(token, cb)`, `openSettings()`. |
| `LocationManager` | `LocationManager` | **8.0** | `isInited`, `isLocationAvailable`, `isAccessRequested`, `isAccessGranted`, `init(cb)`, `getLocation(cb)`, `openSettings()`. |
| `Accelerometer` / `Gyroscope` / `DeviceOrientation` | Sensor Objects | **8.0** | `isStarted`, `x`, `y`, `z` (or `alpha`, `beta`, `gamma`, `absolute`), `start({refresh_rate: 20..1000}, cb)`, `stop(cb)`. |
| `Serverless` | `Serverless` | **Oct 2026** | `Telegram.WebApp.Serverless.call(endpointName, inputObj?, callback)` — invokes `tgcloud/endpoints/<name>.js` with pre-verified `ctx.initData` ([core.telegram.org/bots/serverless](https://core.telegram.org/bots/serverless)). |

---

## 5. Key `window.Telegram.WebApp` Methods (Bot API 6.0–10.4)

- **Lifecycle & Layout:** `ready()`, `expand()`, `close()`, `requestFullscreen()` [8.0], `exitFullscreen()` [8.0], `lockOrientation()` [8.0], `unlockOrientation()` [8.0], `enableClosingConfirmation()` [6.2], `disableClosingConfirmation()` [6.2], `enableVerticalSwipes()` [7.7], `disableVerticalSwipes()` [7.7], `hideKeyboard()` [**9.1**], `setHeaderColor(color)` [6.1/6.9], `setBackgroundColor(color)` [6.1], `setBottomBarColor(color)` [7.10].
- **Permissions & Peer Requests:**
  - `requestWriteAccess([callback])` [6.9] — asks user permission for the bot to DM them.
  - `requestContact([callback])` [6.9] — asks user to share their phone number with the bot.
  - `requestChat(prepared_button_id, [callback])` [**9.6**] — opens a native peer/chat/user/managed-bot picker prepared via `savePreparedKeyboardButton`.
  - `requestEmojiStatusAccess([callback])` [8.0] & `setEmojiStatus(custom_emoji_id, [params, callback])` [8.0].
- **Sharing, Files & Home Screen:**
  - `shareMessage(msg_id, [callback])` [8.0] — opens a native dialog to share a `PreparedInlineMessage` created via Bot API `savePreparedInlineMessage`.
  - `shareToStory(media_url, [params])` [7.8] — opens the native Story editor with `media_url`, optional `text`, and `widget_link: {url, name}`.
  - `downloadFile({url, file_name}, [callback])` [8.0] — shows native file download prompt.
  - `addToHomeScreen()` [8.0] & `checkHomeScreenStatus([callback])` [8.0] (`"unsupported" | "unknown" | "added" | "missed"`).
- **Navigation, Payments & Popups:**
  - `openLink(url, [{try_instant_view, try_browser}])` [6.1/6.4] (must be called inside a user click handler).
  - `openTelegramLink(url)` [6.1/7.0] (does not close the Mini App since 7.0).
  - `openInvoice(url, [callback])` [6.1] — opens an invoice created via `createInvoiceLink`; callback receives `"paid" | "cancelled" | "failed" | "pending"`.
  - `showPopup(params, [cb])`, `showAlert(msg, [cb])`, `showConfirm(msg, [cb])` [6.2], `showScanQrPopup({text}, [cb])`, `closeScanQrPopup()` [6.4], `readTextFromClipboard([cb])` [6.4].
