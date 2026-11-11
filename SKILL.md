---
name: telegram-api-skill
description: Build, debug, and review Telegram bots, Mini Apps (WebApps), In-Chat HTML Widgets (Bot API 10.4), Rich Messages, Telegram Stars payments, Business & Managed Bots, Guest Mode bots, Telegram Serverless apps, and MTProto (Layer 225) clients or userbots. Use whenever the user mentions Telegram, Bot API, MTProto, Mini Apps, WebApp, TelegramWidget, sendWidget, sendRichMessage, BotFather, Telegram Stars, XTR, grammY, Telegraf, aiogram, python-telegram-bot, Telethon, Pyrogram, Kurigram, GramJS, TDLib, or t.me / tg:// deep links.
---

# Telegram Bot API (v10.4) & MTProto (Layer 225) Skill

Authoritative reference and engineering workflow for building accurate, current Telegram bots, Mini Apps, In-Chat HTML Widgets, Telegram Serverless backends, and MTProto clients without guessing.

- **Verified Bot API Version:** **Bot API 10.4** (released November 9, 2026) - [Official Bot API Reference](https://core.telegram.org/bots/api) | [Bot API Changelog](https://core.telegram.org/bots/api-changelog)
- **Verified MTProto Layer:** **Layer 225** ("Guest mode, Custom AI compose tones") - [Official TL Schema](https://core.telegram.org/schema) | [Layer Changelog](https://core.telegram.org/api/layers)
- **Verification Date:** November 11, 2026
- **Live Verification Rule:** Always verify against the live documentation at [core.telegram.org/bots/api](https://core.telegram.org/bots/api), [core.telegram.org/bots/api-changelog](https://core.telegram.org/bots/api-changelog), and [core.telegram.org/api/layers](https://core.telegram.org/api/layers) when a task depends on recent changes or experimental features. Never invent methods, fields, parameters, or limits; if a detail cannot be confirmed from primary documentation, mark it `UNVERIFIED` and consult `VERIFICATION_LOG.md`.

## When to Use

- Building or debugging a Telegram Bot using the HTTP Bot API (webhooks, long polling, Cloudflare Workers, Node.js, Deno, Python, Rust, Go, or Telegram Serverless)
- Creating Bot API 10.4 In-Chat HTML Widgets (`sendWidget`, `sendSharedWidget`, `answerWidgetQuery`, `editMessageWidgetData`, `editSharedWidgetData`, `window.TelegramWidget`)
- Streaming AI responses or sending structured Rich Messages (`sendRichMessage`, `sendRichMessageDraft`, `sendMessageDraft`, `MessageGenerationStopped`, 32,768-char limit)
- Sending Ephemeral Messages in groups or replacing callback messages privately (`EphemeralMessageParameters`, `editEphemeralMessage*`, `deleteEphemeralMessage`)
- Building Telegram Mini Apps (`window.Telegram.WebApp`, `initData` HMAC-SHA256 & Ed25519 validation, Fullscreen, Safe Areas, `DeviceStorage`, `SecureStorage`, `Serverless`, sensors, `requestChat`, `savePreparedInlineMessage`)
- Implementing monetization with Telegram Stars (`XTR`), digital/physical invoices, subscriptions, paid media (up to 25,000 Stars), paid broadcasts, regular/unique collectible gifts, suggested channel posts, or TON wallet widget queries
- Automating Business Accounts, Managed Bots (`getManagedBotToken`, `t.me/newbot/...`), Guest Mode bots (`answerGuestQuery`), or Bot-to-Bot communication
- Implementing or debugging MTProto clients, userbots, or custom protocol layers (Layer 225 TL schema, MTProto 2.0 AES-256-IGE, DH key exchange, SRP 2FA, `pts`/`qts`/`seq` updates, `upload.saveFilePart`/`getFile`, and peer ID conversions)

## Reference Router (Progressive Disclosure)

Read the specific reference file matching your task before writing code:

### 1. Architecture & Protocol Selection

- **Choosing between Bot API, MTProto, TDLib, Local Bot API Server, and Telegram Serverless:** Read `references/decision-guide.md`
- **Comparing client libraries (`grammY`, `Telegraf`, `aiogram`, `python-telegram-bot`, `Telethon`, `Pyrogram`/`Kurigram`, `GramJS`, `TDLib`):** Read `references/libraries.md`
- **Reviewing per-version changes (Bot API 6.0 through 10.4 & MTProto Layers 196 through 225):** Read `references/whats-new.md`
- **Auditing common bugs, anti-patterns, and edge cases:** Read `references/pitfalls.md`

### 2. Bot API Core & Reference (`references/bot-api/`)

- **Auth, HTTP formats, `Update` object (all 27 types), `getUpdates` vs `setWebhook`, rate limits, file upload/download limits, Local Bot API Server flags, error codes:** Read `references/bot-api/core-and-updates.md`
- **All 186 Bot API 10.4 methods (signatures, required/optional parameters, return types, version tags):** Read `references/bot-api/methods.md`
- **All 402 Bot API 10.4 types (grouped by domain with key fields and version tags):** Read `references/bot-api/types.md`

### 3. Feature Deep Dives (`references/`)

- **Rich text formatting, `MessageEntity` UTF-16 offset math, HTML vs MarkdownV2 escaping, expandable blockquotes, `<tg-time>` date/time entities, custom emoji, and Rich Messages (`sendRichMessage` / 32,768 chars):** Read `references/formatting.md`
- **Inline keyboards, reply keyboards, button styles/colors (`style`, `icon_custom_emoji_id`, `disabled`), `copy_text`, `request_users` / `request_chat` / `request_managed_bot`, `PreparedKeyboardButton`, callback data limits:** Read `references/keyboards-and-buttons.md`
- **Mini Apps (`window.Telegram.WebApp` full API, launch modes, `initData` validation, Fullscreen, Safe Areas, `DeviceStorage`, `SecureStorage`, `Serverless`, `LocationManager`, Biometrics, Motion sensors):** Read `references/mini-apps.md`
- **Bot API 10.4 In-Chat HTML Widgets (`sendWidget`, `window.TelegramWidget`, QuickJS sandbox, `chat_data` vs `public_data`, TON wallet queries), OIDC & Legacy Login Widgets, Web Widgets, and Deep Links (`t.me` & `tg://`):** Read `references/widgets-and-login.md`
- **Payments, Telegram Stars (`XTR`), subscriptions, paid media, paid broadcasts, regular & unique collectible gifts, Business Bots, Managed Bots, Guest Mode, Channel Direct Messages (Monoforums), Suggested Posts, and Checklists:** Read `references/payments-stars-business.md`
- **Webhooks, Cloudflare Workers edge hosting, Telegram Serverless (`tgcloud`), Local Bot API Server deployment, idempotency, flood-wait/429 handling, and broadcast queues:** Read `references/webhooks-and-hosting.md`

### 4. MTProto Technical Reference (`references/mtproto/`)

- **MTProto 2.0 architecture, TL binary serialization, boxed vs bare types, `auth_key` DH generation, AES-256-IGE encryption, `msg_id`/`seq_no`/salt, service messages, transports (Abridged, Intermediate, Padded, Full) & obfuscation:** Read `references/mtproto/protocol-and-transport.md`
- **User & Bot authorization (`auth.sendCode`, `auth.signIn`, QR login, Passkeys, OAuth), 2FA SRP (`passwordKdfAlgoSHA256SHA256PBKDF2HMACSHA512iter100000SHA256ModPow`), DC migration, parallel sessions (`tmp_sessions`), `invokeWithLayer(225)`:** Read `references/mtproto/auth-and-sessions.md`
- **Updates state machine (`pts`, `qts`, `seq`, `updates.getDifference`, `updates.getChannelDifference`), `min` constructors (`inputPeer*FromMessage`), Bot API dialog ID conversion (including Monoforum range `-4000000000000` to `-2002147483649`), file upload/download parts & `file_reference` refresh, and RPC errors:** Read `references/mtproto/updates-files-and-ids.md`

## Deterministic Helper Scripts (`scripts/`)

Run these tested Python 3 scripts directly to validate data or compute exact values:

- `python3 scripts/escape_markdown_v2.py "<text>"` - Escapes text for `MarkdownV2` (body, `pre`/`code`, or inline URL context).
- `python3 scripts/utf16_entity_offsets.py "<text>" "<substring>"` - Computes exact UTF-16 `offset` and `length` for `MessageEntity` objects and demonstrates byte-scan vs UTF-16 code unit calculation.
- `python3 scripts/validate_initdata.py --bot-token "$BOT_TOKEN" --init-data "<raw_init_data>"` - Verifies Mini App `initData` (HMAC-SHA256 with `"WebAppData"`) or Legacy Login Widget data (HMAC-SHA256 with `SHA256(bot_token)`).
- `python3 scripts/dialog_id_converter.py <id_or_type>` - Converts between MTProto peer IDs (`user`, `chat`, `channel`, `monoforum`, `secret_chat`) and Bot API dialog IDs.
- `python3 scripts/coverage_audit.py` - Audits the skill's documented Bot API 10.4 methods and types against the canonical index and updates `COVERAGE.md`.

## Runnable Examples (`examples/`)

- `examples/cloudflare-worker-grammy/` - TypeScript Cloudflare Worker handling webhooks (`X-Telegram-Bot-Api-Secret-Token`), Bot API 10.4 `sendWidget` / `answerWidgetQuery`, `sendRichMessage`, and Mini App `initData` HMAC-SHA256 verification.
- `examples/python-aiogram/` - Python 3 `aiogram` v3 bot demonstrating `MarkdownV2` expandable blockquotes, custom emoji, `<tg-time>` formatting, Stars (`XTR`) invoicing (`sendInvoice`, `answerPreCheckoutQuery`, `refundStarPayment`), and `sendMessageDraft` streaming.
- `examples/python-mtproto/` - Python 3 MTProto examples (`Telethon` and `Pyrogram`/`Kurigram`) showing 2FA login, `FloodWait` retry handling, and raw TL method invocation.

## Core Steps for Any Telegram Task

1. **Identify the surface:** Determine whether the user needs the HTTP Bot API, an In-Chat HTML Widget (`sendWidget`), a Mini App (`window.Telegram.WebApp`), Telegram Serverless (`tgcloud`), or raw MTProto / userbot capabilities (`references/decision-guide.md`).
2. **Load the domain reference:** Read the corresponding file in `references/` before writing code so parameter names, limits, and version-specific changes match Bot API 10.4 and MTProto Layer 225.
3. **Apply critical invariants:**
   - Never hard-code bot tokens, `api_hash`, or webhook secrets; always read from environment variables (`process.env.BOT_TOKEN`, `os.environ["BOT_TOKEN"]`, or Cloudflare Worker `env.BOT_TOKEN`).
   - Always include non-default update types (`callback_query`, `widget_query`, `shared_widget_query`, `message_reaction`, `chat_member`, `pre_checkout_query`) in `allowed_updates` when registering webhooks or polling.
   - Compute `MessageEntity` offsets and lengths in **UTF-16 code units**, never UTF-8 byte length or Unicode code point count.
   - Answer `pre_checkout_query` within **10 seconds** and only deliver goods after receiving the `successful_payment` message update.
   - Answer `callback_query` and `widget_query` promptly so the client loading spinner stops.

## Gotchas

- **Widgets vs Mini Apps vs Web Widgets:** Telegram uses "Widgets" for three distinct concepts:
  1. **In-Chat HTML Widgets (Bot API 10.4):** Self-contained HTML/CSS/JS bubbles (`<= 32 KB` raw, `<= 4,096 B` zlib level 9 compressed) sent via `sendWidget` and running offline inside a QuickJS sandbox via `window.TelegramWidget` ([core.telegram.org/bots/widgets](https://core.telegram.org/bots/widgets)). In production, `sendWidget` currently works only in private chats and automatically sets `has_protected_content`.
  2. **Mini Apps (WebApps):** Full hosted web applications launched in a WebView via `window.Telegram.WebApp` ([core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)). Since July 20, 2026 (Bot API 10.2), Mini App methods are blocked if called from an origin different from the registered Mini App domain.
  3. **Embeddable Web Widgets:** Login Widget (OIDC / legacy), Post Widget, Discussion Widget, and Share Button embedded on external websites ([core.telegram.org/widgets](https://core.telegram.org/widgets)).
- **Ephemeral Message Parameter Change (Bot API 10.3 & 10.4):** Bot API 10.2 introduced `receiver_user_id` and `callback_query_id` directly on `send*` methods, but **Bot API 10.3 replaced them** with `ephemeral_message_parameters` of type `EphemeralMessageParameters`. In Bot API 10.4, `receiver_user_id` inside `EphemeralMessageParameters` and `chat_id` on `send*` methods are optional when replying ephemerally to a `callback_query_id`.
- **Quiz Polls Parameter Change (Bot API 9.6):** `correct_option_id` was replaced by `correct_option_ids` (`Array of Integer`) on `Poll` and `sendPoll` to support multi-answer quizzes, and minimum poll options decreased from 2 to 1 in Bot API 10.0.
- **Business Connection Rights Change (Bot API 9.0 & 10.0):** `BusinessConnection.can_reply` was replaced by `BusinessConnection.rights` (`BusinessBotRights`) in Bot API 9.0. Since Bot API 10.0, users no longer need Telegram Premium to connect a Business Bot.
- **Bot API Dialog ID Range Expansion (Layer 214 / 225):** The valid Bot API dialog ID range is now `-4000000000000` to `1099511627775` (expanded from `-2002147483648` to support Monoforum / Channel Direct Messages IDs in `-4000000000000` to `-2002147483649`). Never reject IDs below `-2002147483648`.
