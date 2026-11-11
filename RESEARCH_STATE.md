# Research & Build State Tracker (`RESEARCH_STATE.md`)

- **Target Latest Bot API Version:** **Bot API 10.4** (Released November 9, 2026) — Verified from [Telegram Bot API Changelog](https://core.telegram.org/bots/api-changelog)
- **Target Latest MTProto Layer:** **Layer 225** — Verified from [MTProto API Layers](https://core.telegram.org/api/layers)
- **Date Checked:** November 11, 2026

---

## Phase Checklist

- [x] **PHASE 1 — DISCOVERY & SOURCE MAP**
  - [x] Verify latest Bot API version (`10.4`, Nov 9, 2026) and MTProto layer (`Layer 225`).
  - [x] Crawl Bot API specification (`https://core.telegram.org/bots/api`) and full changelog (`https://core.telegram.org/bots/api-changelog`) from Bot API 6.0 through 10.4 (all 28 releases).
  - [x] Crawl Bot Platform docs (`/bots/features`, `/bots/webapps`, `/bots/widgets`, `/bots/serverless`, `/bots/payments-stars`, `/bots/webhooks`, `/bots/self-signed`, `/bots/faq`, `/bots/games`, `/widgets/login`).
  - [x] Crawl MTProto specification (`/mtproto`, `/mtproto/description`, `/mtproto/mtproto-transports`, `/mtproto/transports`, `/mtproto/serialize`, `/mtproto/auth_key`, `/mtproto/service_messages`, `/schema`, `/api/layers`, `/api/obtaining_api_id`, `/api/auth`, `/api/srp`, `/api/qr-login`, `/api/datacenter`, `/api/updates`, `/api/files`, `/api/errors`, `/api/entities`, `/api/min`, `/api/bots`, `/api/bots/ids`, `/api/monoforum`, `/api/suggested-posts`, `/api/stories`, `/api/reactions`, `/api/web-events`, `/api/links`).
  - [x] Crawl official local server (`tdlib/telegram-bot-api`) and client libraries (`grammY`, `Telegraf`, `aiogram`, `python-telegram-bot`, `Telethon`, `Pyrogram`/`Kurigram`, `GramJS`, `TDLib`).
  - [x] Generate `SOURCES.md` and `VERIFICATION_LOG.md`.

- [x] **PHASE 2 — DEEP EXTRACTION**
  - [x] Extract all **186 Bot API 10.4 methods** (`references/bot-api/methods.md`).
  - [x] Extract all **402 Bot API 10.4 object & union types** (`references/bot-api/types.md`).
  - [x] Extract Bot API core, updates, webhooks, limits, and local server (`references/bot-api/core-and-updates.md` & `references/webhooks-and-hosting.md`).
  - [x] Extract Rich Formatting, UTF-16 offsets, HTML vs MarkdownV2, and Bot API 10.2–10.4 `RichMessage` (`references/formatting.md`).
  - [x] Extract Keyboards, Buttons, `style`, `icon_custom_emoji_id`, `copy_text`, `request_managed_bot`, and `EphemeralMessageParameters` (`references/keyboards-and-buttons.md`).
  - [x] Extract Mini Apps (`window.Telegram.WebApp` through 9.5) and `initData` HMAC/Ed25519 validation (`references/mini-apps.md`).
  - [x] Extract Bot API 10.4 In-Chat HTML Widgets (`sendWidget`, `window.TelegramWidget`), Login Widget, and deep links (`references/widgets-and-login.md`).
  - [x] Extract Payments, Telegram Stars (`XTR`), Gifts, Checklists, Suggested Posts, Paid Media, and Business accounts (`references/payments-stars-business.md`).
  - [x] Extract per-version changelog diff from Bot API 6.0 to 10.4 (`references/whats-new.md`).
  - [x] Extract MTProto 2.0 protocol, TL, DH, SRP 2FA, updates, 4 GB files, and Monoforum ID conversions (`references/mtproto/*.md`).
  - [x] Extract Client Library comparison (`references/libraries.md`), Decision Guide (`references/decision-guide.md`), and Common Pitfalls (`references/pitfalls.md`).

- [x] **PHASE 3 — CROSS-VERIFICATION**
  - [x] Cross-verify claims against official docs and schemas (`VERIFICATION_LOG.md`).
  - [x] Execute automated coverage audit (`scripts/coverage_audit.py` -> `COVERAGE.md`).
  - [x] Execute and verify all helper scripts (`escape_markdown_v2.py`, `utf16_entity_offsets.py`, `validate_initdata.py`, `dialog_id_converter.py`).

- [x] **PHASE 4 — BUILD THE SKILL**
  - [x] Author `SKILL.md` (<500 lines router with valid YAML frontmatter), `README.md`, `LICENSE` (MIT), `CHANGELOG.md`.
  - [x] Author runnable examples (`examples/cloudflare-worker-grammy/`, `examples/python-aiogram/`, `examples/python-mtproto/`) and GitHub workflows (`.github/workflows/`).

- [x] **PHASE 5 — SELF-REVIEW & RELEASE PREP**
  - [x] Test 10 realistic agent tasks against the skill and record outcomes in `COVERAGE.md`.
  - [x] Audit for zero leaked secrets/tokens and package `telegram-api-skill.zip`.
