---
name: telegram-api-skill-custom
description: Build, debug, and review Telegram bots, Mini Apps, In-Chat HTML Widgets (Bot API 10.4), Rich Messages, Stars payments, Business/Managed Bots, and MTProto (Layer 225) clients. Condensed zero-code system skill with quick rules, limits, and formulas. Use whenever the user mentions Telegram, Bot API, MTProto, WebApp, sendWidget, BotFather, Stars, XTR, grammY, aiogram, Telethon, Pyrogram, TDLib, or t.me deep links.
---

# Telegram Bot API 10.4 & MTProto Layer 225 — System Custom Skill (Condensed, Code-Free)

**Verified Against:** Bot API **10.4** (Nov 9, 2026) | MTProto **Layer 225** | Verified **Nov 11, 2026** — Coverage: **186/186 methods**, **402/402 types**, 38/38 changelog releases.

This is the lightweight system-skill edition: quick rules, limits, and formulas only — **no executable code** (safe for Gemini Custom Skills and any platform that rejects scripts). Field-level parameter tables, full signatures, and runnable sources live in the repository: `SKILL-single-file.md` (everything in one file) or `references/` + `scripts/` + `examples/`. Consult those before writing anything beyond one-shot snippets.

## 1. How to Use This Skill

- Find the relevant section below **before** coding. Everything here is authoritative; when a parameter is not listed, look it up in `SKILL-single-file.md` **Part 4 (methods)** / **Part 5 (types)** — never guess names, fields, or limits.
- For very recent or experimental behavior, verify against live docs: core.telegram.org/bots/api, /bots/api-changelog, /api/layers. Unconfirmed details must be marked `UNVERIFIED`.
- Prefer `parse_mode: "HTML"` or explicit `entities`; use `MarkdownV2` only with context-aware escaping (Section 6).
- All five helper utilities exist in `scripts/` (usage one-liners in Section 15): UTF-16 offsets, MarkdownV2 escaping, initData validation, dialog-ID conversion, coverage audit. Run them instead of hand-rolling math.

## 2. Hard Invariants (Always Apply)

1. **Never** hard-code bot tokens, `api_id`/`api_hash`, or webhook secrets — read from environment (`process.env.BOT_TOKEN`, `os.environ["BOT_TOKEN"]`, `env.BOT_TOKEN`).
2. Include non-default update types in `allowed_updates` — see the critical rule in Section 4.
3. Compute `MessageEntity.offset`/`length` in **UTF-16 code units**, never UTF-8 bytes or code-point count: `len(text.encode("utf-16-le")) // 2` (each non-BMP emoji counts 2, not 1).
4. Answer `pre_checkout_query` within **10 seconds** (ideally < 1 s); fulfill only after `message.successful_payment` arrives. Store `telegram_payment_charge_id` for idempotency/refunds.
5. Always call `answerCallbackQuery` / `answerWidgetQuery` on every interaction, or the client spinner spins 30+ s.
6. `callback_data` is **1–64 bytes**: use compact tokens (`act:buy:4812`), store payloads in KV/DB keyed by short ID.
7. Never call `getUpdates` while a webhook is active (`409 Conflict`) — `deleteWebhook` first, or use a staging bot.
8. Handle `429` by sleeping `parameters.retry_after` seconds; handle `400` group-upgrade via `parameters.migrate_to_chat_id`; on `403 bot was blocked` mark the user inactive — never retry.

## 3. Architecture Decision Matrix

