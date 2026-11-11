# Webhooks, Edge Hosting (Cloudflare Workers), Telegram Serverless & Broadcast Queues (`references/webhooks-and-hosting.md`)

- **Source:** [Telegram Webhooks Guide](https://core.telegram.org/bots/webhooks), [Telegram Serverless](https://core.telegram.org/bots/serverless), [Bots FAQ](https://core.telegram.org/bots/faq), [grammY Web Bundle](https://github.com/grammyjs/grammy)
- **Verified Against:** **Bot API 10.4** (November 9, 2026; checked November 11, 2026)

---

## 1. Cloudflare Workers & Edge Runtime Webhook Pattern

Edge runtimes (Cloudflare Workers, Vercel Edge, Deno Deploy) terminate CPU/wall-clock execution as soon as the HTTP `Response` is returned unless background work is registered with `ctx.waitUntil(...)`.

### Best Practices for Cloudflare Workers Webhooks
1. **Verify `X-Telegram-Bot-Api-Secret-Token` in Constant Time:** Reject unauthorized requests with `401 Unauthorized` before parsing JSON.
2. **Explicitly Register All Required `allowed_updates`:**
   ```json
   {
     "url": "https://bot.example.workers.dev/webhook",
     "secret_token": "YOUR_RANDOM_64_CHAR_SECRET",
     "allowed_updates": [
       "message",
       "edited_message",
       "callback_query",
       "inline_query",
       "widget_query",
       "shared_widget_query",
       "pre_checkout_query",
       "purchased_paid_media",
       "managed_bot",
       "subscription",
       "stopped_message_generation",
       "guest_message",
       "chat_join_request",
       "my_chat_member"
     ]
   }
   ```
   *(Missing `"widget_query"` or `"shared_widget_query"` causes `"Widget stopped"` errors on Bot API 10.4 widget interactions!)*
3. **Deduplicate `update_id` for Idempotency:** If your webhook handler takes > 5–10 seconds or returns a `5xx` error, Telegram retries the exact same `Update` with the same `update_id`. Store recent `update_id`s in Cloudflare KV / D1 / Redis (or offload slow LLM/media jobs via `ctx.waitUntil(processUpdate(update))` and return `new Response("OK", { status: 200 })` immediately).
4. **Use Web-Compatible Bundles:** When using `grammY` on Cloudflare Workers, import from `"grammy/web"` (`import { Bot, webhookCallback } from "grammy/web"`).

---

## 2. Telegram Serverless (`tgcloud` — Official V8 Isolate Hosting)

Introduced and expanded on **October 6, 2026** ([core.telegram.org/bots/serverless](https://core.telegram.org/bots/serverless)), Telegram Serverless runs bot update handlers, Mini App backend endpoints, static Mini App front-ends (`https://app<app_id>.tgcloud.ai/`), and an integrated SQLite database directly inside Telegram's infrastructure.

### Project Structure (`tgcloud` CLI v0.2.0+)
```text
my-bot/
├── tgcloud/                    # Deployed V8 isolate modules (only .js files here are deployed)
│   ├── handlers/               # Flat folder: 1 file per Update type (e.g. message.js, callback_query.js, widget_query.js)
│   ├── endpoints/              # Flat folder: Mini App RPC endpoints (e.g. getProfile.js -> POST /api/getProfile)
│   ├── lib/                    # Shared helper modules (subdirectories allowed)
│   └── schema.js               # Drizzle-like SQLite table definitions
├── dist/                       # Optional Mini App static front-end build output
└── tgcloud.jsonc               # Static hosting & routing config
```

### Key `tgcloud` Runtime Rules
- **No external npm packages at runtime:** Only `sdk` (`import { api, db, fetch, EndpointError } from 'sdk'` and `import { table, integer, text, boolean, json, index, sql, eq } from 'sdk/db'`) and relative `.js` imports inside `tgcloud/` (`import { helper } from '../lib/helper.js'`) are resolvable.
- **No foreign keys in `schema.js`:** Enforce relational integrity in application logic.
- **Unwrapped Handler Payloads:** `tgcloud/handlers/message.js` receives `(message, ctx)` where `message` is already `update.message` and `ctx.update` holds the raw `Update`.
- **Pre-Verified Mini App Endpoints:** `tgcloud/endpoints/getProfile.js` receives `(input, ctx)` where `ctx.initData` is already cryptographically verified by the platform (unauthenticated requests are rejected with `401` before your code runs). Call from the client via:
  ```javascript
  Telegram.WebApp.Serverless.call('getProfile', { lang: 'en' }, (err, result) => { ... });
  ```
- **Two-Step Deploy & Migrate Workflow:**
  ```bash
  npx tgcloud run handlers/message '{ chat: { id: 1 }, text: "hello" }'  # Test locally on cloud V8
  npx tgcloud push                                                       # Atomic code & static deploy
  npx tgcloud migrate                                                    # Review & apply SQLite schema diff
  ```

---

## 3. Broadcast Queueing & `429 Too Many Requests` Handling

Never broadcast to thousands of users with `Promise.all` or an unthrottled loop. Implement a two-tier token bucket queue:

1. **Global Pacing:** Cap outgoing passive notifications at **25–28 messages/second** (staying safely under the ~30 msg/s free ceiling), or up to **900–1,000 messages/second** when `allow_paid_broadcast: true` is passed.
2. **Per-Chat Pacing:** Ensure at least **1,000 ms** between messages to the same private chat and at most **20 messages / 60 seconds** to the same group/supergroup.
3. **Automatic `retry_after` Backoff & Cleanup:**
   ```python
   async def send_safe(session, token: str, payload: dict) -> dict | None:
       url = f"https://api.telegram.org/bot{token}/sendMessage"
       while True:
           async with session.post(url, json=payload) as resp:
               data = await resp.json()
               if data.get("ok"):
                   return data["result"]
               code = data.get("error_code")
               if code == 429:
                   wait = data.get("parameters", {}).get("retry_after", 5)
                   await asyncio.sleep(wait + 1)
                   continue
               if code == 403:
                   # User blocked bot or kicked from chat -> mark inactive in DB
                   return None
               if code == 400 and "migrate_to_chat_id" in data.get("parameters", {}):
                   payload["chat_id"] = data["parameters"]["migrate_to_chat_id"]
                   continue
               raise RuntimeError(f"Bot API error {code}: {data.get('description')}")
   ```

---

## 4. Testing Environments

- **Dedicated Test Environment ([core.telegram.org/bots/features#dedicated-test-environment](https://core.telegram.org/bots/features#dedicated-test-environment)):**
  - Log into Test DCs (DC 1–3, test phone numbers `99966XYYYY` where login code is `XXXXX`).
  - Message `@BotFather` on the test server to create a test bot.
  - Call Bot API methods with `/test/` inserted after `/bot<token>`:
    `https://api.telegram.org/bot<token>/test/<METHOD_NAME>`
  - Unlocks full testing of **Bot API 10.4 Widgets in groups, inline mode, and forwards**, **Telegram Stars payments without real money**, and **Attachment Menu Mini Apps**.
