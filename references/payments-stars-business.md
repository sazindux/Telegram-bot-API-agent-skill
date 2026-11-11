# Payments, Telegram Stars (`XTR`), Gifts, Business & Agentic Features (`references/payments-stars-business.md`)

- **Source:** [Bot Payments API for Digital Goods (Stars)](https://core.telegram.org/bots/payments-stars), [Bot Payments API (Physical Goods)](https://core.telegram.org/bots/payments), [Bot Features](https://core.telegram.org/bots/features), [Bot API Reference](https://core.telegram.org/bots/api)
- **Verified Against:** **Bot API 10.4** (November 9, 2026; checked November 11, 2026)

---

## 1. Telegram Stars (`XTR`) vs Physical Goods Payments

| Attribute | Digital Goods & Services (Telegram Stars) | Physical Goods & Services |
|---|---|---|
| **Mandatory Rule** | **Must** use Telegram Stars (`currency: "XTR"`) per Apple/Google store rules. | Uses third-party payment provider (`Stripe`, etc.) in fiat currency (`USD`, `EUR`, `LKR`, etc.). |
| `currency` parameter | `"XTR"` | 3-letter ISO 4217 code (see [currencies.json](https://core.telegram.org/bots/payments/currencies.json)). |
| `provider_token` parameter | Pass empty string `""` or omit | Provider token from `@BotFather` (`123:TEST:...` or `123:LIVE:...`). |
| `prices` (`Array of LabeledPrice`) | **Exactly 1 item** required for `XTR`; `amount` is the integer count of Stars. | 1 or more line items; `amount` is in the smallest currency unit (e.g. cents for `USD`). |
| Shipping & Buyer Info | Not used (`need_shipping_address`, `is_flexible`, `need_email`, etc. must not be set). | Optional `need_name`, `need_phone_number`, `need_email`, `need_shipping_address`, `is_flexible` (`shipping_query`). |
| Refunds | `refundStarPayment(user_id, telegram_payment_charge_id)` via Bot API. | Handled via the third-party payment provider dashboard/API. |
| Mandatory Bot Commands | Must handle `/terms` and `/paysupport` (plus `/support`). | Must handle `/terms` and `/support`. |

### Complete Payment Lifecycle (4 Steps)
1. **Create Invoice:** Call `sendInvoice` (sends invoice message to chat) or `createInvoiceLink` (returns an HTTPS invoice URL to open in a Mini App via `Telegram.WebApp.openInvoice(url)`).
2. **Shipping Query (Physical Flexible Invoices Only):** If `is_flexible: true`, handle `Update.shipping_query` by calling `answerShippingQuery(shipping_query_id, ok=True, shipping_options=[...])`.
3. **Pre-Checkout Query (10-Second Deadline!):** When the user clicks Pay, Telegram sends `Update.pre_checkout_query`. You **must** call `answerPreCheckoutQuery(pre_checkout_query_id, ok=True)` (or `ok=False, error_message="..."`) within **10 seconds**, or the transaction is automatically canceled.
4. **Confirm & Deliver (`successful_payment`):** **Never deliver goods inside `pre_checkout_query`!** Wait for the `Message` with `message.successful_payment` (`SuccessfulPayment`). Persist `successful_payment.telegram_payment_charge_id` (required for `refundStarPayment`) and `invoice_payload`, then deliver the item.

---

## 2. Star Subscriptions, Paid Media, Balance & Affiliates

- **Star Subscriptions (Bot API 8.0 / 9.0 / 10.2):**
  - Call `createInvoiceLink` with `currency: "XTR"`, `subscription_period: 2592000` (30 days in seconds), and a price up to **10,000 Telegram Stars** per period (raised in Bot API 9.0).
  - Manage/cancel recurring billing via `editUserStarSubscription(user_id, telegram_payment_charge_id, is_canceled)`.
  - Receive lifecycle updates via `Update.subscription` (`BotSubscriptionUpdated`, **Bot API 10.2+**) and `SuccessfulPayment.is_recurring` / `is_first_recurring` / `subscription_expiration_date`.
- **Paid Media (Bot API 7.4 / 7.10 / 9.0 / 9.3 / 10.0):**
  - Send locked photos, videos, or **live photos** (`InputPaidMediaLivePhoto`, **Bot API 10.0+**) via `sendPaidMedia(chat_id, star_count, media, payload=..., caption=...)`.
  - Maximum `star_count`: **25,000 Telegram Stars** (raised from 2,500 -> 10,000 in 9.0 -> **25,000 in Bot API 9.3**).
  - When unlocked in non-channel chats with a non-empty `payload`, the bot receives `Update.purchased_paid_media` (`PaidMediaPurchased`).
- **Bot & Business Star Balances & Transactions:**
  - `getMyStarBalance()` (**Bot API 9.1+**): Returns the bot's own `StarAmount` (`amount` + `nanostar_amount`).
  - `getStarTransactions(offset, limit)` (Bot API 7.5+): Returns `StarTransactions` with `StarTransaction` items (`id`, `amount`, `nanostar_amount` [8.1+], `date`, `source`, `receiver` of type `TransactionPartner*`).
  - `getBusinessAccountStarBalance(business_connection_id)` & `transferBusinessAccountStars(business_connection_id, star_count)` (**Bot API 9.0+**).
- **Paid Messages in Chats & Waivers (Bot API 9.0 / 9.3 / 10.4):**
  - `ChatFullInfo.paid_message_star_count` (9.3) and `Message.paid_star_count` (9.0) track Stars paid per message.
  - `Message.paid_messages_waived` (`PaidMessagesWaived`, **Bot API 10.4**) indicates a service message where the sender used a link waiving the Star fee.
- **Affiliate Programs (Bot API 8.1+):**
  - `TransactionPartnerAffiliateProgram` and `TransactionPartnerUser.affiliate` (`AffiliateInfo`) report commission details (`commission_per_mille`, `amount`, `nanostar_amount`, `affiliate_user`, `affiliate_chat`).

---

## 3. Gifts, Unique Collectible Gifts & TON Wallet (Bot API 8.0–10.4)

- **Sending Regular Gifts & Premium:**
  - `getAvailableGifts()` -> returns `Gifts` catalog.
  - `sendGift(gift_id, user_id=..., chat_id=..., text=..., pay_for_upgrade=...)` (channel `chat_id` added in 8.3; `"date_time"` entities allowed in `text` since 9.6).
  - `giftPremiumSubscription(user_id, month_count, star_count, text=...)` (**Bot API 9.0+**): Gifts 3, 6, or 12 months of Telegram Premium using the bot's Stars.
- **Inspecting & Managing Gifts (Bot API 9.0 / 9.3 / 10.3 / 10.4):**
  - `getUserGifts(user_id, ...)` & `getChatGifts(chat_id, ...)` (**Bot API 9.3+**): Fetch gifts owned by any user or chat.
  - `getUniqueGift(name)` (**Bot API 10.4+**): Fetch a `UniqueGift` collectible by its slug/name!
  - `getBusinessAccountGifts(business_connection_id, ...)` (**Bot API 9.0 / 9.3**): Filter by `exclude_unsaved`, `exclude_saved`, `exclude_unlimited`, `exclude_limited_upgradable` [9.3], `exclude_limited_non_upgradable` [9.3], `exclude_unique`, `exclude_from_blockchain` [9.3].
  - `convertGiftToStars(business_connection_id, owned_gift_id)` (**9.0**): Converts a regular gift into Stars.
  - `deleteBusinessAccountGift(business_connection_id, owned_gift_id)` (**Bot API 10.4+**): Deletes a regular gift owned by a managed business account without receiving Stars.
  - `upgradeGift(business_connection_id, owned_gift_id, keep_original_details=..., star_count=...)` (**9.0**) & `transferGift(business_connection_id, owned_gift_id, new_owner_chat_id, star_count=...)` (**9.0**).
- **TON Wallet Cards & Transfers (Bot API 10.4):**
  - `ChatFullInfo.ton_wallet_card` (`TonWalletCard`, containing `TonWalletCardSticker`, `TonNft`, `TonNftAttribute`, and `AreaPosition`).
  - `Message.ton_wallet_transfer` (`TonWalletTransfer`) for service messages about TON transfers.

---

## 4. Business Bots, Managed Bots, Guest Mode & Bot-to-Bot (Bot API 9.0–10.4)

### A. Business Bots (Secretary Mode — No Premium Required Since Bot API 10.0!)
- Users connect a bot in Telegram Settings -> Telegram Business -> Chatbots (since **Bot API 10.0**, users do **not** need Telegram Premium to connect a Business Bot).
- Bot receives `Update.business_connection` (`BusinessConnection` with `id`, `user`, `user_chat_id`, `rights` of type `BusinessBotRights` [9.0+]), `business_message`, `edited_business_message`, and `deleted_business_messages`.
- Pass `business_connection_id` to `sendMessage`, `sendPhoto`, `sendChecklist`, `postStory`, `readBusinessMessage`, `deleteBusinessMessages`, `setBusinessAccountName/Username/Bio/ProfilePhoto/GiftSettings`, etc.

### B. Managed Bots (Bot Manager Mode — Bot API 9.6 / 10.0 / 10.4)
- Enable **Bot Management Mode** in `@BotFather`'s Mini App (`User.can_manage_bots == True`).
- Share a creation link `https://t.me/newbot/<manager_bot>/<suggested_username>?name=<Name>` or send a `KeyboardButtonRequestManagedBot` button.
- Receive `Update.managed_bot` (`ManagedBotUpdated`), fetch the child bot's token via `getManagedBotToken(user_id)` (or rotate via `replaceManagedBotToken(user_id)`), and manage access settings via `getManagedBotAccessSettings(user_id)` / `setManagedBotAccessSettings(user_id, ...)` (**Bot API 10.0+**).

### C. Guest Mode (`answerGuestQuery` — Bot API 10.0+)
- Enable **Guest Mode** in `@BotFather`'s Mini App (`User.supports_guest_queries == True`).
- When a user `@mentions` the bot (up to 3 guest bots per message) or replies to its message in **any** group or private chat (even where the bot is **not** a member!), the bot receives `Update.guest_message` (`Message` with `guest_query_id`, `guest_bot_caller_user`, `guest_bot_caller_chat`).
- Reply once into that chat using `answerGuestQuery(guest_query_id, result)` (where `result` is an `InlineQueryResult` / `InputRichMessageContent`), returning `SentGuestMessage`.

### D. Bot-to-Bot Communication (Bot API 10.0+)
- Enable **Bot-to-Bot Communication Mode** in `@BotFather`.
- **In Groups:** Mention `/command@OtherBot` or reply to another bot's message (if at least one bot has Bot-to-Bot enabled, or if the receiving bot is admin / has Privacy Mode disabled).
- **In Private Chats:** Pass `@other_bot_username` as `chat_id` to `sendMessage` (requires Bot-to-Bot enabled on **both** bots).
- **Mandatory Safeguard:** Always implement loop-prevention (max interaction depth, deduplication, and per-bot cooldowns).

---

## 5. Channel Direct Messages (Monoforums), Suggested Posts & Checklists

- **Channel Direct Messages (`direct_messages_topic_id` — Bot API 9.2+):**
  - Identified by `Chat.is_direct_messages == True` and `ChatFullInfo.parent_chat`.
  - Incoming messages have `Message.direct_messages_topic` (`DirectMessagesTopic` with `topic_id` and `user`).
  - Pass `direct_messages_topic_id` to `sendMessage`, `sendPhoto`, `copyMessage`, `forwardMessage`, etc.
- **Suggested Posts (`SuggestedPostParameters` — Bot API 9.2+):**
  - Submit a suggested post to a channel direct messages topic by passing `suggested_post_parameters` (`SuggestedPostParameters`: optional `price` in `XTR` Stars or `TON` nanograms, optional `send_date`) on `sendMessage` / `sendPhoto` / etc.
  - Channel admin bots with `can_manage_direct_messages` (and `can_post_messages` for approval) call `approveSuggestedPost(chat_id, message_id, send_date=...)` or `declineSuggestedPost(chat_id, message_id, comment=...)`.
  - Paid suggested posts (`Message.is_paid_post == True`) **must not be deleted for 24 hours** to receive payment.
- **Checklists (`sendChecklist` & `editMessageChecklist` — Bot API 9.1 / 9.2 / 9.3):**
  - Send interactive task lists on behalf of a business account using `sendChecklist(business_connection_id, chat_id, checklist)` (`InputChecklist` with `title` and `tasks` array of `InputChecklistTask`).
  - Track completion updates via `Message.checklist_tasks_done` and `Message.checklist_tasks_added`, and reply to a specific task via `ReplyParameters.checklist_task_id` (9.2+).