| Need | Stack | Why |
|---|---|---|
| Standard bot, Mini App backend, Stars, widgets, files ≤ 50 MB up / 20 MB down | **Hosted Bot API** (Cloudflare Workers + grammY, aiogram 3.x, any VPS) | Zero state, instant webhooks |
| No hosting bills, pay with Stars | **Telegram Serverless** (`tgcloud`, V8 isolates, built-in SQLite, WASI components) | Hosted by Telegram, `sdk` modules only |
| Large files (20 MB–4 GB), full member list up to 9,999 via `getChat` | **Local Bot API Server** (`tdlib/telegram-bot-api --local`) | 2,000 MB upload / 4,000 MB download, absolute local file paths |
| Read history before join, search globally, join channels by invite, automate a **user** account | **MTProto** (Telethon, Pyrogram/Kurigram, GramJS) or **TDLib** | Full user-account power, strict anti-spam/ToS rules apply |
| Cross-platform client app with native sessions | **TDLib** (`td_api.tl`) | Maintained by Telegram, handles updates/encryption |

## 4. Requests, Updates & Webhooks

- Endpoint: `https://api.telegram.org/bot<token>/<METHOD>` (test env: insert `/test/` after `bot<token>`; files: `/file/bot<token>/<file_path>`). GET or POST, UTF-8, case-insensitive method names. JSON encoding recommended; `multipart/form-data` required for binary uploads (`attach://<name>` for refs).
- Every response: `ok`, `result`, optional `description`, optional `parameters` (`migrate_to_chat_id`, `retry_after`).
- Webhook HTTP replies may carry `"method": "<NAME>"` + params, but you get **no return value** that way.
- Updates are stored **24 h**; `getUpdates` and `setWebhook` are mutually exclusive.
- **Critical `allowed_updates` rule:** an empty array subscribes to all **except** `chat_member`, `message_reaction`, `message_reaction_count`; a previously-set custom list silently withholds new types — always explicitly list `widget_query`, `shared_widget_query`, `pre_checkout_query`, `chat_member`, `message_reaction`, `message_reaction_count`, `purchased_paid_media`, `subscription`, `managed_bot`, `guest_message`, `stopped_message_generation` when needed. A `Update` object carries **at most one** event field (plus `update_id`); 27 event types exist in 10.4.
- Webhook requirements: **IPv4 only**; ports `443, 80, 88, 8443`; TLS 1.2+; Telegram source subnets `149.154.160.0/20` and `91.108.4.0/22`; `secret_token` (1–256 chars of `A-Za-z0-9_-`) arrives in header `X-Telegram-Bot-Api-Secret-Token` — verify with **constant-time** comparison before parsing; `max_connections` 1–100 (default 40).
- Edge runtimes: register slow work with `ctx.waitUntil(...)` and return `200 OK` immediately; deduplicate `update_id` (Telegram retries the same update after failures/5xx).

## 5. Rate Limits, File Limits & Error Recovery

| Scope | Limit |
|---|---|
| Same private chat / group member | ≤ 1 msg/s (bursts tolerated) |
| Same group / supergroup | ≤ 20 msg/min |
| Free bulk broadcast | ~30 msg/s total |
| Paid broadcast (`allow_paid_broadcast: true`, 7.11+) | up to 1,000 msg/s at **0.1 Stars/msg**; needs BotFather enablement, ≥ 100,000 Stars balance, ≥ 100,000 MAU |

| Path | Upload | Download |
|---|---|---|
| Cloud API | 50 MB (photos 10 MB); by URL 20 MB (photos 5 MB) | 20 MB, link valid 1 h |
| Local Bot API Server | 2,000 MB | 4,000 MB, absolute local path returned |
| MTProto (user, Premium) | 2,000 MB (4,000 MB) | 4,000 MB |
| `file_id` resend | no size limit (per-bot, never cross-bot) | — |

Quick fixes: `400 chat not found` → user never started bot / bot missing from chat; `400 message is not modified` → identical edit, diff first; `400 can't parse entities` → bad MarkdownV2/HTML escaping; `400 query is too old` → answer callbacks ≤ ~30 s, pre-checkout ≤ 10 s; `400 INPUT_MEDIA_WIDGET_TOO_LARGE` / `HTML_INVALID` → widget > 32,768 B raw or > 4,096 B zlib-9 or contains NUL; `401 Unauthorized` → bad token; `403 blocked` → stop messaging that user; `409 Conflict` → polling/webhook clash; `429` → sleep `retry_after`. Text messages ≤ 4,096 chars; captions ≤ 1,024 (media groups 2,048 per caption with 10 items).

