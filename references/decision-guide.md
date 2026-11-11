# Decision Guide: Cloud Bot API vs. Local Bot API Server vs. Telegram Serverless vs. MTProto vs. TDLib

- **Verified Against:** Bot API 10.4 & MTProto Layer 225
- **Verification Date:** November 11, 2026
- **Primary Sources:**
  - [Telegram Bot API Specification](https://core.telegram.org/bots/api)
  - [Telegram Serverless (`tgcloud`)](https://core.telegram.org/bots/serverless)
  - [Official Local Bot API Server (`tdlib/telegram-bot-api`)](https://github.com/tdlib/telegram-bot-api)
  - [MTProto API Overview](https://core.telegram.org/api)
  - [Telegram API Terms of Service](https://core.telegram.org/api/terms)

---

## 1. Architectural Decision Matrix

| Requirement / Capability | Hosted Bot API (`api.telegram.org`) | Local Bot API Server (`telegram-bot-api` `--local`) | Telegram Serverless (`tgcloud` / `botrun.org`) | MTProto Client (Telethon / Kurigram / GramJS) | TDLib (`td_api.tl`) |
|---|---|---|---|---|---|
| **Identity Type** | Bot Account (`@BotFather`) | Bot Account (`@BotFather`) | Bot Account (`@BotFather`) | **User Account** OR **Bot Account** | **User Account** OR **Bot Account** |
| **Network Protocol** | HTTPS REST / JSON | HTTP REST / JSON (localhost) | WASI P2 `.wasm` (sandboxed HTTP) | MTProto 2.0 TCP / WebSocket (Binary TL) | MTProto 2.0 (via C++ JSON/native bindings) |
| **Max File Upload** | **50 MB** | **2,000 MB (2 GB)** | **50 MB** (or local server if proxied) | **2,000 MB** (4,000 MB with Premium user) | **2,000 MB** (4,000 MB with Premium user) |
| **Max File Download** | **20 MB** | **4,000 MB (4 GB)** (zero-copy local path) | **20 MB** | **4,000 MB (4 GB)** | **4,000 MB (4 GB)** |
| **Read Historical Messages** | **No** (only incoming updates after bot joins) | **No** (only incoming updates; can export up to 9,999 chat member IDs in `getChat`) | **No** | **Yes** (`messages.getHistory`, `messages.search`) | **Yes** (`getChatHistory`, `searchChatMessages`) |
| **Initiate DM to Arbitrary User** | **No** (user must `/start` bot, interact with widget/Mini App, or approve chat request) | **No** | **No** | **Yes** (as User account, subject to spam/FloodWait rules) | **Yes** (as User account) |
| **Join Public/Private Channels & Scrape/Analyze** | **No** (bots cannot join via invite link on their own; must be added by admin) | **No** | **No** | **Yes** (`channels.joinChannel`, `messages.importChatInvite`) | **Yes** (`joinChat`, `joinChatByInviteLink`) |
| **In-Chat HTML Widgets (`sendWidget`), Mini Apps, Stars Invoices, Inline Mode** | **Yes (First-class)** | **Yes (First-class)** | **Yes (First-class)** | Supported (via raw TL constructors, much more verbose) | Supported (via `td_api.tl`) |
| **Webhook ports & SSL** | `443, 80, 88, 8443` (HTTPS required) | **Any port (`1–65535`)**, HTTP or HTTPS (`--local`) | Managed automatically by Telegram | N/A (Persistent TCP socket) | N/A (Persistent TCP socket) |
| **Infrastructure Needed** | Any serverless edge (Cloudflare Workers) or VPS | Linux/Docker VPS (`2+ GB RAM` recommended for TDLib cache) | **None** (hosted on Telegram infrastructure, paid via Stars) | Persistent process (VPS/container) with disk/DB for `.session` | Persistent process with local disk for TDLib SQLite DB |

---

## 2. Flowchart: Which Stack Should You Choose?

1. **Are you building a standard Bot, Mini App backend, Stars payment flow, or In-Chat Widget (`sendWidget`) with files `<= 20 MB` (download) / `<= 50 MB` (upload)?**
   - **Yes -> Hosted Bot API (`https://api.telegram.org`)** with **Cloudflare Workers** (`grammY` or native `fetch`) or a Python **aiogram 3.x** service. Zero state management, instant webhook delivery.
2. **Do you want zero external cloud hosting bills and want to pay with your bot's Telegram Stars balance?**
   - **Yes -> Telegram Serverless (`tgcloud`)** ([Source](https://core.telegram.org/bots/serverless)). Compile your bot to a WASI Preview 2 (`wasip2`) `.wasm` component, declare external domains in `manifest.json`, and deploy with `tgcloud deploy`.
3. **Is your Bot processing large videos, documents, or audio files (`20 MB – 4 GB`), or do you need the full member list (up to 9,999 members) of a chat via `getChat`?**
   - **Yes -> Official Local Bot API Server (`tdlib/telegram-bot-api --local`)** ([Source](https://github.com/tdlib/telegram-bot-api)). Your bot code still uses standard Bot API libraries (`grammY` / `aiogram`), pointed at `http://127.0.0.1:8081/bot<token>/<method>`, reading downloaded files directly from local disk paths (`file.file_path`) without HTTP download limits.
4. **Do you need to read past message history before the bot joined, search global messages, join channels via invite links, or automate a personal User account?**
   - **Yes -> MTProto Client (`Telethon`, `Kurigram`, or `GramJS`)** or **TDLib**. Note that automating a personal user account ("userbot") carries strict anti-spam and Terms of Service rules (Section 3 below).

---

## 3. Account-Ban Risks, Terms of Service & Safety Rules for MTProto Userbots

Operating an MTProto client logged in as a **User account** is governed by the [Telegram API Terms of Service](https://core.telegram.org/api/terms) and anti-abuse systems ([Source](https://core.telegram.org/api/obtaining_api_id), [Source](https://core.telegram.org/api/errors)):

1. **Never Cold-DM or Mass-Invite Unsolicited Users:**
   - Sending unsolicited messages to users who do not share a contact relationship or mutual group, or calling `channels.inviteToChannel` in bulk, triggers `PEER_FLOOD` (`400`), temporary restrictions (inspected via `@SpamBot`), or permanent `USER_DEACTIVATED_BAN` (`401`).
2. **Never Share `.session` Files Across IPs (`AUTH_KEY_DUPLICATED`):**
   - Using the same MTProto `auth_key` simultaneously from two different IP addresses (e.g., running locally while a cloud container is still active) triggers `406 AUTH_KEY_DUPLICATED` and can invalidate **all** active sessions on the account.
3. **Avoid Rapid Login/Logout Loops & Fresh VOIP Numbers:**
   - Repeatedly calling `auth.sendCode` / `auth.logOut` in automated CI scripts triggers `FLOOD_WAIT_X` (often 24–72 hours) or flags the account as a spam farm.
   - Always persist the session string (`StringSession` in Telethon/GramJS) or SQLite session file across restarts, and pass `future_auth_tokens` in `codeSettings` when re-authenticating ([Source](https://core.telegram.org/api/auth)).
   - For automated testing, connect to the **Telegram Test Data Centers** (DC 2 test IP `149.154.167.40`, test phone numbers `99966XYYYY` where `X` is `1..3` for DC 1..3 and confirmation code is `XXXXX` repeated 5 times) rather than production accounts ([Source](https://core.telegram.org/api/auth#test-accounts)).
4. **Always Obey `FLOOD_WAIT_X`:**
   - When the server returns `420 FLOOD_WAIT_X`, pause requests on that method/session for `X` seconds. Continuously hammering the server during an active flood wait escalates the ban duration or results in IP/account suspension ([Source](https://core.telegram.org/api/errors)).
5. **Account Recovery (`recover@telegram.org`):**
   - If a legitimate developer account or testing number is mistakenly banned by automated anti-spam filters (`PHONE_NUMBER_BANNED` / `USER_DEACTIVATED_BAN`), appeal via email to `recover@telegram.org` or through `@SpamBot` with the phone number and `api_id` details ([Source](https://core.telegram.org/api/obtaining_api_id)).
