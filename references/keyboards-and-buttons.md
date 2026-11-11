# Keyboards, Buttons & Interactive UI (`references/keyboards-and-buttons.md`)

- **Source:** [InlineKeyboardMarkup](https://core.telegram.org/bots/api#inlinekeyboardmarkup), [ReplyKeyboardMarkup](https://core.telegram.org/bots/api#replykeyboardmarkup), [Telegram Bot Features — Keyboards](https://core.telegram.org/bots/features#keyboards)
- **Verified Against:** **Bot API 10.4** (November 9, 2026; checked November 11, 2026)

---

## 1. `InlineKeyboardMarkup` & `InlineKeyboardButton` (All 11 Action Types + Styling)

An `InlineKeyboardMarkup` attaches buttons directly beneath a message:
- `inline_keyboard`: `Array of Array of InlineKeyboardButton` (rows of buttons; max ~100 buttons total, up to 8 per row).
- `force_reply` (`True`, optional, **added in Bot API 10.3**): Shows the reply interface to the user alongside the inline keyboard!

### `InlineKeyboardButton` Fields (Bot API 10.4)

Every `InlineKeyboardButton` **must** have `text` (`String`) and **exactly one** of the 11 action fields below, plus optional visual styling fields (`icon_custom_emoji_id`, `style`):

| Field | Type | Introduced | Description & Constraints |
|---|---|---|---|
| `text` | `String` | 2.0 | Required label text on the button. |
| `icon_custom_emoji_id` | `String` | **Bot API 9.4** | Optional custom emoji ID shown on the button (requires bot to be allowed to use custom emojis in the message, e.g. bot owner has Premium). |
| `style` | `String` | **Bot API 9.4** | Optional button color style: `"primary"`, `"success"`, or `"danger"` (maps to MTProto `keyboardButtonStyle` `bg_primary`, `bg_success`, `bg_danger`). |
| **Action 1:** `url` | `String` | 2.0 | HTTP(S) or `tg://` link opened when pressed. |
| **Action 2:** `callback_data` | `String` | 2.0 | **1–64 bytes** (UTF-8 byte length, not character count!) sent to the bot in a `CallbackQuery` update. |
| **Action 3:** `web_app` | `WebAppInfo` | 6.0 | Launches a Mini App (`{"url": "https://..."}`) with full `initData` and `query_id` (`answerWebAppQuery`). Not available in channels. |
| **Action 4:** `login_url` | `LoginUrl` | 4.3 | Seamless Telegram Web Login URL (`url`, `forward_text`, `bot_username`, `request_write_access`). |
| **Action 5:** `switch_inline_query` | `String` | 2.0 | Prompts user to pick a chat, opens it, and inserts `@bot_username <query>` in the input field. |
| **Action 6:** `switch_inline_query_current_chat` | `String` | 2.0 | Inserts `@bot_username <query>` directly in the **current** chat's input field. |
| **Action 7:** `switch_inline_query_chosen_chat` | `SwitchInlineQueryChosenChat` | 6.7 | Prompts user to pick a chat filtered by `allow_user_chats`, `allow_bot_chats`, `allow_group_chats`, `allow_channel_chats` and inserts `@bot <query>`. |
| **Action 8:** `copy_text` | `CopyTextButton` | **Bot API 7.11** | Copies `{"text": "..."}` (**1–256 characters**) to the user's clipboard in one tap with native toast feedback. |
| **Action 9:** `callback_game` | `CallbackGame` | 2.1 | Launches the HTML5 Game attached to the message. **Must be the first button in the first row.** |
| **Action 10:** `pay` | `Boolean` | 3.0 | Sends a Pay button on an invoice message (`sendInvoice`). **Must be the first button in the first row.** |
| **Action 11:** `disabled` | `DisabledButton` | **Bot API 10.3** | Pass `{}` (`DisabledButton`) to render the button in a non-interactive disabled state! |

### Minimal Working Example (Styled, Copy-Text, Disabled & Callback Buttons)
```json
{
  "chat_id": 123456789,
  "text": "Order #1042 is ready for pickup.",
  "reply_markup": {
    "force_reply": true,
    "inline_keyboard": [
      [
        {
          "text": "Confirm Pickup",
          "callback_data": "pickup:1042:confirm",
          "style": "success",
          "icon_custom_emoji_id": "5368324170671202286"
        },
        {
          "text": "Cancel Order",
          "callback_data": "pickup:1042:cancel",
          "style": "danger"
        }
      ],
      [
        {
          "text": "Copy Pickup Code",
          "copy_text": { "text": "PK-1042-99X" }
        },
        {
          "text": "Refund (Locked)",
          "disabled": {}
        }
      ]
    ]
  }
}
```

### Handling `CallbackQuery` & `answerCallbackQuery`
- When a user taps a `callback_data` button, Telegram sends an `Update` with `callback_query` (`id`, `from`, `message` as `MaybeInaccessibleMessage`, `inline_message_id`, `chat_instance`, `data`).
- **Always call `answerCallbackQuery(callback_query_id=...)`** — even with no `text` — to stop the loading spinner on the user's button!
- Optional `answerCallbackQuery` fields:
  - `text` (`0–200 characters`): Shown as a toast notification at the top/bottom of the screen, or as a modal alert if `show_alert: true`.
  - `show_alert` (`Boolean`): Shows a popup with an OK button instead of a toast.
  - `url` (`String`): Opens a game URL or `t.me/<bot>?start=XXXX` deep link.
  - `cache_time` (`Integer`, default `0`): Seconds the client may cache the callback result.
- **Ephemeral Callback Replies (Bot API 10.3 & 10.4):** Instead of (or in addition to) a toast, you can call `sendMessage` / `sendRichMessage` / `sendPhoto` etc. with `ephemeral_message_parameters: {"callback_query_id": query.id, "replace_callback_query_message": true}` to show a private ephemeral message (or replace the original message purely for that user!) in any group/chat except channel direct messages.

---

## 2. `ReplyKeyboardMarkup` & `KeyboardButton`

Replaces the user's system keyboard with predefined reply buttons (not available in channels):

| `ReplyKeyboardMarkup` Field | Type | Default | Description |
|---|---|---|---|
| `keyboard` | `Array of Array of KeyboardButton` | Required | Button rows (`KeyboardButton` or plain `String`). |
| `is_persistent` | `Boolean` | `False` | Always show the keyboard when the regular keyboard is hidden. |
| `resize_keyboard` | `Boolean` | `False` | Shrink keyboard vertically to fit button rows (**almost always set `true`**). |
| `one_time_keyboard` | `Boolean` | `False` | Hide keyboard automatically after the user presses a button. |
| `input_field_placeholder` | `String` | Optional | Placeholder shown in the input field when keyboard is active (**1–64 chars**). |
| `selective` | `Boolean` | `False` | Show only to `@mentioned` users in `text` or the sender of `reply_to_message_id`. |
| `force_reply` | `True` | Optional | **Added in Bot API 10.3:** Simultaneously activates reply mode to the message. |

### `KeyboardButton` Action Types (Private Chats Only for Request Actions)

Besides plain text (which sends the button's `text` as a message), a `KeyboardButton` can have `icon_custom_emoji_id` (**9.4+**), `style` (**9.4+**), and **at most one** of these optional request fields:

1. **`request_users` (`KeyboardButtonRequestUsers`, Bot API 6.5 / 7.0):**
   - Opens a native picker to select up to `max_quantity` (`1–10`, default `1`) users matching criteria (`request_id`, `user_is_bot`, `user_is_premium`, `request_name`, `request_username`, `request_photo`).
   - Result arrives in `Message.users_shared` (`UsersShared`).
2. **`request_chat` (`KeyboardButtonRequestChat`, Bot API 6.5 / 7.0):**
   - Opens a native picker to select a group or channel matching criteria (`request_id`, `chat_is_channel`, `chat_is_forum`, `chat_has_username`, `chat_is_created`, `user_administrator_rights`, `bot_administrator_rights`, `bot_is_member`, `request_title`, `request_username`, `request_photo`).
   - Result arrives in `Message.chat_shared` (`ChatShared`).
3. **`request_managed_bot` (`KeyboardButtonRequestManagedBot`, Bot API 9.6 / 10.4):**
   - Prompts the user to create a new **Managed Bot** controlled by your manager bot (`request_id`, `suggested_name`, `suggested_username`).
   - In **Bot API 10.4**, Telegram Premium users can also assign secondary usernames ending in `agent`, `ai`, `app`, `game`, or `gay` to up to 2 owned bots via `suggested_username`.
   - Result arrives in `Message.managed_bot_created` (`ManagedBotCreated`) and `Update.managed_bot` (`ManagedBotUpdated`).
4. **`request_contact` (`Boolean`):** Sends the user's phone number as a `Contact` message.
5. **`request_location` (`Boolean`):** Sends the user's current `Location`.
6. **`request_poll` (`KeyboardButtonPollType`):** Prompts user to create a poll (`{"type": "quiz"}` or `{"type": "regular"}`) and send it.
7. **`web_app` (`WebAppInfo`):** Opens a Mini App that can return data via `Telegram.WebApp.sendData(string)` (up to 4,096 bytes) in `Message.web_app_data`.

### Requesting Users/Chats/Managed Bots from Mini Apps (`savePreparedKeyboardButton` — Bot API 9.6+)
Bots can call `savePreparedKeyboardButton(user_id, button)` with a `KeyboardButton` containing `request_users`, `request_chat`, or `request_managed_bot` to obtain a `PreparedKeyboardButton` (`id`), and then invoke `Telegram.WebApp.requestChat(id, callback)` inside a Mini App!

---

## 3. `ReplyKeyboardRemove` & `ForceReply`

- **`ReplyKeyboardRemove`:** `{"remove_keyboard": true, "selective": false}` — removes the current `ReplyKeyboardMarkup`.
- **`ForceReply`:** `{"force_reply": true, "input_field_placeholder": "Type your answer...", "selective": true}` — automatically opens the reply UI on the user's client pointing to the bot's message.