## 6. Formatting Quick Rules

- **HTML:** escape only `<`, `>`, `&` in body text. Supports bold/italic/underline/strikethrough/spoiler, `blockquote` (+ `expandable`), `code`/`pre`, `a href`, `tg-emoji`, `tg-time` (`unix`, `format`), custom emoji via `tg://emoji?id=...`.
- **MarkdownV2:** outside code/links escape **all 18 characters** `_ * [ ] ( ) ~ \` > # + - = | { } . !` plus backslash; inside `code`/`pre` escape only backtick and backslash; inside `(…)` link URLs escape only `)` and backslash. Legacy `"Markdown"` is deprecated — avoid.
- **Entities array:** passing explicit `entities` beats `parse_mode` for precision; offsets in UTF-16 (Section 2.3).
- **Rich Messages (10.1–10.4):** `sendRichMessage` / `sendRichMessageDraft`; ≤ **32,768 chars**; blocks (header, paragraph, preformatted, list, blockquote, pullquote, table, details, slideshow, collage, embed-post, related-articles) + buttons; streaming via drafts with `MessageGenerationStopped` update.

## 7. Mini App & Login Widget Verification (Do Not Mix!)

- **Mini App `initData`:** take the **raw** `window.Telegram.WebApp.initData` string (never `initDataUnsafe`); build `data_check_string` from all fields except `hash` sorted alphabetically as `key=value` lines joined by newlines; compute `secret_key = HMAC_SHA256(key="WebAppData", msg=bot_token)`; valid iff `hex(HMAC_SHA256(key=secret_key, msg=data_check_string)) == hash`. Also check `now - auth_date ≤ 86400`. Ed25519 third-party validation: verify `signature` with Telegram's public key `e7bf03a2fa4602af4580703d88dda5bb59f32ed8b02a56c187fe7d34caed242d` over the UTF-8 string of `bot_id + ":WebAppData\n" + data_check_string`.
- **Login Widget:** `secret_key = SHA256(bot_token)` instead — using the Mini App formula here (or vice versa) fails every check.
- Mini App platform: since **July 20, 2026 (10.2)**, methods are blocked from origins other than the registered Mini App domain; full SDK (`Telegram.WebApp`) incl. Fullscreen, Safe Areas, Biometrics, `DeviceStorage`/`SecureStorage`, sensors, `requestChat`, `savePreparedInlineMessage` — details in Part 8 / single-file Part 8.

## 8. In-Chat HTML Widgets (Bot API 10.4)

- Methods: `sendWidget(chat_id, url, aspect_ratio, data)`, `sendSharedWidget`, `answerWidgetQuery(widget_query_id, ...)`, `editMessageWidgetData`, `editSharedWidgetData`.
- Limits: HTML ≤ 32,768 bytes raw / ≤ 4,096 bytes zlib level 9; no NUL; sandboxed QuickJS (`window.TelegramWidget`) — no `localStorage`, no cookies, no network unless `#allow-same-origin` + `_telegram-widget.<domain>` TXT record verified.
- Include `<meta name="telegram-widget-origins" content="https://yourdomain.com">`; pass state via widget `data` + `TelegramWidget.onDataUpdated`; trigger queries via `TelegramWidget.sendQuery(payload)`; answer with `answerWidgetQuery` (optionally with `EphemeralMessageParameters`).
- Production: works only in **private chats**, auto-sets `has_protected_content`; forwarded shared widgets arrive as `shared_widget_query`.
- TON wallet query types: `WidgetQueryWallet` with `TonWalletCard` / `TonWalletTransfer` (+ `TonNft` attributes) — see Part 5 / single-file Part 5.

