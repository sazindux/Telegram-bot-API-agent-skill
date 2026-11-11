# Changelog (`CHANGELOG.md`)

All notable changes to the `telegram-api-skill` repository are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this skill tracks the official [Telegram Bot API Changelog](https://core.telegram.org/bots/api-changelog) and [MTProto Layer Changelog](https://core.telegram.org/api/layers).

## [1.2.0] - 2026-11-11

### Added
- **Condensed edition (`SKILL-custom.md`):** ~200-line, 100% code-free system custom skill for platforms that reject executable code (e.g. Gemini Chat Custom Skills) or enforce small skill budgets. Contains hard invariants, the architecture decision matrix, rate/file limits, webhook requirements, MarkdownV2/initData/dialog-ID quick formulas, widget/payment/MTProto quick rules, breaking changes (9.6–10.4), the complete grouped 186-method and 402-type name catalogs (coverage-verified), and the top 12 production pitfalls.
- **README:** "Which Edition Should I Use?" comparison table and "Condensed Edition" section with installation instructions.

## [1.1.0] - 2026-11-11

### Added
- **Single-file edition (`SKILL-single-file.md`):** the complete skill — all 17 reference parts, the full 186-method / 402-type catalogs, all five helper-script sources, and all runnable examples — consolidated into one drop-in document for any AI agent, with a Source File ↔ Location Map, Table of Contents, and agent-facing usage instructions in the header.
- **README:** "Single-File Edition" section documenting when/how to use the single file and context-window guidance.

## [1.0.0] - 2026-11-11

### Added
- **Full Bot API 10.4 Coverage (Released November 9, 2026):**
  - 100% coverage of all **186 methods** (`references/bot-api/methods.md`) and **402 object & union types** (`references/bot-api/types.md`) verified against [core.telegram.org/bots/api](https://core.telegram.org/bots/api).
  - Complete guide for **In-Chat HTML Widgets** (`sendWidget`, `sendSharedWidget`, `answerWidgetQuery`, `editMessageWidgetData`, `editSharedWidgetData`, `window.TelegramWidget`, QuickJS sandbox, and TON wallet integration) from [core.telegram.org/bots/widgets](https://core.telegram.org/bots/widgets).
  - Deep dive into **Rich Messages** (`sendRichMessage`, `sendRichMessageDraft`, 31 `RichText` classes, 25 `RichBlock` / `InputRichBlock` classes, 32,768-character limit, `<tg-thinking>`, and `tg://document?id=`).
  - Complete **Ephemeral Messages** workflow (`EphemeralMessageParameters`, optional `receiver_user_id`/`chat_id` for callback replies in 10.4, `replace_callback_query_message`, `editEphemeralMessage*`, `deleteEphemeralMessage`).
  - **Telegram Serverless (`tgcloud` CLI v0.2.0, Oct 6, 2026)** reference (`sdk/db`, `sdk/api`, `handlers/`, `endpoints/`, `Telegram.WebApp.Serverless.call`) from [core.telegram.org/bots/serverless](https://core.telegram.org/bots/serverless).
  - **Mini Apps (`window.Telegram.WebApp`)** reference covering Bot API 6.0 through 10.4 (`requestChat`, `DeviceStorage`, `SecureStorage`, `hideKeyboard`, `iconCustomEmojiId`, Fullscreen, Safe Areas, Biometrics, Motion Sensors, `LocationManager`, and July 20, 2026 Origin Hardening).
  - **Payments, Stars (`XTR`), Gifts & Business:** Digital/physical invoices, Star subscriptions, paid media (up to 25,000 Stars), paid broadcasts (0.1 Stars/msg up to 1,000 msg/s), regular & unique collectible gifts, TON wallet cards/transfers, Business Bots (no Premium required since 10.0), Managed Bots, Guest Mode (`answerGuestQuery`), Channel Direct Messages (Monoforums), Suggested Posts, and Checklists.
- **Full MTProto Layer 225 Coverage:**
  - MTProto 2.0 specification (AES-256-IGE key derivation, DH `auth_key` exchange, `RSA_PAD` OAEP+, TL serialization, Abridged/Intermediate/Padded/Full transports, and AES-256-CTR transport obfuscation).
  - Authorization flows (`auth.sendCode`, `future_auth_tokens`, SRP 6a 2FA with 100,000-iteration PBKDF2-SHA512, QR login, Passkeys, OAuth) and parallel session rules (`tmp_sessions`, `AUTH_KEY_DUPLICATED`).
  - Update state synchronization (`pts`, `qts`, `seq`, `updates.getDifference`, `updates.getChannelDifference`, `updateMessageID`), chunked file transfers (`upload.saveFilePart`/`saveBigFilePart`/`getFile`, `FILE_REFERENCE_EXPIRED` refresh), and bi-directional Peer ID <-> Bot API Dialog ID conversion (including the Layer 214/225 Monoforum range `-4000000000000` to `-2002147483649`).
- **Deterministic Helper Scripts (`scripts/`):**
  - `validate_initdata.py`, `escape_markdown_v2.py`, `utf16_entity_offsets.py`, `dialog_id_converter.py`, and `coverage_audit.py`.
- **Runnable Examples (`examples/`) & CI Workflows (`.github/workflows/`):**
  - Cloudflare Workers + `grammY`, Python `aiogram` v3, Python `Telethon` & `Pyrogram`/`Kurigram`, plus GitHub Actions for markdown/link checking and daily Bot API changelog monitoring.
