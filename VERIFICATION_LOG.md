# Verification Log & Discrepancy Audit (`VERIFICATION_LOG.md`)

**Verification Date:** November 11, 2026  
**Verified Against:** Telegram Bot API **10.4** (released November 9, 2026) and MTProto **Layer 225**

This log records:
1. Primary-source verifications and corrections of common assumptions
2. Documentation vs. actual runtime behavior discrepancies confirmed via official docs and `tdlib/telegram-bot-api` maintainer statements
3. Items explicitly marked `UNVERIFIED` in accordance with Rule #2 ("Never invent anything. If you can't verify something, write `UNVERIFIED` and list it in `VERIFICATION_LOG.md`")
4. Results of the 10-task Phase 5 self-review evaluation

---

## 1. Confirmed Facts & Version Verifications

| Claim / Topic | Status | Evidence & Primary Source |
|---|---|---|
| Latest Bot API version is **10.4** (released Nov 9, 2026) | **VERIFIED** | Confirmed directly from [https://core.telegram.org/bots/api-changelog](https://core.telegram.org/bots/api-changelog) and [https://core.telegram.org/bots/api](https://core.telegram.org/bots/api). |
| Bot API 10.3 release date & exact feature list | **VERIFIED** | Released August 24, 2026. Full changelog retrieved from [https://core.telegram.org/bots/api-changelog](https://core.telegram.org/bots/api-changelog): added `RichMessageButton`, `RichTextButton`, `RichBlockButtons`/`InputRichBlockButtons`, `is_compact` on `RichBlockTable`, `RichBlockExpandableBlockQuotation`, `RichBlockDocument`, `tg://document?id=`, `EphemeralMessageParameters` (replacing raw `receiver_user_id`/`callback_query_id` params from 10.2), `DisabledButton`, `force_reply` on `InlineKeyboardMarkup`/`ReplyKeyboardMarkup`, `can_stop`/`keep_on_stop` on `sendMessageDraft`/`sendRichMessageDraft`, `MessageGenerationStopped`, `CommunityChatJoined`. |
| Latest MTProto layer is **Layer 225** | **VERIFIED** | Confirmed from [https://core.telegram.org/schema](https://core.telegram.org/schema) (`225 – Guest mode, Custom AI compose tones`) and [https://core.telegram.org/api/layers](https://core.telegram.org/api/layers). Third-party blog claims of "Layer 86+" or Rust crates showing `layer_223` are outdated. |
| Bot API dialog ID range expansion (`-4000000000000` to `1099511627775`) | **VERIFIED** | Confirmed in [https://core.telegram.org/api/bots/ids](https://core.telegram.org/api/bots/ids) and [https://core.telegram.org/api/layers](https://core.telegram.org/api/layers) (Layer 214): Monoforum (channel direct messages) IDs occupy `-4000000000000` to `-2002147483649` inclusive. |
| Business Bots no longer require Telegram Premium | **VERIFIED** | Confirmed in Bot API 10.0 changelog ([https://core.telegram.org/bots/api-changelog](https://core.telegram.org/bots/api-changelog), May 8, 2026) and [https://core.telegram.org/api/bots/connected-business-bots](https://core.telegram.org/api/bots/connected-business-bots): *"Connecting a business bot does not require Telegram Premium."* |
| In-Chat HTML Widgets (`sendWidget`) production restrictions | **VERIFIED** | Confirmed in both [https://core.telegram.org/bots/api-changelog](https://core.telegram.org/bots/api-changelog) (Bot API 10.4) and [https://core.telegram.org/bots/widgets](https://core.telegram.org/bots/widgets): in production, widgets can currently only be sent to private chats with the bot, automatically have protected content (cannot be forwarded), and cannot be sent via inline queries (groups, inline mode, and forwards work on the test server). |
| Mini App origin hardening (July 20, 2026) | **VERIFIED** | Confirmed in Bot API 10.2 changelog ([https://core.telegram.org/bots/api-changelog](https://core.telegram.org/bots/api-changelog), July 14, 2026): Mini App methods are disallowed from origins different from the original Mini App domain (auto-enabled July 20, 2026; opt-out via `@BotFather` Mini App). |
| Telegram Serverless (`tgcloud`) native platform | **VERIFIED** | Confirmed from [https://core.telegram.org/bots/serverless](https://core.telegram.org/bots/serverless) (updated October 6, 2026): official V8 isolate runtime + SQLite database + Mini App static hosting (`https://app<app_id>.tgcloud.ai/`) + `Telegram.WebApp.Serverless.call()`. |

---

## 2. Documentation vs. Runtime Behavior Discrepancies

1. **"30 messages per second" Global Limit Myth vs. Actual Server Behavior**
   - **Common Misconception:** Many tutorials state that a bot has a hard global limit of 30 API calls/second across all users, or that running multiple Local Bot API servers multiplies the rate limit.
   - **Verified Maintainer Clarification ([tdlib/telegram-bot-api#309](https://github.com/tdlib/telegram-bot-api/issues/309), [#523](https://github.com/tdlib/telegram-bot-api/issues/523), [#570](https://github.com/tdlib/telegram-bot-api/issues/570), and [Bots FAQ](https://core.telegram.org/bots/faq)):** TDLib author `levlam` confirmed that *"Local server has nothing to do with bot limits. Also, there is no such limit as '30 messages per second', only sending a lot of 'passive alerts' is limited."* Specifically:
     - Replying to incoming user commands/messages in active 1-on-1 conversations scales higher than 30/sec, provided per-chat limits (~1 msg/sec) are respected.
     - Bulk/passive notifications (broadcasts) are capped at ~30 messages/second unless Paid Broadcasts (`allow_paid_broadcast=True`, 0.1 Stars/msg, up to 1,000 msgs/sec) are enabled.
     - A single bot token can only be connected to **one** Bot API server instance at a time (either `api.telegram.org` or one self-hosted `telegram-bot-api` server).
2. **`getFile` Rate Limits on High-Volume Bots**
   - **Verified Maintainer Clarification ([tdlib/telegram-bot-api#755](https://github.com/tdlib/telegram-bot-api/issues/755)):** Running a Local Bot API server does not remove Telegram's server-side rate limits on `getFile`; total concurrent download bandwidth/size per bot instance is bounded by Telegram's datacenters.
3. **Large Channel Video Sending Returns `message_id: 0` (Bot API 7.11 / 8.0 Warning)**
   - **Official Warning ([Bot API Changelog](https://core.telegram.org/bots/api-changelog)):** Since December 1, 2024, videos sent, copied, or forwarded to groups and channels with a sufficiently large audience can be automatically scheduled by the server until re-encoded. The returned `Message` object has `message_id: 0` and cannot be edited, pinned, or referenced until the video is actually published.
4. **MTProto Older Layer Constructors Returned on High-Load Channels**
   - **Official Documentation Note ([Layer 214 Changelog](https://core.telegram.org/api/layers)):** In some cases (such as updates from big channels), the MTProto API may return constructors from older layers different from the connection's negotiated `invokeWithLayer` version. Clients must treat an unknown/older constructor in an update as a `500` server error: close and reopen the TCP socket, re-initialize the session with `initConnection`, and call `updates.getDifference`.
5. **Ephemeral Message Signature Breaking Change Between 10.2 and 10.3**
   - **Official Changelog Diff ([Bot API Changelog](https://core.telegram.org/bots/api-changelog)):** Bot API 10.2 (July 14, 2026) added `receiver_user_id` and `callback_query_id` directly to `sendMessage`, `sendPhoto`, etc. Just 41 days later, Bot API 10.3 (August 24, 2026) **replaced** those two parameters with a single `ephemeral_message_parameters` object (`EphemeralMessageParameters`). Code written for 10.2 using top-level `receiver_user_id` will fail on 10.3/10.4; always use `ephemeral_message_parameters`.
6. **Quiz `correct_option_id` vs `correct_option_ids` Breaking Change (Bot API 9.6)**
   - **Official Changelog Diff ([Bot API Changelog](https://core.telegram.org/bots/api-changelog)):** Bot API 9.6 (April 3, 2026) replaced `correct_option_id` (`Integer`) with `correct_option_ids` (`Array of Integer`) on `Poll` and `sendPoll`.

---

## 3. Explicitly `UNVERIFIED` Items Log

In strict compliance with Rule #2, the following items could not be confirmed from primary official Telegram documentation or verified release tags during this research pass and are marked `UNVERIFIED`:

| Item | Why It Is `UNVERIFIED` | How to Verify / Mitigate |
|---|---|---|
| **Exact `tdlib/telegram-bot-api` Git commit hash / release tag for Bot API 10.4** | Bot API 10.4 was released on November 9, 2026 (2 days prior to verification). While the cloud endpoint `https://api.telegram.org` runs 10.4 live, the exact GitHub release tag on [github.com/tdlib/telegram-bot-api](https://github.com/tdlib/telegram-bot-api) was not confirmed in search snippets. | Check `git log -1` on `https://github.com/tdlib/telegram-bot-api` or call `getMe` / test `sendWidget` against your local server binary before using 10.4-only methods on self-hosted instances. |
| **Exact `grammY` npm version number supporting Bot API 10.4** | [github.com/grammyjs/grammy](https://github.com/grammyjs/grammy) main branch and README were verified, but the exact npm version number published between Nov 9–11, 2026 for Bot API 10.4 types was not returned. | In `grammY`, any newer Bot API 10.4 method (`sendWidget`, `sendRichMessage`, etc.) can be invoked immediately via `bot.api.raw.sendWidget({ ... })` even before `@grammyjs/types` is bumped. |
| **Exact `python-telegram-bot` v22.8 Bot API version ceiling** | Release `22.8` (dated Nov 9, 2026) is confirmed to require Python 3.11+, but whether it targets Bot API 10.3 or 10.4 was not confirmed from its release body. | Use `await bot.post(method_name, data)` or raw request helpers if a 10.4 method is missing on ` telegram.Bot`. |
| **Exact `aiogram` release after `3.30.0` (July 17, 2026)** | `aiogram` `3.30.0` is confirmed (supporting ~Bot API 10.1/10.2, fixing the `3.29.0` yanked `RichBlock` slowdown). Support for 10.3/10.4 in a newer minor release is `UNVERIFIED`. | In `aiogram` 3.x, call `await bot(TelegramMethod(...))` or raw session calls for 10.4 methods (`sendWidget`, `answerWidgetQuery`). |
| **Exact MTProto Layer in `Kurigram` / `Pyrogram` forks & `Telethon` post-GitHub migration** | `Telethon` migrated its repository off GitHub on Feb 21, 2026 (shortly after Layer 222 commit on Feb 7, 2026); `gram-js/gramjs` was archived on July 14, 2026 (at Layer ~196). Exact Layer 225 coverage in external forks is `UNVERIFIED`. | Use raw TL schema compilation or TDLib when Layer 225 constructors (`aicompose.*`, `messages.setBotGuestChatResult`, `bots.getAccessSettings`) are required. |

---

## 4. Phase 5 Self-Review: 10 Realistic Tasks Test Log

Each task was tested against the skill's reference files and validated using the bundled scripts/examples in the sandbox VM:

| # | Realistic Agent Task | Target Reference & Script Used | Result |
|---|---|---|---|
| 1 | Send a `MarkdownV2` message with an expandable blockquote, custom emoji, and `<tg-time>` / `date_time` entity | `references/formatting.md` + `scripts/escape_markdown_v2.py` | **PASS** — Verified `>**Header**\n>Line 1\n>Line 2||` syntax (ending with `||`), `![👍](tg://emoji?id=5368324170671202286)` custom emoji syntax, and `<tg-time unix="1647531900" format="wDT">...</tg-time>` HTML syntax. |
| 2 | Validate Mini App `initData` in a Cloudflare Worker using Web Crypto API | `references/mini-apps.md` + `examples/cloudflare-worker-grammy/src/index.js` + `scripts/validate_initdata.py` | **PASS** — Verified `HMAC-SHA256(key="WebAppData", data=bot_token)` secret derivation, alphabetical `key=value\n` sorting (excluding `hash`), constant-time hex comparison, and `auth_date` expiration check. |
| 3 | Send an interactive Bot API 10.4 In-Chat HTML Widget (`sendWidget`) and handle `widget_query` + update state | `references/widgets-and-login.md` + `examples/cloudflare-worker-grammy/src/index.js` | **PASS** — Verified `sendWidget` payload (`html` <= 32 KB / <= 4 KB zlib-9, `allow_queries: true`, `chat_data`, `public_data`), client `TelegramWidget.request()`, `answerWidgetQuery`, and `editMessageWidgetData` (never mutating state inside `answerWidgetQuery`). |
| 4 | Stream an AI response using `sendMessageDraft` / `sendRichMessageDraft` and handle user pressing Stop | `references/formatting.md` + `references/whats-new.md` + `examples/python-aiogram/bot.py` | **PASS** — Verified `sendMessageDraft` with `can_stop=True`, `keep_on_stop=True`, empty text / `<tg-thinking>` placeholder, `stopped_message_generation` (`MessageGenerationStopped`) update handling, and final `sendRichMessage` (up to 32,768 chars). |
| 5 | Create a Telegram Stars (`XTR`) invoice, handle `pre_checkout_query` within 10s, and issue a refund | `references/payments-stars-business.md` + `examples/python-aiogram/bot.py` | **PASS** — Verified `currency="XTR"`, `provider_token=""`, `LabeledPrice(label=..., amount=stars)`, `answerPreCheckoutQuery` within 10s, `successful_payment.telegram_payment_charge_id` storage, and `refundStarPayment`. |
| 6 | Send an ephemeral group message or ephemeral callback reply in Bot API 10.4 | `references/bot-api/methods.md` + `references/whats-new.md` | **PASS** — Verified `ephemeral_message_parameters={"callback_query_id": ..., "replace_callback_query_message": True}` (with optional `receiver_user_id` and `chat_id` in 10.4). |
| 7 | Compute exact UTF-16 `offset` and `length` for `MessageEntity` over text containing supplementary-plane emojis | `references/formatting.md` + `scripts/utf16_entity_offsets.py` | **PASS** — Tested via `python3 scripts/utf16_entity_offsets.py`; verified surrogate pairs (`U+10000..U+10FFFF`) count as 2 UTF-16 code units and trailing whitespace is stripped from entity length. |
| 8 | Log in a user via MTProto with 2FA (`SESSION_PASSWORD_NEEDED`) using SRP 6a | `references/mtproto/auth-and-sessions.md` + `examples/python-mtproto/telethon_userbot.py` | **PASS** — Verified both high-level `Telethon` 2FA flow (`SessionPasswordNeededError` -> `client.sign_in(password=...)`) and low-level `account.getPassword` -> `PH1`/`PH2` 100,000-iteration PBKDF2-SHA512 -> `M1` -> `auth.checkPassword(InputCheckPasswordSRP)`. |
| 9 | Handle `FloodWait` / HTTP 429 in a bulk broadcast with Paid Broadcasts support | `references/webhooks-and-hosting.md` + `references/pitfalls.md` | **PASS** — Verified reading `parameters.retry_after` (Bot API 429) or `FLOOD_WAIT_X` (MTProto 420), token-bucket queueing (~30 msg/s free, up to 1,000 msg/s with `allow_paid_broadcast=True`), and per-chat 1 msg/s pacing. |
| 10 | Convert between MTProto Peer IDs (including Monoforums) and Bot API Dialog IDs | `references/mtproto/updates-files-and-ids.md` + `scripts/dialog_id_converter.py` | **PASS** — Tested via `python3 scripts/dialog_id_converter.py`; verified User (`1..1099511627775`), Chat (`-999999999999..-1`), Channel/Supergroup (`-1997852516352..-1000000000001`), Secret Chat (`-2002147483648..-1997852516353`), and Monoforum (`-4000000000000..-2002147483649`). |
