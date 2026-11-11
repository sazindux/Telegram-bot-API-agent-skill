# Telegram Bot API (v10.4) & MTProto (Layer 225) Agent Skill

[![Bot API](https://img.shields.io/badge/Telegram_Bot_API-10.4_(Nov_9,_2026)-0088cc?logo=telegram)](https://core.telegram.org/bots/api)
[![MTProto](https://img.shields.io/badge/MTProto-Layer_225-26A5E4?logo=telegram)](https://core.telegram.org/schema)
[![Coverage](https://img.shields.io/badge/Coverage-186_Methods_%7C_402_Types_(100%25)-brightgreen)](./COVERAGE.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

A complete, primary-source-verified **AI Agent Skill** for the **Telegram Bot API (v10.4)**, **In-Chat HTML Widgets**, **Mini Apps (WebApps)**, **Telegram Serverless (`tgcloud`)**, and **MTProto (Layer 225)**. Built so AI coding assistants (Claude Code, Cursor, OpenCode, Gemini, Windsurf, GitHub Copilot) can write accurate, current Telegram code without guessing or hallucinating outdated parameters.

- **Verified Against:** [Telegram Bot API 10.4](https://core.telegram.org/bots/api) (released November 9, 2026) & [MTProto Layer 225](https://core.telegram.org/api/layers)
- **Verification Date:** November 11, 2026
- **Coverage Audit:** **186 / 186** Bot API methods (100.0%) and **402 / 402** Bot API object & union types (100.0%) documented — see [`COVERAGE.md`](./COVERAGE.md) and [`VERIFICATION_LOG.md`](./VERIFICATION_LOG.md).

## Key Features

- **100% Bot API 10.4 Reference (`references/bot-api/`):** Complete signatures, parameter tables, limits, and version tags for all 186 methods and 402 types, including Bot API 10.4 **In-Chat HTML Widgets** (`sendWidget`, `sendSharedWidget`, `answerWidgetQuery`, `editMessageWidgetData`, `editSharedWidgetData`, TON wallet queries), Bot API 10.1–10.3 **Rich Messages** (`sendRichMessage`, `sendRichMessageDraft`, 32,768-char limit, compact tables, buttons), and Bot API 10.2–10.4 **Ephemeral Messages** (`EphemeralMessageParameters`).
- **Deep Formatting & UTF-16 Entity Math (`references/formatting.md`):** Exact escaping rules for `HTML`, `MarkdownV2`, and legacy `Markdown`, surrogate-pair UTF-16 offset calculation, expandable blockquotes (`<blockquote expandable>` / `>...||`), `<tg-time>` (`date_time`) entities, custom emoji, `ton_address`, and `bank_card_number` entities.
- **Mini Apps, In-Chat Widgets & Login (`references/mini-apps.md`, `references/widgets-and-login.md`):** Full `window.Telegram.WebApp` SDK (`telegram-web-app.js?65`), `window.TelegramWidget` QuickJS sandbox (`<= 4,096 B` zlib-9), `initData` HMAC-SHA256 & Ed25519 third-party verification, OAuth 2.0 / OIDC Login (`core.telegram.org/widgets/login`), and `t.me` / `tg://` deep links.
- **Stars (`XTR`), Gifts, Business & Agentic Flows (`references/payments-stars-business.md`):** Digital/physical payments, Star subscriptions, paid media (up to 25,000 Stars), paid broadcasts (0.1 Stars/msg up to 1,000 msg/s), regular & unique collectible gifts, Business Bots, Managed Bots (`t.me/newbot/...`), Guest Mode (`answerGuestQuery`), Bot-to-Bot communication, Channel Direct Messages (Monoforums), Suggested Posts, and Checklists.
- **MTProto Layer 225 Technical Reference (`references/mtproto/`):** Binary TL serialization, MTProto 2.0 AES-256-IGE key derivation, DH `auth_key` exchange, Abridged/Intermediate/Padded/Full transports & AES-256-CTR obfuscation, SRP 6a 2FA math, `pts`/`qts`/`seq` update state machine, chunked file transfers (`file_reference` refresh), and Peer ID <-> Bot API Dialog ID conversion (including the Monoforum range `-4000000000000` to `-2002147483649`).
- **Deterministic CLI Scripts (`scripts/`) & Runnable Examples (`examples/`):** Ready-to-run Python 3 utilities for `initData` validation, `MarkdownV2` escaping, UTF-16 entity offsets, Dialog ID conversion, and coverage auditing, plus Cloudflare Workers (`grammY`) and Python (`aiogram`, `Telethon`, `Pyrogram`) templates.

## Repository Structure

```text
telegram-api-skill/
├── SKILL.md                        # Agent skill frontmatter + progressive-disclosure router (<500 lines)
├── SKILL-single-file.md            # Complete single-file edition — entire skill inlined (drop into any AI chat, ~100k tokens)
├── README.md                       # Human overview, installation, usage, and contribution guide
├── LICENSE                         # MIT License
├── CHANGELOG.md                    # Skill release history
├── VERIFICATION_LOG.md             # Verified claims, doc vs runtime discrepancies, UNVERIFIED log, 10-task test audit
├── SOURCES.md                      # Every official Telegram URL & repo crawled with access dates
├── COVERAGE.md                     # 186/186 methods & 402/402 types coverage audit report
├── RESEARCH_STATE.md               # Phase 1-5 execution checklist
├── references/
│   ├── bot-api/
│   │   ├── core-and-updates.md     # Auth, HTTP formats, Update types, webhooks vs polling, rate & file limits, errors
│   │   ├── methods.md              # All 186 Bot API 10.4 methods grouped by category with signatures & version tags
│   │   └── types.md                # All 402 Bot API 10.4 types grouped by category with fields & version tags
│   ├── formatting.md               # MessageEntity UTF-16 math, HTML vs MarkdownV2, <tg-time>, Rich Messages (32,768 chars)
│   ├── keyboards-and-buttons.md    # Inline & reply keyboards, button styles/colors, copy_text, request_*, callback limits
│   ├── mini-apps.md                # window.Telegram.WebApp full reference, initData validation, storage, sensors, Serverless
│   ├── widgets-and-login.md        # Bot API 10.4 In-Chat HTML Widgets (TelegramWidget), OIDC/Legacy Login, deep links
│   ├── payments-stars-business.md  # Stars (XTR), subscriptions, paid media, gifts, Business/Managed/Guest bots, Monoforums
│   ├── webhooks-and-hosting.md     # Cloudflare Workers, Telegram Serverless (tgcloud), Local Bot API server, 429 queues
│   ├── whats-new.md                # Per-version changelog breakdown (Bot API 6.0 -> 10.4 & MTProto Layers 196 -> 225)
│   ├── mtproto/
│   │   ├── protocol-and-transport.md # TL binary serialization, MTProto 2.0 AES-256-IGE, DH exchange, transports, MTProxy
│   │   ├── auth-and-sessions.md    # User/Bot login, SRP 6a 2FA math, QR/Passkey/OAuth, DC migration, tmp_sessions
│   │   └── updates-files-and-ids.md # pts/qts/seq getDifference, upload/download chunks, file_reference, Dialog ID ranges
│   ├── libraries.md                # grammY, Telegraf, aiogram, python-telegram-bot, Telethon, Pyrogram/Kurigram, GramJS, TDLib
│   ├── decision-guide.md           # When to use Bot API vs Local Bot API vs Telegram Serverless vs MTProto vs TDLib
│   └── pitfalls.md                 # Common mistakes & anti-patterns with production-ready fixes
├── examples/
│   ├── cloudflare-worker-grammy/   # JavaScript (JSDoc-typed) Cloudflare Worker (webhook secret, sendWidget, sendInvoice, initData)
│   ├── python-aiogram/             # Python 3 aiogram v3 bot (MarkdownV2, Stars XTR payments, sendMessageDraft streaming)
│   └── python-mtproto/             # Python 3 Telethon & Pyrogram/Kurigram userbot/bot examples (2FA, FloodWait, raw TL)
├── scripts/
│   ├── validate_initdata.py        # CLI & library for Mini App initData and Login Widget HMAC-SHA256 verification
│   ├── escape_markdown_v2.py       # Context-aware MarkdownV2 escaper (body, code/pre, inline URL)
│   ├── utf16_entity_offsets.py     # UTF-16 offset/length calculator & MessageEntity builder
│   ├── dialog_id_converter.py      # Bi-directional MTProto Peer ID <-> Bot API Dialog ID converter (incl. Monoforums)
│   └── coverage_audit.py           # Automated 186-method / 402-type coverage auditor
└── .github/
    └── workflows/
        ├── ci-lint-and-links.yml       # Runs helper-script self-tests, coverage audit and secret-leak scan on push/PR
        ├── changelog-monitor.yml       # Daily check of core.telegram.org for new Bot API versions / MTProto layers; opens an issue on change
        └── integration-smoke-test.yml  # Optional live Bot API smoke test (getMe, getWebhookInfo, getMyStarBalance, send+delete round-trip) — enable with BOT_TOKEN & TEST_CHAT_ID repo secrets
```

## Installation & Usage

### Option 1: Install as an Agent Skill
Copy the `telegram-api-skill` directory into your agent's `skills/` directory:

```bash
# Claude Code / OpenCode / Cursor / Gemini Skills directory
cp -r telegram-api-skill ~/.claude/skills/telegram-api-skill
```

The agent will automatically read [`SKILL.md`](./SKILL.md) and load the appropriate reference file from `references/` based on your prompt.

### Option 2: Run the Bundled Helper Scripts

```bash
# 1. Compute exact UTF-16 offsets and lengths for MessageEntity
python3 scripts/utf16_entity_offsets.py "Hello 👨‍👩‍👧‍👦 World!" "World"

# 2. Escape text safely for MarkdownV2
python3 scripts/escape_markdown_v2.py "Price: $19.99 (save 20%!) -> https://t.me/durov"

# 3. Validate Mini App initData HMAC-SHA256 signature
python3 scripts/validate_initdata.py --bot-token "$BOT_TOKEN" --init-data "$RAW_INIT_DATA"

# 4. Convert between MTProto Peer IDs and Bot API Dialog IDs (including Monoforums)
python3 scripts/dialog_id_converter.py -2500000000000

# 5. Run the 100% Bot API 10.4 coverage audit
python3 scripts/coverage_audit.py
```

## Single-File Edition: [`SKILL-single-file.md`](./SKILL-single-file.md)

The **entire skill** — every reference document, the full 186-method and 402-type catalogs, all five helper-script sources, and all runnable examples — is also available as **one self-contained file** (~395 KB, ≈100k tokens). Nothing was removed: it is the multi-file skill merged 1:1, with a **Source File ↔ Location Map**, a **Table of Contents**, and agent-facing usage instructions in the header.

### When to Use It

- **Drop into any AI agent chat:** Paste the whole file directly into a conversation (Claude, Gemini, GPT, Cursor, Windsurf — any agent with a large context window) or attach it as a project / system document. No repository, file tree, or `skills/` directory required.
- **Install as an agent skill:** The file keeps the YAML `name` / `description` frontmatter, so skill platforms (Claude Code, OpenCode, etc.) auto-index it exactly like the multi-file version.
- **Offline / single-artifact bundle:** Ship one file instead of the whole repository.

### How to Use It

1. Paste the entire file into the agent's context, or place it next to your prompt and tell the agent to read it.
2. The agent reads the **"How to Use This Document"** header (6 numbered instructions, including the hard invariants), then jumps to the relevant **Part 1–17** or **Appendix A–G** via the Table of Contents for the task at hand.
3. The five helper scripts are embedded with full source in **Appendix D** — in a chat-only setting the agent writes the file first (exact filenames given), then runs it.
4. The three runnable example projects (Cloudflare Worker + grammY, aiogram v3, Telethon/Pyrogram) are in **Appendix E**, deployable as-is.

### Context-Window Notes

- ≈100k tokens — fits comfortably in 200k-context agents (Claude, Gemini); workable in 128k-context agents when the conversation stays focused.
- For smaller-context agents, paste only the needed **Part** (each is self-contained) or use the multi-file version above.

### Verification

The single file was generated programmatically from this repository: every source file's content is asserted byte-present, and the 186/186 method and 402/402 type counts are re-verified inside the document itself. After updating the multi-file references, regenerate the single file from the updated sources.

## Contributing

1. **Primary Sources Only:** Every method, type, field, or limit added to `references/` must cite its exact anchor on `https://core.telegram.org/bots/api`, `https://core.telegram.org/bots/api-changelog`, or `https://core.telegram.org/api/layers`.
2. **Never Guess:** If a behavior is undocumented or cannot be confirmed against official docs/schemas, mark it `UNVERIFIED` and log it in [`VERIFICATION_LOG.md`](./VERIFICATION_LOG.md).
3. **Run the Audit:** Run `python3 scripts/coverage_audit.py` before opening a pull request to verify 100% method and type coverage and ensure zero leaked tokens.

## License

Released under the [MIT License](./LICENSE).
