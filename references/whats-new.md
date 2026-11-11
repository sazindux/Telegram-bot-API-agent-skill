# What's New: Complete Changelog Diff (Bot API 6.0 -> 10.4 & MTProto Layers 196 -> 225) (`references/whats-new.md`)

- **Source:** [Bot API Changelog](https://core.telegram.org/bots/api-changelog), [MTProto Layer Changelog](https://core.telegram.org/api/layers)
- **Verified Against:** **Bot API 10.4** (November 9, 2026) and **MTProto Layer 225** (checked November 11, 2026)

---

## 1. Newest Bot API Versions in Detail (Bot API 9.0 -> 10.4)

### Bot API 10.4 — November 9, 2026 ([Source](https://core.telegram.org/bots/api-changelog#november-9-2026))
- **In-Chat HTML Widgets:**
  - Added `sendWidget`, `sendSharedWidget`, `answerWidgetQuery`, `editMessageWidgetData`, `editSharedWidgetData`.
  - Added classes `Widget`, `WidgetQuery`, `SharedWidgetQuery`, `WidgetQueryType` (`WidgetQueryTypeData`, `WidgetQueryTypeSignData`, `WidgetQueryTypeSentTransaction`), `WidgetQueryWallet`, `InputWidgetMessageContent`, `InputSharedWidgetMessageContent`.
  - Added `widget` field on `Message` and `ExternalReplyInfo`; `widget_query` and `shared_widget_query` on `Update`.
  - Production restriction: `sendWidget` currently works only in private chats and automatically enables `has_protected_content` (cannot be forwarded or copied via `copyMessage`/`copyMessages`); inline widget results are test-server only.
- **Ephemeral Callback Replies in Any Chat:**
  - Bots can send ephemeral replies to callback queries in any chat (except channel direct messages) by specifying `callback_query_id` without `receiver_user_id` inside `ephemeral_message_parameters` on `sendMessage`, `sendRichMessage`, `sendAnimation`, `sendAudio`, `sendContact`, `sendDocument`, `sendLivePhoto`, `sendLocation`, `sendPhoto`, `sendSticker`, `sendVenue`, `sendVideo`, `sendVideoNote`, and `sendVoice`. Both `EphemeralMessageParameters.receiver_user_id` and `chat_id` on those methods are now optional when `callback_query_id` is set.
- **Quotes from Rich Messages:** Added `TextQuote.rich_texts` and `ReplyParameters.quote_rich_texts`.
- **TON Wallet Cards & Transfers:** Added `TonWalletCard`, `TonWalletCardSticker`, `TonNft`, `TonNftAttribute` (`ChatFullInfo.ton_wallet_card`), `TonWalletTransfer` (`Message.ton_wallet_transfer`), and renamed `StoryAreaPosition` -> `AreaPosition`.
- **Chat Share Themes:** Added `ChatShareTheme` (`ChatShareThemeEmoji`, `ChatShareThemeUniqueGift` on `ChatFullInfo.share_theme`), `EmojiType` (`EmojiTypeEmoji`, `EmojiTypeCustomEmoji`), `ChatShareThemeBackdrop`, `ChatShareThemeBackdrops`, and `getChatShareThemeBackdrops`.
- **Gifts:** Added `getUniqueGift(name)` and `deleteBusinessAccountGift(business_connection_id, owned_gift_id)`.
- **General & Entities:**
  - Secondary bot usernames ending in `agent`, `ai`, `app`, `game`, or `gay` for up to 2 bots owned by Premium users (`KeyboardButtonRequestManagedBot.suggested_username`).
  - Added `RichTextTonAddress` and `MessageEntity` types `"ton_address"` and `"bank_card_number"`.
  - Added `custom_description_parse_mode` and `custom_description_entities` to `verifyUser` and `verifyChat`.
  - Added `PaidMessagesWaived` (`Message.paid_messages_waived`).
  - Added private-chat topic deep links: `https://t.me/<bot_username>/<message_thread_id>`.

### Bot API 10.3 — August 24, 2026 ([Source](https://core.telegram.org/bots/api-changelog#august-24-2026))
- **Rich Messages Expansion:** Added `RichMessageButton`, `RichTextButton`, `RichBlockButtons` / `InputRichBlockButtons`, `is_compact` on `RichBlockTable` / `InputRichBlockTable`, `RichBlockExpandableBlockQuotation` / `InputRichBlockExpandableBlockQuotation`, `RichBlockDocument` / `InputRichBlockDocument`, and `tg://document?id=` links.
- **Ephemeral Messages Refactor (Breaking vs 10.2):** Added `EphemeralMessageParameters` (`receiver_user_id`, `callback_query_id`, `replace_callback_query_message`) and **replaced** top-level `receiver_user_id` and `callback_query_id` on `send*` methods with `ephemeral_message_parameters`. Added `rich_message` to `editEphemeralMessageText`, `show_caption_above_media` to `editEphemeralMessageCaption`, and new file upload support in `editEphemeralMessageMedia`.
- **Reply Markup:** Added `DisabledButton` (`InlineKeyboardButton.disabled`) and `force_reply` on `InlineKeyboardMarkup` and `ReplyKeyboardMarkup`.
- **Streaming Stop Control:** Added `can_stop` and `keep_on_stop` to `sendMessageDraft` and `sendRichMessageDraft`, plus `Update.stopped_message_generation` (`MessageGenerationStopped`).
- **General:** Added `can_send_welcome_messages` admin right, `CommunityChatJoined` (`Message.community_chat_joined`), and `text`/`entities`/`is_private` on `UniqueGiftInfo`.

### Bot API 10.2 — July 14, 2026 ([Source](https://core.telegram.org/bots/api-changelog#july-14-2026))
- **Rich Message Input Blocks & Media:** Added `InputRichMessageMedia`, `InputMediaVoiceNote`, and 22 `InputRichBlock*` classes (`InputRichMessage.blocks` and `InputRichMessage.media`).
- **Ephemeral Messages & Commands:** Added `BotCommand.is_ephemeral`, `Message.receiver_user`, `Message.ephemeral_message_id`, `ReplyParameters.ephemeral_message_id`, `editEphemeralMessageText/Media/Caption/ReplyMarkup`, and `deleteEphemeralMessage`.
- **Communities:** Added `Community`, `CommunityChatAdded`, `CommunityChatRemoved`, and `ChatFullInfo.community`.
- **Subscriptions & Security:** Added `Update.subscription` (`BotSubscriptionUpdated`) and enforced **Mini App Origin Hardening** (effective July 20, 2026).

### Bot API 10.1 — June 11, 2026 ([Source](https://core.telegram.org/bots/api-changelog#june-11-2026))
- **Rich Messages Debut:** Added `sendRichMessage`, `sendRichMessageDraft`, `RichMessage`, `InputRichMessage`, `InputRichMessageContent`, `editMessageText(rich_message=...)`, 28 `RichText*` classes, and 22 `RichBlock*` classes (up to 32,768 chars).
- **Join Request Queries & Guard Bots:** Added `User.supports_join_request_queries`, `ChatFullInfo.guard_bot`, `ChatJoinRequest.query_id`, `WebAppInitData.chat_join_request_query_id`, `sendChatJoinRequestWebApp`, and `answerChatJoinRequestQuery`.
- **Polls:** Added `Link` (`PollMedia.link`) and `InputMediaLink` (`InputPollOptionMedia`).

### Bot API 10.0 — May 8, 2026 ([Source](https://core.telegram.org/bots/api-changelog#may-8-2026))
- **Guest Mode:** Added `User.supports_guest_queries`, `Message.guest_bot_caller_user`, `Message.guest_bot_caller_chat`, `Message.guest_query_id`, `Update.guest_message`, `SentGuestMessage`, and `answerGuestQuery`.
- **Live Photos:** Added `LivePhoto`, `InputMediaLivePhoto`, `PaidMediaLivePhoto`, `InputPaidMediaLivePhoto`, `sendLivePhoto`, and support in `sendMediaGroup` / `editMessageMedia`.
- **Polls Overhaul:** Added `PollMedia`, `InputPollMedia`, `InputPollOptionMedia`, `InputMediaSticker/Location/Venue`, `members_only`, `country_codes`, and lowered minimum poll options from 2 to **1**.
- **Chat & Reactions Moderation:** Added `deleteMessageReaction`, `deleteAllMessageReactions`, `can_react_to_messages` permission, and `getChatAdministrators(return_bots=...)`.
- **Business, Bot-to-Bot & Personal Channels:** Business Bots no longer require Premium; added bot-to-bot messaging via `@username`; allowed empty text in `sendMessageDraft`; added `BotAccessSettings`, `getManagedBotAccessSettings`, `setManagedBotAccessSettings`, and `getUserPersonalChatMessages`.

### Bot API 9.6 — April 3, 2026 ([Source](https://core.telegram.org/bots/api-changelog#april-3-2026))
- **Managed Bots:** Added `User.can_manage_bots`, `KeyboardButtonRequestManagedBot` (`KeyboardButton.request_managed_bot`), `ManagedBotCreated`, `ManagedBotUpdated` (`Update.managed_bot`), `getManagedBotToken`, `replaceManagedBotToken`, `PreparedKeyboardButton`, `savePreparedKeyboardButton`, `WebApp.requestChat`, and `t.me/newbot/...` links.
- **Multi-Answer Quizzes & Open Polls:** Replaced `correct_option_id` with `correct_option_ids` on `Poll` and `sendPoll`; raised max poll `open_period` to `2,628,000` seconds; added `allows_revoting`, `shuffle_options`, `allow_adding_options`, `hide_results_until_closes`, poll `description`, `PollOption.persistent_id`, `PollOptionAdded`, `PollOptionDeleted`, and `ReplyParameters.poll_option_id`.

### Bot API 9.5 — March 1, 2026 ([Source](https://core.telegram.org/bots/api-changelog#march-1-2026))
- Added `MessageEntity` type `"date_time"` (`<tg-time>`).
- Allowed **all bots** to use `sendMessageDraft`.
- Added member tags (`ChatMemberMember.tag`, `ChatMemberRestricted.tag`, `Message.sender_tag`, `setChatMemberTag`, `can_edit_tag`, `can_manage_tags`).
- Added `BottomButton.iconCustomEmojiId` for Mini Apps.

### Bot API 9.4 — February 9, 2026 ([Source](https://core.telegram.org/bots/api-changelog#february-9-2026))
- Allowed bots to use custom emoji in outgoing messages if the bot owner has Telegram Premium.
- Allowed bots to call `createForumTopic` in private chats (`User.allows_users_to_create_topics`).
- Added `icon_custom_emoji_id` and `style` (button colors) to `KeyboardButton` and `InlineKeyboardButton`.
- Added `setMyProfilePhoto`, `removeMyProfilePhoto`, `getUserProfileAudios` (`UserProfileAudios`, `ChatFullInfo.first_profile_audio`), `VideoQuality` (`Video.qualities`), `ChatOwnerLeft`, `ChatOwnerChanged`, `UniqueGiftModel.rarity`, and `UniqueGift.is_burned`.

### Bot API 9.3 — December 31, 2025 ([Source](https://core.telegram.org/bots/api-changelog#december-31-2025))
- **Private-Chat Topics & Streaming:** Added `User.has_topics_enabled`, `sendMessageDraft`, and `message_thread_id` support in private chats across all `send*`, `copy*`, `forward*`, and forum management methods.
- **Gifts & Monetization:** Added `getUserGifts`, `getChatGifts`, `UniqueGiftColors`, `GiftBackground`, `repostStory`, `UserRating`, `ChatFullInfo.paid_message_star_count`, `message_effect_id` on `forwardMessage`/`copyMessage`, and raised max paid media price to **25,000 Stars**.

### Bot API 9.2 — August 15, 2025 ([Source](https://core.telegram.org/bots/api-changelog#august-15-2025))
- **Channel Direct Messages & Suggested Posts:** Added `Chat.is_direct_messages`, `DirectMessagesTopic`, `direct_messages_topic_id` parameter, `SuggestedPostParameters`, `SuggestedPostInfo`, `approveSuggestedPost`, `declineSuggestedPost`, and `ReplyParameters.checklist_task_id`.

### Bot API 9.1 — July 3, 2025 ([Source](https://core.telegram.org/bots/api-changelog#july-3-2025))
- **Checklists & Star Balance:** Added `Checklist`, `ChecklistTask`, `InputChecklist`, `InputChecklistTask`, `sendChecklist`, `editMessageChecklist`, `getMyStarBalance`, `DirectMessagePriceChanged`, `WebApp.hideKeyboard`, and increased max poll options to **12**.

### Bot API 9.0 — April 11, 2025 ([Source](https://core.telegram.org/bots/api-changelog#april-11-2025))
- **Business Account Automation, Stories & Unique Gifts:** Added `BusinessBotRights`, `readBusinessMessage`, `deleteBusinessMessages`, `setBusinessAccount*`, `getBusinessAccountStarBalance`, `transferBusinessAccountStars`, `getBusinessAccountGifts`, `convertGiftToStars`, `upgradeGift`, `transferGift`, `postStory`, `editStory`, `deleteStory`, `giftPremiumSubscription`, `UniqueGift`, `AcceptedGiftTypes`, and Mini App `DeviceStorage` & `SecureStorage`.

---

## 2. Historical Summary Table (Bot API 6.0 -> 8.3)

| Version | Release Date | Key Additions & Changes |
|---|---|---|
| **8.3** | Feb 12, 2025 | `sendGift` to channels (`chat_id`), `TransactionPartnerChat`, `Video.cover` & `start_timestamp`, reactions on service messages. |
| **8.2** | Jan 1, 2025 | Third-party verification (`verifyUser`, `verifyChat`, `removeUserVerification`, `removeChatVerification`), `sendGift(pay_for_upgrade=...)`, removed `InlineQueryResultArticle.hide_url`. |
| **8.1** | Dec 4, 2024 | Affiliate programs (`TransactionPartnerAffiliateProgram`, `AffiliateInfo`), `StarTransaction.nanostar_amount`. |
| **8.0** | Nov 17, 2024 | Mini Apps 2.0 (Fullscreen, `safeAreaInset`, `addToHomeScreen`, `setEmojiStatus`, `shareMessage`/`savePreparedInlineMessage`, `downloadFile`, `LocationManager`, Motion sensors, Ed25519 3P validation), Star Subscriptions (`subscription_period`, `editUserStarSubscription`), Paid Gifts (`getAvailableGifts`, `sendGift`). |
| **7.11** | Oct 31, 2024 | `CopyTextButton` (`InlineKeyboardButton.copy_text`), Paid Broadcasts (`allow_paid_broadcast`, `TransactionPartnerTelegramApi`), `editMessageMedia` on text-only messages. |
| **7.10** | Sep 6, 2024 | `PaidMediaPurchased` (`Update.purchased_paid_media`), Star Giveaways (`prize_star_count`), Mini App `SecondaryButton` & `bottomBarColor`. |
| **7.9** | Aug 14, 2024 | Super Channels, `ChatMemberSubscription`, Star reaction type (`ReactionTypePaid`), `createChatSubscriptionInviteLink` / `editChatSubscriptionInviteLink`. |
| **7.8** | Jul 31, 2024 | Main Mini App (`User.has_main_web_app`), `WebApp.shareToStory`, `business_connection_id` on `pinChatMessage`/`unpinChatMessage`. |
| **7.7** | Jul 7, 2024 | `refundStarPayment`, Mini App `enableVerticalSwipes` / `disableVerticalSwipes`. |
| **7.6** | Jul 1, 2024 | `sendPaidMedia`, `PaidMedia*` classes, `TransactionPartnerTelegramAds`, Direct Link Mini Apps default to fullscreen height. |
| **7.5** | Jun 18, 2024 | `getStarTransactions`, `StarTransaction*`, `TransactionPartner*`, `business_connection_id` on `editMessage*`/`stopPoll`. |
| **7.4** | May 28, 2024 | Telegram Stars (`XTR`) digital payments, `refunded_payment`, `expandable_blockquote`, `message_effect_id`. |
| **7.3** | May 6, 2024 | `ChatFullInfo` split from `Chat`, `BackgroundType*` / `BackgroundFill*`, live location `proximity_alert_radius` updates. |
| **7.2** | Mar 31, 2024 | `BusinessConnection`, `business_message` updates, `Birthdate`, `BusinessIntro/Location/OpeningHours`, Mini App `BiometricManager`. |
| **7.1** | Feb 16, 2024 | `getUserChatBoosts`, administrator rights for stories (`can_post_stories`, `can_edit_stories`, `can_delete_stories`), `ChatBoostAdded`. |
| **7.0** | Dec 29, 2023 | Reactions (`setMessageReaction`, `MessageReactionUpdated`), Replies 2.0 (`ReplyParameters`, `ExternalReplyInfo`, `TextQuote`), `LinkPreviewOptions`, `blockquote`, `deleteMessages`/`forwardMessages`/`copyMessages` (batch up to 100), Giveaways & Chat Boosts, Mini App `SettingsButton`. |
| **6.9** | Sep 22, 2023 | Story admin rights, Mini App `CloudStorage`, `requestWriteAccess`, `requestContact`. |
| **6.8** | Aug 18, 2023 | `Story` object, `PollAnswer.voter_chat`, `unpinAllGeneralForumTopicMessages`. |
| **6.7** | Apr 21, 2023 | `SwitchInlineQueryChosenChat`, `InlineQueryResultsButton`, `setMyName`/`getMyName`, Direct Link Mini Apps, `WebApp.switchInlineQuery`. |
| **6.6** | Mar 9, 2023 | `setMyDescription`, `setMyShortDescription`, full Sticker Set management (`InputSticker`, `setStickerEmojiList`, `setStickerKeywords`, etc.). |
| **6.5** | Feb 3, 2023 | `KeyboardButtonRequestUsers` (replaced `KeyboardButtonRequestUser` in 7.0), `KeyboardButtonRequestChat`, media permissions split (`can_send_photos`, `can_send_videos`, etc.). |
| **6.4** | Dec 30, 2022 | General Forum Topic methods (`editGeneralForumTopic`, `hideGeneralForumTopic`, etc.), `has_media_spoiler`, Mini App QR scanner & clipboard. |
| **6.3** | Nov 5, 2022 | Forum Topics (`createForumTopic`, `editForumTopic`, `closeForumTopic`, `deleteForumTopic`, `message_thread_id`). |
| **6.2** | Aug 12, 2022 | Custom Emoji (`custom_emoji` entity, `getCustomEmojiStickers`), Mini App `showPopup`/`showAlert`/`showConfirm`. |
| **6.1** | Jun 20, 2022 | `createInvoiceLink`, Attachment Menu in groups/channels, `join_to_send_messages`, `join_by_request`, Mini App `BackButton`, `HapticFeedback`, `openInvoice`. |
| **6.0** | Apr 16, 2022 | Web Apps (Mini Apps) debut (`WebAppInfo`, `MenuButtonWebApp`, `answerWebAppQuery`, `setChatMenuButton`, `setMyDefaultAdministratorRights`). |
