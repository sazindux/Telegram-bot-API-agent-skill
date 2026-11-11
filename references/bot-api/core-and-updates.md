# Bot API Core, Requests, Updates, Limits & Errors (`references/bot-api/core-and-updates.md`)

- **Source:** [https://core.telegram.org/bots/api](https://core.telegram.org/bots/api), [https://core.telegram.org/bots/faq](https://core.telegram.org/bots/faq), [https://core.telegram.org/bots/webhooks](https://core.telegram.org/bots/webhooks), [https://github.com/tdlib/telegram-bot-api](https://github.com/tdlib/telegram-bot-api)
- **Verified Against:** **Bot API 10.4** (November 9, 2026; checked November 11, 2026)

---

## 1. Authentication & Request Formats

- **Bot Token Format:** `<bot_id>:<alphanumeric_secret>` (e.g., `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`), where `<bot_id>` is the bot's 64-bit `User.id`. Obtained via [@BotFather](https://t.me/BotFather) or programmatically for managed bots via `getManagedBotToken` (Bot API 9.6+).
- **Endpoint URL:**
  - Cloud API: `https://api.telegram.org/bot<token>/<METHOD_NAME>`
  - Test Environment API: `https://api.telegram.org/bot<token>/test/<METHOD_NAME>`
  - File Download URL: `https://api.telegram.org/file/bot<token>/<file_path>`
- **HTTP Methods:** Both `GET` and `POST` are supported. Method names are **case-insensitive**. All requests must use **UTF-8**.
- **4 Supported Parameter Encodings:**
  1. URL query string (`?chat_id=123&text=Hello`)
  2. `application/x-www-form-urlencoded`
  3. `application/json` (recommended for all requests **except** direct binary file uploads)
  4. `multipart/form-data` (required when uploading local files via `InputFile` or `attach://<file_attach_name>`)

### Response Envelope & Webhook Direct Reply

Every HTTP response is a JSON object with:
```json
{
  "ok": true,
  "result": { ... },
  "description": "Optional human-readable description"
}
```
On error:
```json
{
  "ok": false,
  "error_code": 429,
  "description": "Too Many Requests: retry after 35",
  "parameters": {
    "retry_after": 35
  }
}
```
- **`ResponseParameters` fields:**
  - `migrate_to_chat_id` (`Integer`, optional): The group has been upgraded to a supergroup with the specified 64-bit identifier; update your stored `chat_id` and retry.
  - `retry_after` (`Integer`, optional): In case of flood control (`429`), the number of seconds left to wait before the request can be repeated.
- **Making Requests in Webhook Responses:** When responding to an incoming webhook `POST`, you can return an HTTP `200 OK` with `Content-Type: application/json` (or `application/x-www-form-urlencoded` / `multipart/form-data`) containing `"method": "<METHOD_NAME>"` plus the method's parameters (e.g., `{"method": "sendMessage", "chat_id": 123, "text": "Ack"}`).
  - **Caveat:** You **cannot** receive the return value (`Message` object, `message_id`, or error status) when invoking a method inside the webhook HTTP response body ([core.telegram.org/bots/api#making-requests-when-getting-updates](https://core.telegram.org/bots/api#making-requests-when-getting-updates)).

---

## 2. Receiving Updates: `getUpdates` vs `setWebhook`

Telegram stores unconfirmed incoming updates for up to **24 hours**. `getUpdates` (long polling) and `setWebhook` (push) are **mutually exclusive**: calling `getUpdates` while a webhook is active returns `409 Conflict: can't use getUpdates method while webhook is active`.

### `Update` Object — Complete 27 Update Types (Bot API 10.4)

At most **one** of the optional fields below can be present in any given `Update` object ([core.telegram.org/bots/api#update](https://core.telegram.org/bots/api#update)):

| Field Name | Type | Default in `allowed_updates`? | Special Requirements & Version Introduced |
|---|---|---|---|
| `update_id` | `Integer` | Always present | Sequential positive integer; resets randomly if no updates for >= 7 days. |
| `message` | `Message` | Yes | New incoming message of any kind (text, photo, sticker, service message, etc.). |
| `edited_message` | `Message` | Yes | Edited message known to the bot. |
| `channel_post` | `Message` | Yes | New incoming channel post where bot is a member/admin. |
| `edited_channel_post` | `Message` | Yes | Edited channel post. |
| `business_connection` | `BusinessConnection` | Yes | Bot connected/disconnected/edited on a Business Account (Bot API 7.2+). |
| `business_message` | `Message` | Yes | New message from a connected Business Account (Bot API 7.2+). |
| `edited_business_message` | `Message` | Yes | Edited message from a connected Business Account (Bot API 7.2+). |
| `deleted_business_messages` | `BusinessMessagesDeleted` | Yes | Messages deleted from a connected Business Account (Bot API 7.2+). |
| `guest_message` | `Message` | Yes | New guest mode summoning message; reply via `answerGuestQuery` using `Message.guest_query_id` (**Bot API 10.0+**). |
| `message_reaction` | `MessageReactionUpdated` | **No (Must opt-in)** | User changed reaction; bot must be **admin** in chat and list `"message_reaction"` in `allowed_updates` (Bot API 7.0+). Not sent for bot reactions. |
| `message_reaction_count` | `MessageReactionCountUpdated` | **No (Must opt-in)** | Anonymous reaction counts changed; bot must be **admin** and list `"message_reaction_count"` in `allowed_updates` (grouped, delayed up to a few minutes) (Bot API 7.0+). |
| `inline_query` | `InlineQuery` | Yes | Incoming inline query (requires Inline Mode enabled in `@BotFather`). |
| `chosen_inline_result` | `ChosenInlineResult` | Yes | User selected an inline result (requires `/setinlinefeedback` enabled in `@BotFather`). |
| `callback_query` | `CallbackQuery` | Yes | User pressed an inline keyboard callback or game button. |
| `widget_query` | `WidgetQuery` | Yes | Query sent by an In-Chat HTML Widget in a message sent by or via the bot (**Bot API 10.4+**). |
| `shared_widget_query` | `SharedWidgetQuery` | Yes | Query sent from a forwarded message containing a shared HTML widget (**Bot API 10.4+**). |
| `shipping_query` | `ShippingQuery` | Yes | Shipping address query for invoices with `is_flexible=True`. |
| `pre_checkout_query` | `PreCheckoutQuery` | Yes | Checkout confirmation query; must call `answerPreCheckoutQuery` within **10 seconds**. |
| `purchased_paid_media` | `PaidMediaPurchased` | Yes | User purchased paid media with a non-empty `payload` sent by the bot in a non-channel chat (Bot API 7.10+). |
| `poll` | `Poll` | Yes | New poll state (only for polls sent by the bot or manually stopped polls). |
| `poll_answer` | `PollAnswer` | Yes | User changed vote in a non-anonymous poll sent by the bot. |
| `my_chat_member` | `ChatMemberUpdated` | Yes | Bot's own member status changed (including user blocking/unblocking the bot in private chat). |
| `chat_member` | `ChatMemberUpdated` | **No (Must opt-in)** | Any member's status changed; bot must be **admin** and explicitly list `"chat_member"` in `allowed_updates`. |
| `chat_join_request` | `ChatJoinRequest` | Yes | User requested to join chat; bot must have `can_invite_users` admin right (or be a guard bot, Bot API 10.1+). |
| `chat_boost` | `ChatBoostUpdated` | Yes | Chat boost added/changed; bot must be **admin** (Bot API 7.0+). |
| `removed_chat_boost` | `ChatBoostRemoved` | Yes | Chat boost removed; bot must be **admin** (Bot API 7.0+). |
| `managed_bot` | `ManagedBotUpdated` | Yes | A bot managed by this manager bot was created or its token/owner changed (**Bot API 9.6+**). |
| `subscription` | `BotSubscriptionUpdated` | Yes | User Star payment subscription changed (**Bot API 10.2+**). |
| `stopped_message_generation` | `MessageGenerationStopped` | Yes | User pressed Stop on a streaming draft (`sendMessageDraft`/`sendRichMessageDraft`) (**Bot API 10.3+**). |

> **Critical `allowed_updates` Rule:** Passing `allowed_updates: []` (empty array) subscribes to all update types **except** `chat_member`, `message_reaction`, and `message_reaction_count`. Furthermore, if you previously passed a custom `allowed_updates` list (e.g., `["message", "callback_query"]`) and later add Bot API 10.4 widgets or Stars payments without updating `allowed_updates` to include `"widget_query"`, `"shared_widget_query"`, or `"pre_checkout_query"`, Telegram will **not** deliver those updates!

---

## 3. Webhook Technical Requirements

Source: [Marvin's Marvellous Guide to All Things Webhook](https://core.telegram.org/bots/webhooks) & [setWebhook](https://core.telegram.org/bots/api#setwebhook)

| Requirement | Official Specification |
|---|---|
| **IP Protocol** | **IPv4 only** (IPv6 is not supported for cloud webhooks). |
| **Allowed Ports** | `443`, `80`, `88`, `8443` (any port allowed on Local Bot API Server). |
| **Telegram Source Subnets** | `149.154.160.0/20` and `91.108.4.0/22` |
| **TLS Version** | **TLS 1.2+** required on all ports (`SSLv2`, `SSLv3`, `TLS 1.0`, `TLS 1.1` rejected). |
| **Certificates** | Verified CA chain (including all intermediate certs) or self-signed PEM public key uploaded as `InputFile` in `certificate`. `CN` or `SAN` must match the domain exactly (no HTTP redirects). |
| **`secret_token`** | 1–256 chars (`A-Z`, `a-z`, `0-9`, `_`, `-`). Sent by Telegram in the `X-Telegram-Bot-Api-Secret-Token` HTTP header on every webhook POST. Always verify with constant-time comparison. |
| **`max_connections`** | `1–100` (default `40`) on cloud API; up to `100,000` on Local Bot API Server. |

---

## 4. Rate Limits & Paid Broadcasts

Source: [Bots FAQ](https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this) & [Paid Broadcasts](https://core.telegram.org/bots/api#paid-broadcasts)

| Scope | Rate Limit | Behavior When Exceeded |
|---|---|---|
| **Single Chat (Private or Group)** | **<= 1 message / second** (short bursts tolerated) | Returns HTTP `429 Too Many Requests` with `parameters.retry_after`. |
| **Single Group / Supergroup** | **<= 20 messages / minute** | Returns HTTP `429 Too Many Requests` with `parameters.retry_after`. |
| **Bulk / Passive Broadcasts (Free)** | **~30 messages / second** across different users | Returns HTTP `429 Too Many Requests`. |
| **Paid Broadcasts (Bot API 7.11+)** | Up to **1,000 messages / second** | Costs **0.1 Telegram Stars per message** above the free 30 msg/s tier. Requires enabling Paid Broadcasts in `@BotFather`, **>= 100,000 Stars** balance, **>= 100,000 MAU**, and passing `allow_paid_broadcast: true` on `send*` / `copyMessage`. |

---

## 5. File Upload & Download Rules & Local Bot API Server

Source: [Sending Files](https://core.telegram.org/bots/api#sending-files) & [Using a Local Bot API Server](https://core.telegram.org/bots/api#using-a-local-bot-api-server)

### 3 Ways to Send Files (`InputFile` or `String`)
1. **`file_id` (`String`):** Resend a file already on Telegram servers. **No file size limit.**
   - `file_id` is **persistent** per bot, but **cannot** be shared between different bots (`file_unique_id` is consistent across bots for deduplication, but cannot be used to download/send).
2. **HTTP URL (`String`):** Telegram downloads the file from the URL.
   - Max **5 MB** for photos, **20 MB** for other content (cloud API). Must have the correct MIME type.
3. **`multipart/form-data` Upload (`InputFile`):**
   - Cloud API limit: **50 MB** upload (`10 MB` max for photos sent via `sendPhoto`).
   - Local Bot API Server limit: **2,000 MB** (2 GB) upload.

### Cloud API vs. Local Bot API Server (`github.com/tdlib/telegram-bot-api`)

| Capability / Limit | Cloud API (`api.telegram.org`) | Local Bot API Server (`--local`) |
|---|---|---|
| **Max File Download (`getFile`)** | **20 MB** | **Unlimited** (up to Telegram's max file size, 2 GB / 4 GB Premium) |
| **Max File Upload** | **50 MB** | **2,000 MB** |
| **Local Path Upload** | Not supported | Supported via local path or `file://<path>` URI |
| **`getFile` Response (`file_path`)** | Relative path; must download within 1 hour via `https://api.telegram.org/file/bot<token>/<file_path>` | Returns **absolute local filesystem path** directly — zero second download step required |
| **Webhook URL** | `https://` only, IPv4 only, ports `443, 80, 88, 8443` | `http://` or `https://`, any IP (including `127.0.0.1`), **any port** |
| **`max_webhook_connections`** | `1–100` (default `40`) | Up to **`100,000`** |
| **Migration Requirement** | Default | Call `logOut` on cloud API first, then run `telegram-bot-api --local --api-id=<ID> --api-hash=<HASH> --http-port=8081` (use `close` before moving a local instance to another server). |

---

## 6. Common Bot API Error Codes & Fixes

| HTTP Code | Typical `description` Substring | Meaning & Action |
|---|---|---|
| `400` | `Bad Request: chat not found` | User has never started the bot (`t.me/<bot>?start=...`), or bot is not in the group/channel. |
| `400` | `Bad Request: message is not modified` | `editMessageText` / `editMessageReplyMarkup` called with identical text and markup. Ignore or check diff before calling. |
| `400` | `Bad Request: can't parse entities` | Unescaped reserved character in `MarkdownV2`/`Markdown` or unclosed/unsupported HTML tag. |
| `400` | `Bad Request: query is too old and response timeout expired` | `answerCallbackQuery` (> ~30s) or `answerPreCheckoutQuery` (> 10s) called too late. |
| `400` | `Bad Request: group chat was upgraded to a supergroup chat` | Read `parameters.migrate_to_chat_id` and update stored `chat_id`. |
| `400` | `Bad Request: INPUT_MEDIA_WIDGET_TOO_LARGE` / `HTML_INVALID` | Bot API 10.4 widget HTML > 32,768 bytes raw, > 4,096 bytes zlib-9 compressed, or contains `U+0000` NUL. |
| `401` | `Unauthorized` | Invalid or revoked bot token. |
| `403` | `Forbidden: bot was blocked by the user` | User blocked the bot in private chat; mark user inactive in DB and stop sending. |
| `403` | `Forbidden: bot was kicked from the supergroup chat` | Bot was removed from the group/channel. |
| `403` | `Forbidden: bot can't initiate conversation with a user` | Bots cannot DM users first unless the user clicked Start, approved a `chat_join_request`, or granted `requestWriteAccess` in a Mini App. |
| `409` | `Conflict: terminated by other getUpdates request` | Two long-polling instances are running simultaneously with the same token, or a webhook is active. |
| `429` | `Too Many Requests: retry after X` | Rate limit hit. Sleep for `parameters.retry_after` seconds before retrying. |
