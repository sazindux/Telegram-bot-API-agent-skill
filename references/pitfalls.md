# Common Mistakes, Breaking Changes & Anti-Patterns (with Fixes)

- **Verified Against:** Bot API 10.4 (Nov 9, 2026) & MTProto Layer 225
- **Verification Date:** November 11, 2026
- **Primary Sources:**
  - [Telegram Bot API Specification](https://core.telegram.org/bots/api)
  - [Telegram Bot API Changelog](https://core.telegram.org/bots/api-changelog)
  - [Telegram Mini Apps Documentation](https://core.telegram.org/bots/webapps)
  - [Telegram Widgets (In-Chat HTML Widgets)](https://core.telegram.org/bots/widgets)
  - [MTProto Updates](https://core.telegram.org/api/updates)
  - [MTProto Files](https://core.telegram.org/api/files)
  - [Bot API Dialog IDs](https://core.telegram.org/api/bots/ids)

---

## 1. Using UTF-8 Byte or Python Code-Point Indices for `MessageEntity` Offsets
- **The Mistake:** Computing `MessageEntity.offset` and `length` using Python `len(s)` (Unicode code points) or Rust/Go `len(bytes)` (UTF-8 bytes). Any emoji outside the Basic Multilingual Plane (`U+10000`+, such as `🚀` or flag/skin-tone sequences) counts as **1 code point** in Python (`4 UTF-8 bytes`), but **2 UTF-16 code units** in Telegram ([Source](https://core.telegram.org/bots/api#messageentity)). Offsets after the first emoji shift and corrupt bold/link highlights or trigger `400 ENTITY_BOUNDS_INVALID`.
- **The Fix:** Always measure and slice strings in **UTF-16-LE 2-byte units** (or use `scripts/utf16_entity_offsets.py`):
  ```python
  def utf16_len(text: str) -> int:
      return len(text.encode("utf-16-le")) // 2
  ```

---

## 2. Incomplete or Double Escaping in `MarkdownV2`
- **The Mistake:** Using legacy `"Markdown"` mode (which lacks spoilers, underline, strikethrough, blockquotes, custom emoji, and date-time entities and fails on unmatched `_` inside URLs) or forgetting to escape `.`, `-`, `!`, `=`, `(`, `)`, or `>` in `"MarkdownV2"` (`400 Bad Request: can't parse entities: Character '.' is reserved and must be escaped with the preceding '\'`) ([Source](https://core.telegram.org/bots/api#markdownv2-style)).
- **The Fix:** Prefer `parse_mode: "HTML"` (only `<`, `>`, `&` need escaping in body text) or pass an explicit `entities` array (`parse_mode` omitted). When `MarkdownV2` is required, use context-aware escaping (`scripts/escape_markdown_v2.py`):
  - Outside code/links: escape all 18 characters `_*[]()~`>#+-=|{}.!`
  - Inside `code` / `pre`: escape only `` ` `` and `\`
  - Inside `(...)` link URLs: escape only `)` and `\`

---

## 3. Exceeding the 64-Byte `callback_data` Limit on Inline Buttons
- **The Mistake:** Serializing JSON objects or long UUIDs into `InlineKeyboardButton.callback_data` (`1–64 bytes`), causing `400 BUTTON_DATA_INVALID` (especially when multi-byte UTF-8 characters push a 30-character string over 64 bytes) ([Source](https://core.telegram.org/bots/api#inlinekeyboardbutton)).
- **The Fix:** Keep `callback_data` to compact colon-delimited tokens (`"act:buy:4812"`) and store complex payloads in KV/Redis/D1 keyed by a short ID.

---

## 4. Not Calling `answerCallbackQuery` or `answerWidgetQuery`
- **The Mistake:** Handling a button press (`callback_query`) or in-chat widget action (`widget_query` / `shared_widget_query`) by sending or editing a message without calling `answerCallbackQuery` or `answerWidgetQuery`. The user's Telegram client keeps spinning an infinite loading indicator on the button or widget for 30+ seconds ([Source](https://core.telegram.org/bots/api#answercallbackquery), [Source](https://core.telegram.org/bots/widgets)).
- **The Fix:** Always call `answerCallbackQuery(callback_query_id)` (even with empty parameters) or `answerWidgetQuery(widget_query_id)` on every interaction. In Bot API 10.3+, you can also return an **ephemeral message** directly inside `answerCallbackQuery` via `ephemeral_message: EphemeralMessageParameters` ([Source](https://core.telegram.org/bots/api-changelog#october-16-2026)).

---

## 5. Missing `widget_query` and `shared_widget_query` in `allowed_updates`
- **The Mistake:** Deploying an In-Chat HTML Widget (`sendWidget` / `sendSharedWidget`, introduced in Bot API 10.4) while using an explicit `allowed_updates` array in `setWebhook` or `getUpdates` that omits `"widget_query"` and `"shared_widget_query"`, or relying on default `allowed_updates` (which **excludes** `chat_member`, `message_reaction`, and `message_reaction_count`) ([Source](https://core.telegram.org/bots/api#setwebhook), [Source](https://core.telegram.org/bots/api-changelog#november-9-2026)).
- **The Fix:** Explicitly include `"widget_query"`, `"shared_widget_query"`, `"chat_member"`, `"message_reaction"`, and `"message_reaction_count"` whenever specifying `allowed_updates`.

---

## 6. Bot API 10.3 Breaking Change: `EphemeralMessageParameters` Replaced `ephemeral_text`
- **The Mistake:** Passing the Bot API 10.2 fields `ephemeral_text`, `ephemeral_parse_mode`, `ephemeral_entities`, `ephemeral_link_preview_options`, `ephemeral_reply_markup`, or `ephemeral_Receiver_user_id` to `answerCallbackQuery`, `sendMessage`, or `send*`. **Bot API 10.3 (Oct 16, 2026) removed those fields** in a breaking change ([Source](https://core.telegram.org/bots/api-changelog#october-16-2026)).
- **The Fix:** Pass `ephemeral_message` of type `EphemeralMessageParameters` to `answerCallbackQuery`, or use `sendEphemeralMessage(chat_id, receiver_user_id, message: EphemeralMessageParameters)` (note: in Bot API 10.4, `receiver_user_id` and `chat_id` can be omitted when replying to a callback query inside `answerCallbackQuery`) ([Source](https://core.telegram.org/bots/api-changelog#november-9-2026)).

---

## 7. Bot API 9.6 Breaking Change: `correct_option_ids` Replaced `correct_option_id` in Quizzes
- **The Mistake:** Reading `poll.correct_option_id` (singular integer) from `Poll` objects or passing `correct_option_id` to `sendPoll`. **Bot API 9.6 (Apr 3, 2026) replaced `correct_option_id` with `correct_option_ids: Array<Integer>`** to support multi-answer quizzes ([Source](https://core.telegram.org/bots/api-changelog#april-3-2026)).
- **The Fix:** Always pass and read `correct_option_ids: [0]` (array of 0-based indices) in `sendPoll` and `Poll`.

---

## 8. Trusting `Telegram.WebApp.initDataUnsafe` on the Backend
- **The Mistake:** Sending `window.Telegram.WebApp.initDataUnsafe.user.id` from a Mini App frontend to your backend API and trusting the user ID without cryptographic verification. Any attacker can forge JSON requests with arbitrary `user.id` values ([Source](https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app)).
- **The Fix:** Send the raw query string `window.Telegram.WebApp.initData` in an `Authorization` header and verify either:
  1. **HMAC-SHA256** (`secret_key = HMAC_SHA256(key="WebAppData", msg=bot_token)` -> `HMAC_SHA256(key=secret_key, msg=data_check_string) == hash`), OR
  2. **Ed25519** (`signature` field against Telegram's public key `e7bf03a2fa4602af4580703d88dda5bb59f32ed8b02a56c187fe7d34caed242d` over `${bot_id}:WebAppData\n${data_check_string}`), plus check `now - auth_date <= 86400` (see `scripts/validate_initdata.py`).

---

## 9. Using the wrong HMAC Secret Key for Login Widget vs. Mini App `initData`
- **The Mistake:** Using `HMAC_SHA256("WebAppData", bot_token)` to validate a **Telegram Login Widget** payload, or using `SHA256(bot_token)` to validate a **Mini App `initData`** payload. Every signature check fails!
- **The Fix:**
  - **Mini App (`initData`):** `secret_key = HMAC_SHA256(key=b"WebAppData", msg=bot_token.encode())` ([Source](https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app)).
  - **Login Widget (`data-onauth` / `data-auth-url`):** `secret_key = SHA256(bot_token.encode())` ([Source](https://core.telegram.org/widgets/login#checking-authorization)).

---

## 10. Missing `<meta name="telegram-widget-origins">` on In-Chat HTML Widgets (Bot API 10.4)
- **The Mistake:** Serving an In-Chat HTML Widget (`sendWidget`) without restricting allowed origins or forgetting that the iframe runs in a strict sandbox (`allow-scripts` only—no `localStorage`, no `cookies`, no `fetch`/`XHR` unless `url` ends with `#allow-same-origin` and domain ownership is verified via `_telegram-widget.<domain>` TXT DNS record) ([Source](https://core.telegram.org/bots/widgets)).
- **The Fix:** Always include `<meta name="telegram-widget-origins" content="https://yourdomain.com">` in `<head>`, pass dynamic state via `Widget.data` (`editMessageWidgetData` / `editSharedWidgetData`) + `window.TelegramWidget.onDataUpdated`, and trigger actions via `window.TelegramWidget.sendQuery(payload)`.

---

## 11. Failing to Answer `pre_checkout_query` Within 10 Seconds
- **The Mistake:** Running slow database migrations, external fulfillment calls, or LLM generation inside `pre_checkout_query` before calling `answerPreCheckoutQuery`. Telegram enforces a hard **10-second timeout** on `answerPreCheckoutQuery`; if missed, the user's Stars/payment checkout fails with an error dialog ([Source](https://core.telegram.org/bots/payments-stars)).
- **The Fix:** In `pre_checkout_query`, only verify item stock/price and immediately call `answerPreCheckoutQuery(ok=True)` within `< 1 second`. Perform fulfillment only **after** receiving `message.successful_payment` (and store `telegram_payment_charge_id` for idempotency and `refundStarPayment`).

---

## 12. Calling `getUpdates` While a Webhook is Active (`409 Conflict`)
- **The Mistake:** Running a local development instance using long polling (`getUpdates`) while production has an active webhook (`setWebhook`), or running two long-polling containers simultaneously. Telegram returns `409 Conflict: can't use getUpdates method while webhook is active` or `terminated by other getUpdates request` ([Source](https://core.telegram.org/bots/api#getupdates)).
- **The Fix:** Use a dedicated staging bot token from `@BotFather` for local development, or call `deleteWebhook` before starting long polling.

---

## 13. Assuming `sendVideo` in Channels Always Returns a Real `message_id`
- **The Mistake:** Calling `sendVideo`, `sendMediaGroup`, or `sendPaidMedia` to post a video `> 100 MB` in a channel and indexing `result.message_id` immediately in your database. Since **Bot API 8.2 (Jan 1, 2025)**, channels apply server-side video quality transcoding for videos over 100 MB and return a placeholder `Message` with **`message_id: 0`** until transcoding finishes ([Source](https://core.telegram.org/bots/api-changelog#january-1-2025)).
- **The Fix:** Check `if message.message_id == 0:` when posting large videos to channels, and wait for the subsequent `channel_post` update once server-side processing completes.

---

## 14. Checking `str(chat_id).startswith("-100")` to Detect Supergroups/Channels
- **The Mistake:** Hardcoding `String(chatId).startsWith("-100")` to check if a Bot API `chat_id` is a channel/supergroup. Since **Bot API 9.1 / MTProto Layer 225**, **Monoforums** (Direct Message channels) have `channel_id` values in `1002147483649 .. 3000000000000`, which convert to Bot API `chat_id` values in **`-4000000000000 .. -2002147483649`** ([Source](https://core.telegram.org/api/bots/ids)).
- **The Fix:** Always use numeric range checks (`scripts/dialog_id_converter.py`):
  - Standard channel/supergroup: `-1997852516352 <= chat_id <= -1000000000001`
  - Monoforum channel: `-4000000000000 <= chat_id <= -2002147483649`

---

## 15. Reusing an MTProto `.session` Across Multiple IPs (`406 AUTH_KEY_DUPLICATED`) or Caching Expired `file_reference`
- **The Mistake:**
  1. Copying a Telethon/Kurigram `.session` file from your laptop to a VPS while both are connected (`406 AUTH_KEY_DUPLICATED` permanently kills the key).
  2. Storing MTProto `document.file_reference` in a database for weeks and passing it to `upload.getFile` without handling `400 FILE_REFERENCE_EXPIRED` ([Source](https://core.telegram.org/api/files)).
- **The Fix:**
  1. Create a distinct session (`auth_key`) per deployment environment.
  2. Store `(peer_id, access_hash, msg_id)` alongside every cached MTProto media item; on `400 FILE_REFERENCE_EXPIRED`, call `messages.getMessages` / `channels.getMessages` to refresh `file_reference` and retry transparently.
