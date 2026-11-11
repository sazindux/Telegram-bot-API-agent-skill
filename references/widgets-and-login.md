# In-Chat HTML Widgets (Bot API 10.4), Login Widgets & Deep Links (`references/widgets-and-login.md`)

- **Source:** [Telegram Widgets (In-Chat HTML Widgets)](https://core.telegram.org/bots/widgets), [Log In With Telegram (OIDC)](https://core.telegram.org/widgets/login), [Legacy Login Widget](https://core.telegram.org/widgets/login-legacy), [Deep Links](https://core.telegram.org/api/links)
- **Verified Against:** **Bot API 10.4** (November 9, 2026; checked November 11, 2026)

---

## 1. Bot API 10.4 In-Chat HTML Widgets (`sendWidget` & `window.TelegramWidget`)

Introduced in **Bot API 10.4** (November 9, 2026), In-Chat HTML Widgets are small, self-contained interactive blocks drawn directly inside a message bubble ([core.telegram.org/bots/widgets](https://core.telegram.org/bots/widgets)).

### Core Architecture & Sandbox Limits
- **Code + State Model:** A widget is **immutable HTML/CSS/JS code** (set once at creation) plus **mutable state** (`chat_data` and `public_data`) updated exclusively by the bot.
- **Size Limits:**
  - Raw UTF-8 HTML (`html`): **<= 32,768 bytes** (32 KB), must not contain `U+0000` (`INPUT_MEDIA_WIDGET_HTML_INVALID`).
  - Compressed HTML: **<= 4,096 bytes** (4 KB) after server-side `zlib` compression at **level 9** (`INPUT_MEDIA_WIDGET_TOO_LARGE`). Target `<= 3,900 B` when building widgets.
  - `chat_data` and `public_data`: Up to **1,024 UTF-8 bytes** each.
  - `TelegramWidget.request(data)`: **1–64 UTF-8 bytes** (`data` in `answerWidgetQuery`: up to **1,024 UTF-8 bytes**).
- **QuickJS Offline Sandbox:**
  - Runs in QuickJS (not a browser WebView). `fetch`, `XMLHttpRequest`, `WebSocket`, and external URLs throw `NetworkDisabledError` or are stripped.
  - Only `<button>` form controls are kept (`<input>`, `<select>`, `<textarea>` are removed).
  - Bubble dimensions: Width `200–600 px` (typically `320–430 px` on mobile), Height `50–600 px` (no internal scrolling; content > 600 px is clipped). Height units (`vh`) are unsupported.
  - Paint limit: Up to **16 elements** at once may have a blurred shadow, `filter`, `backdrop-filter`, or `opacity < 1`.
- **Production vs. Test Server Availability (as of November 2026):**
  - **Production:** Widgets work in **private chats with the bot** (`sendWidget` / `sendSharedWidget`), including requests and TON wallet integration. Sent widget messages in production automatically have `has_protected_content: true` and cannot be forwarded or copied via `copyMessage`/`copyMessages`.
  - **Test Server:** Full support for private chats, groups/supergroups (requires `can_send_other_messages`), inline mode (`InputWidgetMessageContent` / `InputSharedWidgetMessageContent`), and forwarded shared widgets (`shared_widget_query`).

### Static vs. Shared Widgets & State Flow

| Feature | Static Widget (`is_shared: false`) | Shared Widget (`is_shared: true`) |
|---|---|---|
| **Creation** | `sendWidget` without `is_shared` | First `sendWidget` with `is_shared: true` returns `message.widget.id` (`widget_id`) |
| **Resending** | Send HTML again via `sendWidget` | Call `sendSharedWidget(chat_id, widget_id, ...)` |
| **`chat_data` (Per-Message State)** | Updated via `editMessageWidgetData(chat_id, message_id, chat_data=...)`; pushed live to open widgets | Per-message; updated via `editMessageWidgetData` |
| **`public_data` (Shared State)** | Stored on the message (`editMessageWidgetData`) | Shared across all messages/forwards; updated via `editSharedWidgetData(widget_id, public_data=..., cache_time=5..3600)` |
| **Live Polling of `public_data`** | Pushed automatically with message edits | Widget calls `TelegramWidget.watchPublicData()` to poll at `cache_time` (default 30s, range 5–3600s) while on screen |

> **Critical State Rule:** `answerWidgetQuery(widget_query_id, data=...)` returns a one-off response (`{ result: data }`) ONLY to the user/widget instance that tapped. It **never** mutates `chat_data` or `public_data`. To persist state changes, call `editMessageWidgetData` or `editSharedWidgetData` alongside `answerWidgetQuery`!

### `window.TelegramWidget` JavaScript API Reference

| Property / Method / Event | Signature / Type | Description |
|---|---|---|
| `chatData` / `publicData` | `string \| null` | Current per-message `chat_data` and shared `public_data` (empty/unset is always `null`). |
| `viewer` | `WidgetViewer \| null` | `{ id, first_name, last_name?, username?, language_code?, is_premium? }` (present where widget can send requests). |
| `chatType` | `string \| null` | `"private"`, `"group"`, `"supergroup"`, `"channel"`, or `"sender"`. |
| `colorScheme` / `themeParams` | `"light" \| "dark"` / `ThemeParams` | Matches chat bubble palette (`--tg-theme-bg-color`, `--tg-theme-text-color`, `--tg-theme-hint-color`, `--tg-theme-link-color`, `--tg-theme-button-color`, `--tg-theme-button-text-color`, `--tg-theme-secondary-bg-color`, `--tg-theme-section-separator-color`). |
| `contentSafeAreaInset` | `{top, bottom, left, right}` | Corner timestamp band when no caption is below the widget (`env(safe-area-inset-bottom)`, `--tg-content-safe-area-corner-right/left`). |
| `request(data)` | `(data: string) => Promise<{result: string \| null}>` | Sends 1–64 bytes to the bot (`widget_query` / `shared_widget_query`). Rejects with `WidgetRequestError` (`code`: `"NOT_ALLOWED" \| "BUSY" \| "RATE_LIMITED" \| "TIMEOUT" \| "FAILED" \| "INVALID_ANSWER"`). Must be called synchronously inside a tap handler (or in background in private chat). |
| `watchPublicData()` / `unwatchPublicData()` | `() => void` | Starts/stops polling shared `public_data` while the shared widget is on screen. |
| `setResizeAnchor(anchor)` | `('top' \| 'bottom') => void` | Controls which edge stays fixed when widget height changes (`'top'` default). |
| `copyText(text)` | `(text: string) => void` | One-tap clipboard copy (must be called synchronously in a tap handler). |
| `openLink(url)` / `openTelegramLink(url)` | `(url: string) => void` | Opens external URL or `t.me` link (consumes the tap's single action slot). |
| `HapticFeedback` | `HapticFeedback` | Same methods as `Telegram.WebApp.HapticFeedback`. |
| `wallet` | `WidgetWallet` | TON wallet integration: requests user's TON wallet card (`WidgetQueryTypeData`), TON-signed data (`WidgetQueryTypeSignData`), or TON transaction (`WidgetQueryTypeSentTransaction`). |
| `onEvent(type, fn)` / `offEvent(type, fn)` | Event listener | Events: `'chatDataChanged'`, `'publicDataChanged'`, `'themeChanged'`, `'contentSafeAreaChanged'`. |

### Gesture Claim Rules (`touch-action`)
- **Taps & double taps:** Always belong to the widget.
- **Vertical drags:** Always scroll the chat (`pointercancel` sent to widget). Never build vertical sliders in a widget!
- **Horizontal drags & holds:** Controlled via CSS `touch-action` on the target element:
  - `touch-action: auto` (default): Hold opens chat message menu; horizontal drag triggers swipe-to-reply.
  - `touch-action: pan-y`: Widget claims horizontal drags (carousels, horizontal sliders); hold still opens chat message menu.
  - `touch-action: none`: Widget claims **both** holds (`contextmenu`) and horizontal drags (games, hold buttons, canvas).

---

## 2. Log In With Telegram (OIDC / OAuth 2.0 & Legacy Login Widget)

### A. Modern OIDC / OAuth 2.0 Flow (`https://core.telegram.org/widgets/login`)
1. Open `@BotFather` Mini App -> select bot -> **Login Widget** -> register **Allowed URLs** (origins and redirect URIs) and copy your **Client ID** and **Client Secret**.
2. Redirect user to Telegram's authorization endpoint with `client_id`, `redirect_uri`, `response_type=code`, `scope` (`openid` required; optional `profile`, `phone`, `bot_access`), `state` (CSRF token), and PKCE `code_challenge` (`S256`).
3. Exchange `code` + `code_verifier` via server-side `POST` with HTTP Basic Auth (`base64(client_id:client_secret)`) to receive `access_token` and `id_token` (JWT).
4. Verify the `id_token` signature against Telegram's OIDC JWKS endpoint.

### B. Legacy Login Widget (`https://core.telegram.org/widgets/login-legacy`)
1. Link domain via `/setdomain` in `@BotFather` and embed `https://telegram.org/js/telegram-widget.js?22`.
2. **Server Verification (Different from Mini Apps!):**
   - Sort received fields (`id`, `first_name`, `last_name`, `username`, `photo_url`, `auth_date`) alphabetically as `key=value` joined by `\n` (excluding `hash`).
   - Compute `secret_key = SHA256(bot_token)` (**raw SHA-256 of the bot token**, NOT HMAC with `"WebAppData"`!).
   - Verify `hex(HMAC_SHA256(key = secret_key, data = data_check_string)) == hash` and check `auth_date` freshness.
*(See `scripts/validate_initdata.py --mode login` for a tested implementation.)*

---

## 3. Essential `t.me` & `tg://` Deep Link Formats

Source: [core.telegram.org/api/links](https://core.telegram.org/api/links) & [Bot API 10.4 Changelog](https://core.telegram.org/bots/api-changelog)

| Link Purpose | `t.me` HTTPS Format | `tg://` URI Format | Notes / Version |
|---|---|---|---|
| **Bot Start (Private)** | `https://t.me/<bot>?start=<param>` | `tg://resolve?domain=<bot>&start=<param>` | `<param>`: up to 64 chars (`A-Z`, `a-z`, `0-9`, `_`, `-`). Sends `/start <param>`. |
| **Bot Add to Group** | `https://t.me/<bot>?startgroup=<param>&admin=<rights>` | `tg://resolve?domain=<bot>&startgroup=<param>&admin=<rights>` | Prompts group selection; optional `+`-separated admin rights (`manage_chat+delete_messages+...`). |
| **Bot Add to Channel** | `https://t.me/<bot>?startchannel&admin=<rights>` | `tg://resolve?domain=<bot>&startchannel&admin=<rights>` | Prompts channel selection and sets admin rights. |
| **Private-Chat Bot Topic** | `https://t.me/<bot_username>/<message_thread_id>` | — | **Added in Bot API 10.4:** Opens the specific topic in the private chat with the bot. |
| **Main Mini App** | `https://t.me/<bot>?startapp=<param>&mode=compact` | `tg://resolve?domain=<bot>&startapp=<param>` | Opens Main Mini App (`mode=compact` opens half-screen). |
| **Direct Link Mini App** | `https://t.me/<bot>/<appname>?startapp=<param>` | `tg://resolve?domain=<bot>&appname=<app>&startapp=<param>` | Opens named Mini App in current chat context. |
| **Create Managed Bot** | `https://t.me/newbot/<manager_bot>/<suggested_username>?name=<Name>` | `tg://newbot?manager=<manager_bot>&username=<user>&name=<Name>` | **Added in Bot API 9.6:** Prompts user to create a bot managed by `<manager_bot>`. |
| **Channel Direct Messages** | `https://t.me/<channel_username>?direct` | `tg://resolve?domain=<channel_username>&direct` | Opens the channel's Monoforum direct messages chat. |
| **Message / Checklist / Poll Link** | `https://t.me/<user>/<msg_id>?t=1m20s&task=2&option=<b64>` | `tg://resolve?domain=<user>&post=<id>&task=2&option=<b64>` | Highlights media timestamp `t`, checklist `task` ID, or poll `option` (`base64url`) (**Layer 225**). |
| **Business Chat Link** | `https://t.me/m/<slug>` | `tg://message?slug=<slug>` | Opens business chat with pre-filled styled text. |
| **Collectible Gift / Auction** | `https://t.me/nft/<slug>` / `https://t.me/auction/<slug>` | `tg://nft?slug=<slug>` / `tg://auction?slug=<slug>` | Opens unique gift card or gift auction. |
| **AI Compose Tone** | `https://t.me/addstyle/<slug>` | `tg://addstyle?slug=<slug>` | **Added in Layer 225:** Previews & installs custom AI compose tone. |
| **Upload Doc in RichMessage** | — | `tg://document?id=<id>` | **Added in Bot API 10.3:** General file upload link in `RichMessage`. |