## 9. Payments, Stars & Business Quick Rules

- Stars invoices: `currency="XTR"`, **omit `provider_token`**, prices in Stars; `createInvoiceLink` for links; subscriptions `subscription_period=2592000` (30 days); refunds via `refundStarPayment`; balance/transactions via `getMyStarBalance`, `getStarTransactions`; subscriptions managed via `editUserStarSubscription`.
- `pre_checkout_query`: answer within 10 s (Section 2.4); shipping queries only when `is_flexible=True`.
- Paid media: up to **25,000 Stars** per item (`sendPaidMedia`); purchased events via `purchased_paid_media`.
- Gifts: `getAvailableGifts`, `sendGift`, `getUniqueGift`/`upgradeGift`/`transferGift`/`convertGiftToStars`, gift resale/suggested posts via Suggested Post APIs (`approveSuggestedPost`, `declineSuggestedPost`).
- Business: connect via Business accounts; `BusinessConnection.rights` (replaced `can_reply` in 9.0); no Premium required since 10.0; read/update business profile via `setBusinessAccount*`; managed bots via `getManagedBotToken` / `replaceManagedBotToken` (update type `managed_bot`, 9.6+); Guest Mode via `guest_message` + `answerGuestQuery` (10.0+); Monoforum DM channels + `setChatDirectMessagesPrice` (10.x).

## 10. MTProto (Layer 225) Quick Rules

- Always wrap with `invokeWithLayer(225)` (+ `initConnection`). Transports: Abridged / Intermediate / Padded / Full, optionally AES-256-CTR obfuscated. MTProto 2.0: DH `auth_key` exchange, AES-256-IGE, `msg_id` monotonic per DC, salt rotation.
- Auth: `auth.sendCode` → `auth.signIn`; 2FA = SRP 6a (`passwordKdfAlgoSHA256SHA256PBKDF2HMACSHA512iter100000SHA256ModPow`); QR login; persist session strings — never share one `auth_key` across IPs (`406 AUTH_KEY_DUPLICATED`); test only on Test DCs (`99966XYYYY`, code `XXXXX`).
- Updates: state machine `pts`/`qts`/`seq` + `updates.getDifference` / `getChannelDifference`; `updateMessageID` remaps temporary IDs.
- Files: `upload.saveFilePart` / `saveBigFilePart` (512 KB parts), `upload.getFile`; on `400 FILE_REFERENCE_EXPIRED` re-fetch the container message (`messages.getMessages` / `channels.getMessages`) to refresh `file_reference`.
- Userbot safety: never cold-DM or bulk-invite (`PEER_FLOOD`, bans), obey `FLOOD_WAIT_X` (pause X seconds), avoid auth loops in CI. Bot API dialog-ID math: `bot_api_chat_id = -1000000000000 - channel_id` for channels; standard channels `−1997852516352..−1000000000001`; **Monoforums `−4000000000000..−2002147483649`**; valid Bot API dialog range is now `−4000000000000..1099511627775` — never reject IDs below `−2002147483648`. Users: id as-is; basic groups: `−id`; secret chats: `−1000000000000 - id` — details in Part 15 / single-file Part 15.

## 11. Complete Method Catalog (186, by category)

