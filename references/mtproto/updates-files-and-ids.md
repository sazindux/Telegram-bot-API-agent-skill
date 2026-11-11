# MTProto Updates (`pts`/`qts`/`seq`), File Transfers, Errors & Peer/Dialog IDs

- **Verified Against:** MTProto 2.0 (Layer 225) & Bot API 10.4
- **Verification Date:** November 11, 2026
- **Primary Sources:**
  - [Working with Updates (`pts`, `qts`, `seq`)](https://core.telegram.org/api/updates)
  - [Uploading and Downloading Files](https://core.telegram.org/api/files)
  - [RPC Error Handling](https://core.telegram.org/api/errors)
  - [Peer Entities & Access Hashes](https://core.telegram.org/api/entities)
  - [Min Constructors (`inputPeer*FromMessage`)](https://core.telegram.org/api/min)
  - [Bot API Dialog IDs & Peer ID Conversion](https://core.telegram.org/api/bots/ids)
  - [Monoforums (Direct Messages for Channels)](https://core.telegram.org/api/monoforum)

---

## 1. Updates State Machine (`pts`, `qts`, `seq`, `date`)

MTProto delivers real-time events via boxed `Updates` containers (`updatesTooLong`, `updateShortMessage`, `updateShortChatMessage`, `updateShort`, `updatesCombined`, `updates`) ([Source](https://core.telegram.org/api/updates)).

### 1.1 State Counters ([Source](https://core.telegram.org/api/updates))

| Counter | Scope | Description & Gap Detection Rule |
|---|---|---|
| **`pts`** + `pts_count` | Common box (private chats, basic groups, account settings) **OR** per-channel/supergroup (`channel_id`) | Every `pts`-bearing update carries `pts` and `pts_count`:<br>- If `local_pts + pts_count == pts`: apply the update and set `local_pts = pts`.<br>- If `local_pts + pts_count > pts`: the update was already applied; ignore it.<br>- If `local_pts + pts_count < pts`: **a gap occurred**; wait up to `0.5s` for out-of-order packets, then fetch missing state via `updates.getDifference` (or `updates.getChannelDifference` for channels/supergroups). |
| **`qts`** + `qts_count` (`1`) | Secret chats & bot webhook/callback events (`updateBotWebhookJSON`, `updateBotPrecheckoutQuery`) | Sequential counter independent of `pts`. Apply if `local_qts + 1 == qts`; fetch gap via `updates.getDifference`. |
| **`seq`** + `seq_start` | `updatesCombined` / `updates` containers (`seq != 0`) | Container-level ordering counter:<br>- If `seq == 0`: apply inner updates immediately (relying on inner `pts`/`qts`).<br>- If `local_seq + 1 == seq_start`: apply and set `local_seq = seq`.<br>- If `local_seq + 1 < seq_start`: gap detected -> call `updates.getDifference`. |
| **`date`** | Global fallback timestamp | Updated whenever `seq > 0` or returned by `updates.getState` / `updates.getDifference`. |

### 1.2 Catching Up on Missed Updates (`getDifference` & `getChannelDifference`) ([Source](https://core.telegram.org/api/updates))
1. **Initialization:** On first login, call `updates.getState#edd4882a()` and persist `(pts, qts, date, seq)` locally.
2. **Recovering Common Gaps (`updates.getDifference#19c2f763`):**
   - Pass stored `(pts, date, qts)`.
   - Responses:
     - `updates.differenceEmpty#5d75a138`: No new updates; update `date` and `seq`.
     - `updates.difference#f49ca0`: Apply `new_messages`, `new_encrypted_messages`, and `other_updates`, then update local state to `state`.
     - `updates.differenceSlice#a8fb1981`: Apply slice items, update local state to `intermediate_state`, and **immediately call `updates.getDifference` again** with `intermediate_state`.
     - `updates.differenceTooLong#4afe8f6d(pts)`: Gap exceeds server retention (`> 1,000,000` events); update `local_pts = pts` and reload dialog list via `messages.getDialogs`.
3. **Recovering Channel/Supergroup Gaps (`updates.getChannelDifference#3173d78`):**
   - Each channel/supergroup maintains its own independent `pts` counter!
   - When `updateChannelTooLong#108d941f` arrives or a channel `pts` gap is detected, call `updates.getChannelDifference(channel, filter, pts, limit)` (bots can pass `limit` up to `100000`, users up to `100`).

---

## 2. Entities, `access_hash`, and `min` Constructors

### 2.1 `access_hash` Caching ([Source](https://core.telegram.org/api/entities))
Most MTProto methods require an `InputPeer`, `InputUser`, or `InputChannel` pairing a numeric ID with a 64-bit **`access_hash`** scoped to the calling account (`inputPeerUser(user_id, access_hash)`, `inputPeerChannel(channel_id, access_hash)`).
- Always extract and cache `(id, access_hash)` pairs from the `users` and `chats` arrays bundled at the bottom of `Updates`, `messages.Messages`, and `contacts.ResolvedPeer` responses.
- Basic groups (`inputPeerChat(chat_id)`) do not use an `access_hash`.

### 2.2 `min` Constructors (`user.min` / `channel.min`) ([Source](https://core.telegram.org/api/min))
When a user or channel object is returned inside a forward header or reply where the caller hasn't directly interacted with that peer, the `min` flag bit is set.
- **Crucial Rule:** The `access_hash` inside a `min` constructor is **not valid** for direct global calls like `messages.sendMessage`.
- To interact with a `min` user or channel without a full `access_hash`, pass a message-scoped reference constructor ([Source](https://core.telegram.org/api/min)):
  - `inputPeerUserFromMessage#a87b0a1c(peer:InputPeer, msg_id:int, user_id:long)`
  - `inputPeerChannelFromMessage#bd2a0840(peer:InputPeer, msg_id:int, channel_id:long)`
  - `inputUserFromMessage#1da448e2(peer:InputPeer, msg_id:int, user_id:long)`
  - `inputChannelFromMessage#5b934f9d(peer:InputPeer, msg_id:int, channel_id:long)`

---

## 3. Exact Peer ID <-> Bot API Dialog ID Conversion (Layer 225 / Bot API 10.4)

MTProto uses raw positive 64-bit integer IDs Inside typed `Peer` constructors (`peerUser`, `peerChat`, `peerChannel`), whereas the Bot API encodes the peer type into a single signed 64-bit integer (`chat_id`) ([Source](https://core.telegram.org/api/bots/ids)):

| Entity Type | MTProto Constructor & Raw ID Range (`id`) | Bot API Dialog ID (`chat_id`) Range | Conversion Formula (MTProto `id` -> Bot API `chat_id`) |
|---|---|---|---|
| **User / Bot** | `peerUser(user_id)`<br>`1 <= id <= 1099511627775` (`2^40 - 1`) | `1` to `1099511627775` | `chat_id = user_id` |
| **Basic Group (`chat`)** | `peerChat(chat_id)`<br>`1 <= id <= 999999999999` | `-999999999999` to `-1` | `chat_id = -id` |
| **Channel / Supergroup (`channel`)** | `peerChannel(channel_id)`<br>`1 <= id <= 997852516352` | `-1997852516352` to `-1000000000001` | `chat_id = -1000000000000 - channel_id` |
| **Secret Chat** *(TDLib only)* | `secret_chat_id`<br>`-2147483648 <= id <= 2147483647` | `-2002147483648` to `-1997852516353` | `chat_id = -2000000000000 + secret_chat_id` |
| **Monoforum (Channel Direct Messages)** | `peerChannel(channel_id)` with `channel.monoforum == true`<br>`1002147483649 <= id <= 3000000000000` | `-4000000000000` to `-2002147483649` | `chat_id = -1000000000000 - channel_id` |

> **Critical Layer 225 / Monoforum Rule ([Source](https://core.telegram.org/api/bots/ids), [Source](https://core.telegram.org/api/monoforum)):**
> Full valid Bot API dialog ID range is **`-4000000000000` to `1099511627775`**. Never use string prefix checks like `str(chat_id).startswith("-100")` to detect channels/supergroups—Monoforum channels have Bot API IDs starting with `-200...` through `-4000000000000`! Always use numeric range comparisons (see `scripts/dialog_id_converter.py`).

---

## 4. File Upload & Download (`upload.*`) & `FILE_REFERENCE_EXPIRED`

### 4.1 Uploading Files (`saveFilePart` vs. `saveBigFilePart`) ([Source](https://core.telegram.org/api/files))
- Generate a random 64-bit `file_id` on the client.
- **Chunk (`part`) size rules:**
  - `part_size` **must** divide `524,288` bytes (`512 KB`) evenly and be divisible by `1,024` bytes (`1 KB`): valid values are `1, 2, 4, 8, 16, 32, 64, 128, 256, 512 KB` (use `512 KB` for maximum speed; only the very last chunk may be smaller).
  - Maximum parts per file: **`8,000` parts** (yielding a **`4,000 MB` (`4 GB`)** maximum file size when using `512 KB` chunks; non-Premium users are capped at `4,000` parts / `2 GB`).
- **Small files (`<= 10 MB`):**
  - Upload each chunk via `upload.saveFilePart#b304a621(file_id, file_part, bytes)`.
  - Construct `inputFile#f52ff27f(id=file_id, parts=total_parts, name=filename, md5_checksum="")`.
- **Big files (`> 10 MB` up to `4 GB`):**
  - Upload each chunk (can be parallelized across multiple worker connections) via `upload.saveBigFilePart#de7b673d(file_id, file_part, file_total_parts, bytes)`.
  - Construct `inputFileBig#fa4f0bb5(id=file_id, parts=total_parts, name=filename)`.

### 4.2 Downloading Files (`upload.getFile`) & Refreshing `file_reference` ([Source](https://core.telegram.org/api/files))
- Call `upload.getFile#be5335be(flags, precise:flags.0?true, cdn_supported:flags.1?true, location:InputFileLocation, offset:long, limit:int)`:
  - When `precise` is **not** set: `limit` must be a power of 2 between `4,096` (`4 KB`) and `1,048,576` (`1 MB`), and `offset` must be divisible by `limit`.
  - When `precise` **is** set: `limit` must be `<= 1 MB` and divisible by `1 KB`, and `offset` must be divisible by `1 KB`.
- **Handling `400 FILE_REFERENCE_EXPIRED` / `FILE_REFERENCE_*` ([Source](https://core.telegram.org/api/files)):**
  Every `InputFileLocation` (such as `inputDocumentFileLocation`, `inputPhotoFileLocation`) embeds a short-lived cryptographic **`file_reference:bytes`** bound to the source context (the message, story, user profile, or sticker set from which the media was obtained).
  - If `upload.getFile` or `messages.sendMedia` returns `400 FILE_REFERENCE_EXPIRED` (or `FILE_REFERENCE_INVALID`), you **must** re-fetch the original container object (e.g., call `messages.getMessages` or `channels.getMessages` with the original `(peer, msg_id)`), extract the fresh `file_reference` from the returned `photo`/`document`, and retry the call.

---

## 5. RPC Error Codes & Recovery Actions ([Source](https://core.telegram.org/api/errors))

| HTTP-like Code | Error String Pattern | Meaning & Mandatory Client Action |
|---|---|---|
| `303` | `PHONE_MIGRATE_X`, `NETWORK_MIGRATE_X`, `USER_MIGRATE_X` | Account belongs to DC `X`. Switch primary connection to DC `X`. |
| `303` | `FILE_MIGRATE_X`, `STATS_MIGRATE_X` | Resource resides on DC `X`. Export/import authorization to a worker connection on DC `X`. |
| `400` | `FILE_REFERENCE_EXPIRED`, `FILE_REFERENCE_INVALID` | Refetch the source message/container to obtain a fresh `file_reference:bytes` and retry. |
| `400` | `PEER_ID_INVALID`, `CHANNEL_INVALID` | Missing or invalid `access_hash`, or raw ID was not converted/resolved first. Resolve username or fetch dialog list. |
| `401` | `AUTH_KEY_UNREGISTERED`, `SESSION_REVOKED`, `USER_DEACTIVATED_BAN` | Session is dead or account is banned. Stop retrying immediately; require re-authentication. |
| `401` | `SESSION_PASSWORD_NEEDED` | Account has 2FA enabled; complete SRP 6a flow (`account.getPassword` -> `auth.checkPassword`). |
| `403` | `CHAT_WRITE_FORBIDDEN`, `USER_IS_BLOCKED`, `USER_PRIVACY_RESTRICTED` | Permission denied by chat admin or user privacy settings. Do not retry. |
| `406` | `AUTH_KEY_DUPLICATED` | Same `auth_key` used concurrently from multiple IPs. Key is permanently invalidated. |
| `420` | `FLOOD_WAIT_X`, `FLOOD_PREMIUM_WAIT_X`, `SLOWMODE_WAIT_X` | Rate limit hit. Sleep for **at least `X` seconds** before retrying. |
| `500` | `RPC_CALL_FAIL`, `RPC_MCGET_FAIL`, `INTERDC_X_CALL_ERROR` | Transient Telegram internal server error. Retry with exponential backoff (`1s, 2s, 4s...`). |
