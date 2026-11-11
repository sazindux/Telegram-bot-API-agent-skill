# Client Libraries Comparison & Compatibility Matrix

- **Verified Against:** Bot API 10.4 & MTProto Layer 225
- **Verification Date:** November 11, 2026
- **Primary & Official Library Sources:**
  - [grammY (TypeScript/JavaScript Bot Framework)](https://github.com/grammyjs/grammY)
  - [Telegraf (TypeScript/JavaScript Bot Framework)](https://github.com/telegraf/telegraf)
  - [aiogram (Python Async Bot Framework)](https://github.com/aiogram/aiogram)
  - [python-telegram-bot (Python Async Bot Library)](https://github.com/python-telegram-bot/python-telegram-bot)
  - [Telethon (Python Async MTProto Client)](https://github.com/LonamiWebs/Telethon)
  - [Pyrogram (Archived) & Kurigram (Active Python MTProto Fork)](https://github.com/KurimuzonAkuma/pyrogram)
  - [GramJS (TypeScript/JavaScript MTProto Client)](https://github.com/gram-js/gramjs)
  - [TDLib (C++ Cross-Platform Client Library)](https://github.com/tdlib/td)
  - [Official Local Bot API Server (`telegram-bot-api`)](https://github.com/tdlib/telegram-bot-api)

---

## 1. Library Comparison Matrix

| Library | Language | Protocol | Cloudflare Workers / Edge Ready? | Raw API Passthrough (for Day-0 Bot API 10.4 / Layer 225)? | Active Status & Recommended Use Case |
|---|---|---|---|---|---|
| **[grammY](https://github.com/grammyjs/grammY)** | TypeScript / JS | Bot API (HTTP) | **Yes (First-class)** via `webhookCallback(bot, "cloudflare-mod")` | **Yes:** `await bot.api.raw.sendWidget({...})` | **Top recommendation** for TypeScript/JS, Cloudflare Workers, Deno, Bun, and Node.js bots. |
| **[aiogram 3.x](https://github.com/aiogram/aiogram)** | Python (`asyncio`) | Bot API (HTTP) | Python Workers (Pyodide) or ASGI/VPS | **Yes:** `await bot( TelegramMethod / session.make_request )` | **Top recommendation** for Python bots (clean routers, FSM, middleware, webhook return responses). |
| **[python-telegram-bot v21+](https://github.com/python-telegram-bot/python-telegram-bot)** | Python (`asyncio`) | Bot API (HTTP) | VPS / Container / Serverless HTTP | **Yes:** `await bot._post("sendWidget", data)` | Mature, batteries-included Python Bot API library with built-in `JobQueue`. |
| **[Telegraf v4](https://github.com/telegraf/telegraf)** | TypeScript / JS | Bot API (HTTP) | Partial (requires custom adapter or Node compat) | **Yes:** `await ctx.telegram.callApi("sendWidget", {...})` | Legacy/established Node.js bots; lags newer Bot API releases without `callApi`. |
| **[Telethon](https://github.com/LonamiWebs/Telethon)** | Python (`asyncio`) | MTProto | No (requires persistent TCP / filesystem or custom session) | **Yes:** `await client(functions.messages.SendMessageRequest(...))` or custom `TLObject` | **Top recommendation** for Python MTProto userbots, custom clients, and 4 GB file transfers. |
| **[Kurigram](https://github.com/KurimuzonAkuma/pyrogram)** *(fork of [Pyrogram](https://github.com/pyrogram/pyrogram))* | Python (`asyncio`) | MTProto | No (requires persistent TCP + `tgcrypto` C extension) | **Yes:** `await app.invoke(raw.functions.*)` | Decorator-style Python MTProto client. **Note:** Upstream `pyrogram/pyrogram` is unmaintained; use `kurigram` for current layers (Topics, Stories, Stars, Monoforums). |
| **[GramJS](https://github.com/gram-js/gramjs)** | TypeScript / JS | MTProto | Browser (WebSocket) & Node.js TCP | **Yes:** `await client.invoke(new Api.*)` | JavaScript/TypeScript MTProto client (`StringSession` support). |
| **[TDLib](https://github.com/tdlib/td)** | C++ (bindings for Go, Java, Python, C#, Rust) | MTProto (`td_api.tl`) | No (native C++ binary + local SQLite/binlog) | Managed via `td_api.tl` JSON/C++ interface | Full-featured client engine handling encryption, local database cache, and file transfers automatically. |
| **[telegram-bot-api](https://github.com/tdlib/telegram-bot-api)** | C++ server (wraps TDLib) | Bot API HTTP -> MTProto | No (runs on Linux/macOS/Docker VPS) | Exposes full Bot API 10.4 HTTP interface | Official self-hosted Bot API server unlocking 2,000 MB uploads, 4,000 MB downloads, local file paths, and 9999-member `getChat` lists. |

---

## 2. Calling Bot API 10.4 Methods Before Typed SDK Updates (`raw` / Passthrough)

Whenever Telegram releases a new Bot API version (such as **Bot API 10.4** on November 9, 2026 adding `sendWidget`, `sendSharedWidget`, `answerWidgetQuery`, `editMessageWidgetData`, `editSharedWidgetData`, `getChatShareThemeBackdrops`, `getUniqueGift`, `deleteBusinessAccountGift`, and **Bot API 10.2** adding `sendRichMessage` / `sendRichMessageDraft`), client libraries may take days or weeks to ship updated TypeScript/Python definitions.

**Never hallucinate non-existent SDK helper methods** (like `ctx.replyWithWidget()`). Instead, invoke the raw HTTP method dispatcher built into each library:

### 2.1 grammY (TypeScript / Cloudflare Workers) ([Source](https://github.com/grammyjs/grammY))
```typescript
// Call any Bot API 10.4 method directly via bot.api.raw.<methodName>
const sentMessage = await bot.api.raw.sendWidget({
  chat_id: ctx.chat.id,
  url: "https://widgets.example.com/poll-card",
  aspect_ratio: "16:9",
  data: JSON.stringify({ poll_id: "p_42", votes: [12, 8] }),
});

// Listen for Bot API 10.4 widget_query updates via raw update middleware
bot.use(async (ctx, next) => {
  const rawUpdate = ctx.update as Record<string, unknown>;
  if (rawUpdate.widget_query) {
    const wq = rawUpdate.widget_query as { id: string; data?: string };
    await ctx.api.raw.answerWidgetQuery({
      widget_query_id: wq.id,
      data: JSON.stringify({ ok: true }),
    });
    return;
  }
  await next();
});
```

### 2.2 aiogram 3.x (Python) ([Source](https://github.com/aiogram/aiogram))
```python
from typing import Any
from aiogram import Bot
from aiogram.methods.base import TelegramMethod

class SendWidget(TelegramMethod[dict[str, Any]]):
    __returning__ = dict[str, Any]
    __api_method__ = "sendWidget"

    chat_id: int | str
    url: str
    aspect_ratio: str | None = None
    data: str | None = None

# Usage with an initialized Bot(token=os.environ["BOT_TOKEN"]):
# result = await bot(SendWidget(chat_id=123456789, url="https://example.com/widget", aspect_ratio="1:1"))
```

### 2.3 Zero-Dependency `fetch` (Cloudflare Workers / Edge Runtime)
For maximum cold-start performance (`0 ms` framework overhead) and immediate support for every Bot API 10.4 field (`widget_query`, `shared_widget_query`, `RichMessage`, `PaidMessagesWaived`), call `https://api.telegram.org/bot${env.BOT_TOKEN}/${method}` directly with native `fetch` or return the method JSON directly in the HTTP `200 OK` webhook response body ([Source](https://core.telegram.org/bots/api#making-requests-when-getting-updates)).