- **Getting Updates (4):** `getUpdates`, `setWebhook`, `deleteWebhook`, `getWebhookInfo`
- **Bot Identity & Config (3):** `getMe`, `logOut`, `close`
- **Sending Messages (6):** `sendMessage`, `sendEphemeralMessage`, `forwardMessage`, `forwardMessages`, `copyMessage`, `copyMessages`
- **Sending Media (9):** `sendPhoto`, `sendAudio`, `sendDocument`, `sendVideo`, `sendAnimation`, `sendVoice`, `sendVideoNote`, `sendPaidMedia`, `sendMediaGroup`
- **Location & Contacts (3):** `sendLocation`, `sendVenue`, `sendContact`
- **Polls, Checklists & Dice (3):** `sendPoll`, `sendChecklist`, `sendDice`
- **Drafts, Actions & Reactions (3):** `sendMessageDraft`, `sendChatAction`, `setMessageReaction`
- **In-Chat HTML Widgets (3):** `sendWidget`, `sendSharedWidget`, `answerWidgetQuery`
- **Users, Profiles & Files (4):** `getUserProfilePhotos`, `getUserProfileAudios`, `setUserEmojiStatus`, `getFile`
- **Chat Member Moderation (8):** `banChatMember`, `unbanChatMember`, `restrictChatMember`, `promoteChatMember`, `setChatAdministratorCustomTitle`, `setChatMemberTag`, `banChatSenderChat`, `unbanChatSenderChat`
- **Chat Settings & Invite Links (16):** `setChatPermissions`, `exportChatInviteLink`, `createChatInviteLink`, `editChatInviteLink`, `createChatSubscriptionInviteLink`, `editChatSubscriptionInviteLink`, `revokeChatInviteLink`, `approveChatJoinRequest`, `declineChatJoinRequest`, `setChatPhoto`, `deleteChatPhoto`, `setChatTitle`, `setChatDescription`, `pinChatMessage`, `unpinChatMessage`, `unpinAllChatMessages`
- **Chat Info & Queries (8):** `leaveChat`, `getChat`, `getChatAdministrators`, `getChatMemberCount`, `getChatMember`, `getChatShareThemeBackdrops`, `setChatStickerSet`, `deleteChatStickerSet`
- **Forum Topics (13):** `getForumTopicIconStickers`, `createForumTopic`, `editForumTopic`, `closeForumTopic`, `reopenForumTopic`, `deleteForumTopic`, `unpinAllForumTopicMessages`, `editGeneralForumTopic`, `closeGeneralForumTopic`, `reopenGeneralForumTopic`, `hideGeneralForumTopic`, `unhideGeneralForumTopic`, `unpinAllGeneralForumTopicMessages`
- **Callbacks, Commands & Boosts (20):** `answerCallbackQuery`, `getUserChatBoosts`, `getBusinessConnection`, `getManagedBotToken`, `replaceManagedBotToken`, `setMyCommands`, `deleteMyCommands`, `getMyCommands`, `setMyName`, `getMyName`, `setMyDescription`, `getMyDescription`, `setMyShortDescription`, `getMyShortDescription`, `setMyProfilePhoto`, `removeMyProfilePhoto`, `setChatMenuButton`, `getChatMenuButton`, `setMyDefaultAdministratorRights`, `getMyDefaultAdministratorRights`
- **Gifts, Business & Stories (29):** `getAvailableGifts`, `getUniqueGift`, `sendGift`, `giftPremiumSubscription`, `verifyUser`, `verifyChat`, `removeUserVerification`, `removeChatVerification`, `readBusinessMessage`, `deleteBusinessMessages`, `setBusinessAccountName`, `setBusinessAccountUsername`, `setBusinessAccountBio`, `setBusinessAccountProfilePhoto`, `removeBusinessAccountProfilePhoto`, `setBusinessAccountGiftSettings`, `getBusinessAccountStarBalance`, `transferBusinessAccountStars`, `getBusinessAccountGifts`, `getUserGifts`, `getChatGifts`, `convertGiftToStars`, `upgradeGift`, `transferGift`, `deleteBusinessAccountGift`, `postStory`, `repostStory`, `editStory`, `deleteStory`
- **Updating Messages (21):** `editMessageText`, `editMessageCaption`, `editMessageMedia`, `editMessageLiveLocation`, `stopMessageLiveLocation`, `editMessageChecklist`, `editMessageReplyMarkup`, `stopPoll`, `editMessagePoll`, `addMessagePollOption`, `deleteMessagePollOption`, `editMessageWidgetData`, `editSharedWidgetData`, `approveSuggestedPost`, `declineSuggestedPost`, `deleteMessage`, `deleteMessages`, `sendChatMessageDraft`, `setChatMessageAutoDeleteTime`, `setChatTranslationLanguage`, `setChatDirectMessagesPrice`
- **Stickers (16):** `sendSticker`, `getStickerSet`, `getCustomEmojiStickers`, `uploadStickerFile`, `createNewStickerSet`, `addStickerToSet`, `setStickerPositionInSet`, `deleteStickerFromSet`, `replaceStickerInSet`, `setStickerEmojiList`, `setStickerKeywords`, `setStickerMaskPosition`, `setStickerSetTitle`, `setStickerSetThumbnail`, `setCustomEmojiStickerSetThumbnail`, `deleteStickerSet`
- **Rich Messages (2):** `sendRichMessage`, `sendRichMessageDraft`
- **Inline Mode (3):** `answerInlineQuery`, `answerWebAppQuery`, `savePreparedInlineMessage`
- **Payments & Stars (8):** `sendInvoice`, `createInvoiceLink`, `answerShippingQuery`, `answerPreCheckoutQuery`, `getMyStarBalance`, `getStarTransactions`, `refundStarPayment`, `editUserStarSubscription`
- **Telegram Passport (1):** `setPassportDataErrors`
- **Games (3):** `sendGame`, `setGameScore`, `getGameHighScores`

