# Rich Text Formatting, Message Entities & Rich Messages (`references/formatting.md`)

- **Source:** [Formatting Options](https://core.telegram.org/bots/api#formatting-options), [Rich Messages](https://core.telegram.org/bots/api#rich-messages), [Styled Text with Message Entities (MTProto)](https://core.telegram.org/api/entities)
- **Verified Against:** **Bot API 10.4** (November 9, 2026; checked November 11, 2026)

---

## 1. Message Length Limits

| Surface / Method | Max Length | Counting Unit | Notes |
|---|---|---|---|
| `sendMessage` / `editMessageText` (`text`) | **4,096** characters | UTF-8 characters (after entity parsing) | Use `sendRichMessage` if you need longer structured messages. |
| Media `caption` (`sendPhoto`, `sendVideo`, `sendWidget`, etc.) | **1,024** characters | UTF-8 characters (after entity parsing) | `show_caption_above_media: true` supported on photos, videos, animations, paid media, and widgets. |
| `sendRichMessage` / `sendRichMessageDraft` (`RichMessage`) | **32,768** characters | Rich message content | Introduced in **Bot API 10.1** (June 11, 2026). |
| `TextQuote` (`ReplyParameters.quote`) | **1,024** characters | UTF-8 characters | Must be an exact substring of the replied-to message. |
| `Poll.question` / `Poll.explanation` / `PollOption.text` | `1–300` / `0–200` / `1–100` | Characters | Poll `description` (Bot API 9.6+) supports formatting entities. |

---

## 2. UTF-16 `MessageEntity` Offsets & Lengths (Critical Rule)

Even though all Bot API and MTProto strings are transmitted in **UTF-8**, `MessageEntity.offset` and `MessageEntity.length` are defined in **UTF-16 code units** ([core.telegram.org/api/entities#entity-length](https://core.telegram.org/api/entities#entity-length)):

- **BMP characters (`U+0000` to `U+FFFF`):** ASCII, Latin, Cyrillic, Sinhala, CJK, etc. = **1 UTF-16 code unit**.
- **Supplementary plane characters (`U+10000` to `U+10FFFF`):** Most emojis (`👍`, `🚀`, `👨‍👩‍👧‍👦`), mathematical symbols = **2 UTF-16 code units** (a surrogate pair) per code point!
  - Example: `"Hi 👍 World"` -> `"Hi "` is 3 UTF-16 units (`offset=0, length=3`), `"👍"` is **2 UTF-16 units** (`offset=3, length=2`), `" World"` starts at `offset=5` (`not 4` in Python `len()` and `not 7` in UTF-8 bytes!).
- **Trailing Whitespace Rule:** An entity's `length` must **not** include trailing newlines or spaces (`rtrim` before computing length), though the `offset` of subsequent entities includes all preceding whitespace.
- **Entity-Based Sending vs `parse_mode`:** You can pass an explicit `entities` (or `caption_entities`) array of `MessageEntity` objects **instead of** `parse_mode`. When passing `entities` directly, **no escaping is required** in `text`!

### Fast UTF-16 Code Unit Calculation (Without Full String Re-encoding)
Per [core.telegram.org/api/entities#computing-entity-length](https://core.telegram.org/api/entities#computing-entity-length), any UTF-8 lead byte `>= 0xF0` (`0b11110xxx`) starts a 4-byte supplementary code point (2 UTF-16 units), while any other non-continuation byte (`(byte & 0xC0) != 0x80`) is 1 UTF-16 unit:

```python
def utf16_len(text: str) -> int:
    return len(text.encode("utf-16-le")) // 2

def utf16_slice(text: str, offset: int, length: int) -> str:
    raw = text.encode("utf-16-le")
    return raw[offset * 2 : (offset + length) * 2].decode("utf-16-le")
```
*(See `scripts/utf16_entity_offsets.py` for a full CLI & library helper.)*

---

## 3. Complete `MessageEntity` Types Table (Bot API 10.4)

Source: [core.telegram.org/bots/api#messageentity](https://core.telegram.org/bots/api#messageentity)

| `type` Value | Extra Fields on `MessageEntity` | HTML Syntax | `MarkdownV2` Syntax | Notes & Version |
|---|---|---|---|---|
| `bold` | — | `<b>bold</b>`, `<strong>bold</strong>` | `*bold*` | Nestable (except inside `pre`/`code`). |
| `italic` | — | `<i>italic</i>`, `<em>italic</em>` | `_italic_` | In MarkdownV2, adjacent `_` for underline+italic requires `\r` separator. |
| `underline` | — | `<u>underline</u>`, `<ins>underline</ins>` | `__underline__` | Nestable. |
| `strikethrough` | — | `<s>strike</s>`, `<strike>`, `<del>` | `~strike~` | Nestable. |
| `spoiler` | — | `<tg-spoiler>spoiler</tg-spoiler>` or `<span class="tg-spoiler">spoiler</span>` | `\|\|spoiler\|\|` | Animated hidden text. |
| `blockquote` | — | `<blockquote>quote</blockquote>` | `>line 1\n>line 2` | Block quotation (Bot API 7.0+). Cannot be nested inside another quote. |
| `expandable_blockquote` | — | `<blockquote expandable>quote</blockquote>` | `**>line 1\n>line 2\|\|` | Collapsed-by-default quote (Bot API 7.4+). Note trailing `\|\|` in MarkdownV2! |
| `code` | — | `<code>inline code</code>` | `` `inline code` `` | Fixed-width inline code; cannot contain nested entities. |
| `pre` | `language` (`String`, optional) | `<pre><code class="language-python">...</code></pre>` or `<pre>...</pre>` | ` ```python\n...\n``` ` | Preformatted code block; cannot be nested. |
| `text_link` | `url` (`String`) | `<a href="https://example.com">text</a>` | `[text](https://example.com)` | Inline URL link. |
| `text_mention` | `user` (`User`) | `<a href="tg://user?id=123456789">Name</a>` | `[Name](tg://user?id=123456789)` | Mentions a user by ID (even without a username). |
| `custom_emoji` | `custom_emoji_id` (`String`) | `<tg-emoji emoji-id="5368324170671202286">👍</tg-emoji>` | `![👍](tg://emoji?id=5368324170671202286)` | Inner text must be a valid standard replacement emoji. Allowed for all bots in private/group/supergroup if bot owner has Telegram Premium (**Bot API 9.4+**) or if chat has custom emoji pack. |
| `date_time` | `unix_time` (`Integer`), `date_time_format` (`String`, optional) | `<tg-time unix="1647531900" format="wDT">22:45 tomorrow</tg-time>` | `![22:45 tomorrow](tg://time?unix=1647531900&format=wDT)` | Interactive localized date/time (**Bot API 9.5+**; allowed in checklists, quotes, and gifts in **9.6+**). Cannot be nested. |
| `mention` | — | Auto-parsed (`@username`) | Auto-parsed (`@username`) | Mention by username. |
| `hashtag` | — | Auto-parsed (`#hashtag` or `#hashtag@chatusername`) | Auto-parsed | `#hashtag@username` supported since Bot API 7.11. |
| `cashtag` | — | Auto-parsed (`$USD` or `$USD@chatusername`) | Auto-parsed | `$CASHTAG@username` supported since Bot API 7.11. |
| `bot_command` | — | Auto-parsed (`/start@bot`) | Auto-parsed | Up to 32 chars (`a-z`, `0-9`, `_`). |
| `url` | — | Auto-parsed (`https://...`) | Auto-parsed | Plain URL in text. |
| `email` | — | Auto-parsed (`user@example.com`) | Auto-parsed | Plain email in text. |
| `phone_number` | — | Auto-parsed (`+1-212-555-0123`) | Auto-parsed | Phone number. |
| `bank_card_number` | — | Auto-parsed | Auto-parsed | Bank card number (**added in Bot API 10.4**). |
| `ton_address` | — | Auto-parsed | Auto-parsed | TON blockchain address (**added in Bot API 10.4**). |

### `date_time` (`<tg-time>`) Format String Flags (Bot API 9.5+)
- `unix_time` (`unix` attribute): Unix timestamp between `0` and `current_time + 1098 days` (`time() + 1098 * 86400`).
- `date_time_format` (`format` attribute):
  - Empty / omitted: Keeps the fallback inner text as a clickable link (max 127 UTF-16 units) that opens a native menu (Copy date, Add to system calendar, Schedule reminder).
  - `r`: Relative time (`in 10 minutes`, `2 hours ago`), live-updated by the client. Cannot be combined with other flags.
  - Combos of `w` (day of week), `d` (short date) or `D` (long date), and `t` (short time HH:MM) or `T` (long time HH:MM:SS) — e.g. `wDT`, `dt`, `D`. Max fallback text span when flags are set: **31 UTF-16 code units**.

---

## 4. `HTML` vs `MarkdownV2` Escaping Rules

### `HTML` Mode (`parse_mode: "HTML"`)
Only **3 characters** need escaping in normal text (and `"` inside `href="..."` attributes):
- `<` -> `&lt;`
- `>` -> `&gt;`
- `&` -> `&amp;`
- `"` -> `&quot;` (inside attributes)

> **Recommendation:** Prefer `parse_mode: "HTML"` or explicit `entities` over `MarkdownV2` in production bots — HTML requires escaping only 3 characters instead of 18.

### `MarkdownV2` Mode (`parse_mode: "MarkdownV2"`)
1. **In all normal text (outside `pre`, `code`, and `(...)` link targets):**
   You **MUST** prepend a backslash `\` before all **18 reserved characters** (ASCII codes 1–126):
   ```text
   _ * [ ] ( ) ~ ` > # + - = | { } . !
   ```
   *(And escape `\` itself as `\\`!)*
2. **Inside `pre` and `code` entities:**
   Escape only **2 characters**: `` ` `` (backtick) and `\` (backslash) -> `` \` `` and `\\`.
3. **Inside the `(...)` URL part of inline links `[text](url)` and custom emoji/time `![alt](tg://...)`:**
   Escape only **2 characters**: `)` (closing parenthesis) and `\` (backslash) -> `\)` and `\\`.
4. **Legacy `"Markdown"` Mode (`parse_mode: "Markdown"`):**
   Deprecated legacy mode from Bot API 1.0. Does not support nesting, underline, strikethrough, spoilers, blockquotes, custom emoji, or `<tg-time>`. Never use `"Markdown"` in new code; always use `"HTML"` or `"MarkdownV2"`.

---

## 5. Rich Messages (`sendRichMessage` & `sendRichMessageDraft`) — Bot API 10.1–10.4

Introduced in **Bot API 10.1** (June 11, 2026) and expanded in **10.2** (July 14, 2026), **10.3** (August 24, 2026), and **10.4** (November 9, 2026), Rich Messages allow bots (especially AI agents and report generators) to send structured, multi-block documents up to **32,768 characters** with native tables, math expressions, collapsible details, pull quotes, slideshows, collages, embedded media, thinking blocks, and inline buttons.

### Sending & Streaming Methods
- **`sendRichMessage`**: Sends a final `InputRichMessage` to a chat. Returns `Message` (with `message.rich_message` populated).
- **`sendRichMessageDraft`**: Streams partial rich messages in private chats while generating a reply.
  - Supports `can_stop: true` and `keep_on_stop: true` (**Bot API 10.3+**). When the user taps Stop, the bot receives an `Update` with `stopped_message_generation` (`MessageGenerationStopped`).
- **`sendMessageDraft`**: Streams partial regular text messages (all bots since **Bot API 9.5**; empty `text: ""` allowed since **Bot API 10.0** to display a native *"Thinking…"* indicator).

### `InputRichMessage` Structure
An `InputRichMessage` can be constructed either via rich HTML/Markdown text (with optional `media` array of `InputRichMessageMedia` and `tg://document?id=...` references) or explicitly via `blocks` (`Array of InputRichBlock`):

- **31 Inline `RichText` Types (10.1–10.4):**
  `RichTextPlain`, `RichTextBold`, `RichTextItalic`, `RichTextUnderline`, `RichTextStrikethrough`, `RichTextSpoiler`, `RichTextDateTime`, `RichTextTextMention`, `RichTextSubscript`, `RichTextSuperscript`, `RichTextMarked`, `RichTextCode`, `RichTextCustomEmoji`, `RichTextMathematicalExpression` (LaTeX math!), `RichTextUrl`, `RichTextEmailAddress`, `RichTextPhoneNumber`, `RichTextBankCardNumber`, `RichTextTonAddress` (**10.4**), `RichTextMention`, `RichTextHashtag`, `RichTextCashtag`, `RichTextBotCommand`, `RichTextButton` (**10.3**), `RichTextAnchor`, `RichTextAnchorLink`, `RichTextReference`, `RichTextReferenceLink`.
- **25 Block `RichBlock` / `InputRichBlock` Types (10.1–10.3):**
  - Text & Structure: `InputRichBlockParagraph`, `InputRichBlockSectionHeading`, `InputRichBlockPreformatted`, `InputRichBlockFooter`, `InputRichBlockDivider`, `InputRichBlockAnchor`, `InputRichBlockList` (`InputRichBlockListItem`)
  - Quotes & Collapsibles: `InputRichBlockBlockQuotation`, `InputRichBlockExpandableBlockQuotation` (**10.3**), `InputRichBlockPullQuotation`, `InputRichBlockDetails` (collapsible `<details>`), `InputRichBlockThinking` (`<tg-thinking>` reasoning placeholder)
  - Tables, Math & Interactive: `InputRichBlockTable` (with `RichBlockTableCell` and `is_compact: true` in **10.3**), `InputRichBlockMathematicalExpression`, `InputRichBlockButtons` (`RichMessageButton`, **10.3**)
  - Media & Layout: `InputRichBlockCollage`, `InputRichBlockSlideshow`, `InputRichBlockMap`, `InputRichBlockAnimation`, `InputRichBlockAudio`, `InputRichBlockDocument` (**10.3**), `InputRichBlockPhoto`, `InputRichBlockVideo`, `InputRichBlockVoiceNote`
- **Quoting Rich Messages (Bot API 10.4):** `TextQuote.rich_texts` and `ReplyParameters.quote_rich_texts` allow quoting formatted `RichText` spans from a `RichMessage`.

---

## 6. Link Previews & Reply Parameters (`LinkPreviewOptions` & `ReplyParameters`)

Introduced in **Bot API 7.0** (replacing `disable_web_page_preview` and `reply_to_message_id`):

```json
{
  "chat_id": 123456789,
  "text": "See the status page for details.",
  "link_preview_options": {
    "is_disabled": false,
    "url": "https://status.example.com",
    "prefer_small_media": false,
    "prefer_large_media": true,
    "show_above_text": true
  },
  "reply_parameters": {
    "message_id": 42,
    "chat_id": -1001234567890,
    "allow_sending_without_reply": true,
    "quote": "exact substring from message 42",
    "quote_parse_mode": "HTML",
    "checklist_task_id": 3,
    "poll_option_id": "opt_1"
  }
}
```
- **Cross-Chat Replies:** `ReplyParameters.chat_id` lets a bot reply to a message from *another* chat or channel (producing an `ExternalReplyInfo` on the sent `Message`).
- **Specific Item Replies:**
  - `checklist_task_id` (**Bot API 9.2+**): Replies to a specific task in a `Checklist`.
  - `poll_option_id` (**Bot API 9.6+**): Replies to a specific `PollOption.persistent_id`.
  - `ephemeral_message_id` (**Bot API 10.2+**): Replies to an ephemeral message (`message_id` becomes optional).
  - `quote_rich_texts` (**Bot API 10.4+**): Quotes rich text from a `RichMessage`.