Parameter tables and return types for every method above: `SKILL-single-file.md` **Part 4** (or `references/bot-api/methods.md`).

## 12. Complete Type Catalog (402, by domain)

- **Updates (2):** `Update`, `WebhookInfo`
- **Core (30):** `User`, `Chat`, `ChatFullInfo`, `Message`, `MessageId`, `InaccessibleMessage`, `MaybeInaccessibleMessage`, `MessageEntity`, `TextQuote`, `ExternalReplyInfo`, `ReplyParameters`, `MessageOrigin*` (4), `LinkPreviewOptions`, `EphemeralMessageParameters`, `DirectMessagesTopic`, `PaidMessagesWaived`, `PaidMessagePriceChanged`, `DirectMessagePriceChanged`, `MessageAutoDeleteTimerChanged`, `ChatBoostAdded`, `UsersShared`, `ChatShared`, `WriteAccessAllowed`, `ManagedBotCreated`, `ManagedBotUpdated`, `ResponseParameters`
- **Media/Polls (38):** `PhotoSize`, `Animation`, `Audio`, `Document`, `Story`, `VideoQuality`, `Video`, `VideoNote`, `Voice`, `PaidMediaInfo`, `PaidMedia*`, `Contact`, `Dice`, `Poll`, `PollOption`, `PollAnswer`, `PollOptionAdded`, `PollOptionDeleted`, `InputPoll`, `InputPollOption`, `ChecklistTask`, `Checklist`, `InputChecklistTask`, `InputChecklist`, `ChecklistTasksDone`, `ChecklistTasksAdded`, `Location`, `Venue`, `WebAppData`, `ProximityAlertTriggered`, `UserProfilePhotos`, `UserProfileAudios`, `File`, `InputFile`, `InputProfilePhoto`
- **InputMedia (11):** `InputProfilePhotoStatic`, `InputProfilePhotoAnimated`, `InputMedia*` (5), `InputPaidMedia*` (3)
- **Widgets & TON (15):** `Widget`, `SharedWidget`, `WidgetQuery`, `SharedWidgetQuery`, `WidgetQueryType*` (4), `WidgetQueryWallet`, `TonWalletCard`, `TonWalletCardSticker`, `TonNft`, `TonNftAttribute`, `TonWalletTransfer`, `AreaPosition`
- **Keyboards (15):** `WebAppInfo`, `ReplyKeyboardMarkup`, `KeyboardButton*` (4), `KeyboardButtonPollType`, `ReplyKeyboardRemove`, `InlineKeyboardMarkup`, `InlineKeyboardButton`, `LoginUrl`, `SwitchInlineQueryChosenChat`, `CopyTextButton`, `CallbackQuery`, `ForceReply`
- **Members/Invites/Themes (28):** `ChatPhoto`, `ChatInviteLink`, `ChatAdministratorRights`, `ChatMemberUpdated`, `ChatMember*` (6), `ChatJoinRequest`, `ChatPermissions`, `Birthdate`, `ChatLocation`, `UserRating`, `ChatShareTheme*` (5), `EmojiType*` (3), `ChatThemeChanged`, `ChatOwnerLeft`, `ChatOwnerChanged`
- **Business/Gifts/Boosts (56):** `BusinessIntro`, `BusinessLocation`, `BusinessOpeningHours*` (2), `BusinessConnection`, `BusinessMessagesDeleted`, `BusinessBotRights`, `StoryArea*` (7), `LocationAddress`, `StoryAreaPosition`, `InputStoryContent*` (2), `Gift*` (Gift, Gifts, GiftBackground, GiftInfo), `UniqueGift*` (6), `OwnedGift*` (3), `OwnedGifts`, `AcceptedGiftTypes`, `StarAmount`, `SuggestedPost*` (7), `Giveaway*` (4), `ChatBoostSource*` (3), `ChatBoost`, `ChatBoostUpdated`, `ChatBoostRemoved`, `UserChatBoosts`
- **Forum/Reactions/Menu (45):** `ForumTopic*` (5), `GeneralForumTopic*` (2), `SharedUser`, `VideoChat*` (4), `ReactionType*` (3), `ReactionCount`, `MessageReactionUpdated`, `MessageReactionCountUpdated`, `BotCommand`, `BotCommandScope*` (7), `BotName`, `BotDescription`, `BotShortDescription`, `MenuButton*` (3), `BackgroundFill*` (3), `BackgroundType*` (4), `ChatBackground`
- **Stickers (4):** `Sticker`, `StickerSet`, `MaskPosition`, `InputSticker`
- **Rich Messages (82):** `RichMessage`, `InputRichMessage`, `InputRichMessageMedia`, `RichMessageButton`, `RichText*` (23 incl. `RichTextTonAddress`, `RichTextDateTime`, `RichTextIcon`), `RichBlock*` (26 content/output blocks), `InputRichBlock*` (30 input blocks)
- **Inline Mode (34):** `InlineQuery`, `InlineQueryResultsButton`, `InlineQueryResult*` (17 incl. Cached* and `InputWidgetMessageContent`, `InputSharedWidgetMessageContent`), `InputMessageContent`, `InputTextMessageContent`, `InputLocationMessageContent`, `InputVenueMessageContent`, `InputContactMessageContent`, `InputInvoiceMessageContent`, `ChosenInlineResult`, `SentWebAppMessage`, `PreparedInlineMessage`
- **Payments (25):** `LabeledPrice`, `Invoice`, `ShippingAddress`, `OrderInfo`, `ShippingOption`, `SuccessfulPayment`, `RefundedPayment`, `ShippingQuery`, `PreCheckoutQuery`, `PaidMediaPurchased`, `RevenueWithdrawalState*` (3), `AffiliateInfo`, `TransactionPartner*` (7), `StarTransaction`, `StarTransactions`
- **Passport (14):** `PassportData`, `PassportFile`, `EncryptedPassportElement`, `EncryptedCredentials`, `PassportElementError*` (10)
- **Games (3):** `Game`, `CallbackGame`, `GameHighScore`

Field-level detail: `SKILL-single-file.md` **Part 5** (or `references/bot-api/types.md`).

## 13. Breaking Changes to Remember

- **9.6 (Apr 3, 2026):** `correct_option_id` → `correct_option_ids` (Array of Integer) on `sendPoll`/`Poll`; Managed Bots introduced (`getManagedBotToken`, `managed_bot` update).
- **10.0:** Guest Mode (`guest_message`, `answerGuestQuery`); Business bots no longer require Telegram Premium.
- **10.2 (Jul 20, 2026 origin hardening):** Mini App calls blocked from non-registered origins; ephemeral fields `ephemeral_text`/`ephemeral_receiver_user_id` etc. exist on `send*`; Rich Messages introduced (32,768-char limit).
- **10.3 (Oct 16, 2026):** **breaking:** `ephemeral_*` fields removed from `send*`/`answerCallbackQuery` → use `EphemeralMessageParameters` (via `ephemeral_message`); `receiver_user_id`/`chat_id` optional when replying to a callback (10.4).
- **8.2 (Jan 1, 2025):** channel videos > 100 MB return placeholder `message_id: 0` until transcoding finishes — wait for the follow-up `channel_post`.
- **Layer 214/225:** Monoforum dialog-ID range (see Section 10) — never reject IDs below −2,002,147,483,648.

## 14. Top Production Pitfalls

1. UTF-8/code-point offsets → broken entities; use UTF-16 (Section 2.3) or `scripts/utf16_entity_offsets.py`.
2. Unescaped MarkdownV2 → `400 can't parse entities`; use HTML or the escaper script.
3. Missing `answerCallbackQuery`/`answerWidgetQuery` → infinite spinner.
4. Missing `widget_query`/`shared_widget_query`/`pre_checkout_query` in `allowed_updates` → events silently never delivered.
5. Using `initDataUnsafe` on the backend → forgeable; verify HMAC/Ed25519 (Section 7).
6. Mixing up initData (HMAC with "WebAppData") vs Login Widget (SHA256) secrets.
7. Slow `pre_checkout_query` handling > 10 s → checkout fails.
8. Unthrottled `Promise.all` broadcasts → 429 storms; two-tier pacing (Section 5) + `retry_after` backoff.
9. `callback_data` > 64 bytes → `BUTTON_DATA_INVALID`.
10. Trusting `message_id` of > 100 MB channel videos (placeholder 0).
11. Two pollers / webhook + polling → `409 Conflict`.
12. Widgets without origin meta / same-origin rules → sandboxed out; `sendWidget` is private-chat only in production.

## 15. Where the Full Detail Lives

| Topic | Single-file location | Repo path |
|---|---|---|
| Methods (params, return types) | Part 4 | `references/bot-api/methods.md` |
| Types (fields) | Part 5 | `references/bot-api/types.md` |
| Core, updates, limits, errors | Part 3 | `references/bot-api/core-and-updates.md` |
| Formatting & entities | Part 6 | `references/formatting.md` |
| Keyboards & buttons | Part 7 | `references/keyboards-and-buttons.md` |
| Mini Apps | Part 8 | `references/mini-apps.md` |
| Widgets & Login | Part 9 | `references/widgets-and-login.md` |
| Payments, Stars, Business | Part 10 | `references/payments-stars-business.md` |
| Webhooks & hosting | Part 11 | `references/webhooks-and-hosting.md` |
| Version history 6.0→10.4 | Part 12 | `references/whats-new.md` |
| MTProto protocol/auth/files | Parts 13–15 | `references/mtproto/*.md` |
| Libraries comparison | Part 16 | `references/libraries.md` |
| Pitfalls (full 15 with fixes) | Part 17 | `references/pitfalls.md` |
| Decision guide | Part 2 | `references/decision-guide.md` |
| Helper scripts (full source) | Appendix D | `scripts/*.py` |
| Runnable examples | Appendix E | `examples/` |

Script usage one-liners: `python3 scripts/utf16_entity_offsets.py "<text>" "<substring>"`; `python3 scripts/escape_markdown_v2.py "<text>"`; `python3 scripts/validate_initdata.py --bot-token <token> --init-data "<raw>"`; `python3 scripts/dialog_id_converter.py <id>`; `python3 scripts/coverage_audit.py`.
