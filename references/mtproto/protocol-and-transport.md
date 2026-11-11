# MTProto Protocol, TL Language, Encryption & Transports

- **Verified Against:** MTProto 2.0 (Layer 225)
- **Verification Date:** November 11, 2026
- **Primary Sources:**
  - [MTProto Mobile Protocol Overview](https://core.telegram.org/mtproto)
  - [Detailed Description of MTProto 2.0](https://core.telegram.org/mtproto/description)
  - [MTProto Transports](https://core.telegram.org/mtproto/mtproto-transports)
  - [Transport Obfuscation](https://core.telegram.org/mtproto/transports)
  - [Binary Data Serialization](https://core.telegram.org/mtproto/serialize)
  - [Creating an Authorization Key (DH Exchange)](https://core.telegram.org/mtproto/auth_key)
  - [Service Messages about Messages](https://core.telegram.org/mtproto/service_messages)
  - [Type Language (TL) Schema](https://core.telegram.org/schema)

---

## 1. Architecture Overview (Three Layers)

MTProto is divided into three independent components ([Source](https://core.telegram.org/mtproto)):
1. **High-Level Component (API Query Language / TL):** Defines how API queries and responses are converted into binary messages using Type Language (`TL`) combinators and constructors ([Source](https://core.telegram.org/schema)).
2. **Cryptographic (Authorization) Layer (MTProto 2.0):** Encrypts binary payloads using a shared 2048-bit `auth_key`, SHA-256 `msg_key`, and AES-256-IGE before transmission ([Source](https://core.telegram.org/mtproto/description)).
3. **Transport Component:** Frames and transmits encrypted MTProto payloads over TCP, WebSocket, HTTP, or HTTPS (with optional AES-256-CTR obfuscation and MTProxy secret-based routing) ([Source](https://core.telegram.org/mtproto/mtproto-transports)).

> **Security Note:** MTProto 1.0 (`msg_key` derived via SHA-1) is **deprecated** and must never be used in new implementations ([Source](https://core.telegram.org/mtproto/description)).

---

## 2. Type Language (TL) & Binary Serialization

Every value in MTProto is serialized in **little-endian** byte order and aligned to **4-byte (32-bit) boundaries** ([Source](https://core.telegram.org/mtproto/serialize)).

### 2.1 Primitive & Built-In Types ([Source](https://core.telegram.org/mtproto/serialize))

| Type | Size / Alignment | Encoding Rule |
|---|---|---|
| `int` (`int32`) | 4 bytes | Signed 32-bit little-endian integer. |
| `long` (`int64`) | 8 bytes | Signed 64-bit little-endian integer. |
| `double` | 8 bytes | 64-bit IEEE 754 floating-point (little-endian). |
| `int128` | 16 bytes | 128-bit little-endian integer (used in DH handshakes). |
| `int256` | 32 bytes | 256-bit little-endian integer (used in DH handshakes). |
| `bytes` / `string` | Variable (padded to 4B) | - **Short (`L <= 253` bytes):** 1 byte length `L`, followed by `L` bytes of data, followed by `0..3` zero padding bytes so total length `(1 + L + pad)` is divisible by 4.<br>- **Long (`L >= 254` bytes):** 1 byte `0xFE` (`254`), followed by 3 bytes of `L` in little-endian (up to `16,777,215` bytes), followed by `L` bytes of data, followed by `0..3` zero padding bytes so `(4 + L + pad)` is divisible by 4. |
| `Bool` | 4 bytes | Boxed polymorphic type: `boolTrue#997275b5` (`0xb5, 0x75, 0x72, 0x99`) or `boolFalse#bc799737` (`0x37, 0x97, 0x79, 0xbc`). |
| `true` (bare flag) | 0 bytes | Used only inside conditional bitmask flags (`flags.N?true`); occupies **0 bytes** in the serialized stream because its presence is encoded in the `flags:#` bitmask. |
| `Vector<T>` (boxed) | `4 + 4 + N * sizeof(T)` | Constructor ID `vector#1cb5c415` (`0x15, 0xc4, 0xb5, 0x1c`), followed by 32-bit count `N`, followed by `N` elements of `T`. |
| `vector<t>` (bare) | `4 + N * sizeof(t)` | Omitted constructor ID; starts directly with 32-bit count `N` followed by `N` elements. |
| `Object` / `!X` | Polymorphic | Any boxed TL value starting with its 32-bit CRC32 constructor number. `!X` denotes a function wrapper (such as `invokeWithLayer#da9b0d0d {X:Type} layer:int query:!X = X`). |

### 2.2 Boxed vs. Bare Types & Conditional Flags (`#`)
- **Boxed Type (Capitalized, e.g., `InputPeer`, `Message`):** Polymorphic union. Serialized with its 32-bit CRC32 **constructor ID** first, followed by its fields in exact schema order ([Source](https://core.telegram.org/mtproto/serialize)).
- **Bare Type (Lowercase `%type` or constructor name):** Monomorphic structure. Serialized **without** the leading 4-byte constructor ID (used in core protocol headers like `message` inside `msg_container#73f1f8dc`) ([Source](https://core.telegram.org/mtproto/service_messages)).
- **Bitmask Conditional Fields (`flags:#`, `flags2:#`):** A 32-bit unsigned integer bitmask. A field declared as `flags.5?string` is serialized in the byte stream **if and only if** `(flags & (1 << 5)) != 0`. If the type is `flags.5?true`, setting bit 5 is sufficient and **zero extra bytes** are written ([Source](https://core.telegram.org/mtproto/serialize)).

---

## 3. MTProto 2.0 Encryption & Envelope Format

### 3.1 Unencrypted Message Format (`auth_key_id == 0`)
Used **only** during initial Diffie-Hellman authorization key creation ([Source](https://core.telegram.org/mtproto/description)):

```text
+--------------------+--------------------+------------------------+--------------------+
| auth_key_id = 0    | message_id         | message_data_length    | message_data       |
| (int64, 8 bytes)   | (int64, 8 bytes)   | (int32, 4 bytes)       | (variable bytes)   |
+--------------------+--------------------+------------------------+--------------------+
```

### 3.2 Encrypted Message Format (`auth_key_id != 0`)
Once the 2048-bit `auth_key` (256 bytes) is established ([Source](https://core.telegram.org/mtproto/description)):

```text
External Header (24 bytes):
+--------------------+--------------------+
| auth_key_id (8B)   | msg_key (16B)      |
+--------------------+--------------------+

AES-256-IGE Encrypted Payload (divisible by 16 bytes):
+--------------------+--------------------+--------------------+--------------------+
| salt (8B)          | session_id (8B)    | message_id (8B)    | seq_no (4B)        |
+--------------------+--------------------+--------------------+--------------------+
| message_data_length (4B)                | message_data (N bytes)                  |
+-----------------------------------------+-----------------------------------------+
| random_padding (12 .. 1024 bytes, so total plaintext is divisible by 16)          |
+-----------------------------------------------------------------------------------+
```

- **`auth_key_id` (8 bytes):** Lower 64 bits (bits 64..127 of the 160-bit SHA-1 hash, i.e., the last 8 bytes) of `SHA1(auth_key)` ([Source](https://core.telegram.org/mtproto/description)).
- **`padding` (12..1024 bytes):** In MTProto 2.0, random padding **must be at least 12 bytes** (and up to 1024 bytes) so total encrypted payload length is divisible by 16 bytes, and its content is included in the `msg_key` hash ([Source](https://core.telegram.org/mtproto/description)).

### 3.3 MTProto 2.0 Key Derivation (`msg_key`, `aes_key`, `aes_iv`)
Let `x = 0` for messages **from client to server** and `x = 8` for messages **from server to client** ([Source](https://core.telegram.org/mtproto/description)):

1. **`msg_key` (16 bytes):**
   ```text
   msg_key_large = SHA256( substr(auth_key, 88 + x, 32) + plaintext_including_padding )
   msg_key       = substr(msg_key_large, 8, 16)
   ```
2. **AES-256-IGE Key (`32 bytes`) and IV (`32 bytes`):**
   ```text
   sha256_a = SHA256( msg_key + substr(auth_key, x, 36) )
   sha256_b = SHA256( substr(auth_key, 40 + x, 36) + msg_key )
   aes_key  = substr(sha256_a, 0, 8) + substr(sha256_b, 8, 16) + substr(sha256_a, 24, 8)
   aes_iv   = substr(sha256_b, 0, 8) + substr(sha256_a, 8, 16) + substr(sha256_b, 24, 8)
   ```
3. **Decryption Verification Checks (Mandatory):**
   After AES-256-IGE decryption, the receiver **must** verify ([Source](https://core.telegram.org/mtproto/description)):
   - Recomputed `msg_key` matches the header's `msg_key` byte-for-byte.
   - `message_data_length` is positive, aligned to 4 bytes, and leaves between `12` and `1024` padding bytes.
   - `session_id` matches the active session.
   - `message_id` is within valid time bounds (at most 300s in the past or 30s in the future relative to server time) and strictly greater than previously seen IDs in the session window.

### 3.4 `message_id`, `seq_no`, and `salt` Rules ([Source](https://core.telegram.org/mtproto/description))
- **`message_id` (64-bit integer):** Approx `unix_timestamp * 2^32`. Must be monotonically increasing within a session. Modulo 4 indicates origin:
  - Client-generated messages: `msg_id % 4 == 0`
  - Server response to a client query: `msg_id % 4 == 1`
  - Server-initiated push notification: `msg_id % 4 == 3`
- **`seq_no` (32-bit integer):**
  - **Content-related messages** (almost all RPC queries requiring an acknowledgment): `seq_no = (content_related_count * 2) + 1` (odd number; increments the counter).
  - **Non-content-related messages** (`msgs_ack`, `msg_container`, `ping`, `http_wait`): `seq_no = content_related_count * 2` (even number; does not increment the counter).
- **`salt` (64-bit integer):** Server-issued value rotated every 30 minutes (`bad_server_salt#edab447b` returns the current valid salt; `get_future_salts#b921bd04` fetches up to 64 upcoming salts in advance) ([Source](https://core.telegram.org/mtproto/service_messages)).

---

## 4. Diffie-Hellman `auth_key` Creation Step-by-Step

Generating a permanent or temporary (`p_q_inner_data_temp_dc`) 2048-bit `auth_key` on a Data Center requires 3 unencrypted round-trips ([Source](https://core.telegram.org/mtproto/auth_key)):

1. **`req_pq_multi#be7e8ef1 nonce:int128 = ResPQ`**
   - Client sends a random 128-bit `nonce`.
   - Server returns `resPQ#05162463 nonce:int128 server_nonce:int128 pq:bytes server_public_key_fingerprints:Vector<long>`.
2. **Proof of Work (Prime Factorization):**
   - Client factors the 64-bit composite number `pq` into two primes `p < q` (typically via Pollard's rho Brent algorithm in `< 5 ms`).
3. **`req_DH_params#d712e4be` with Modern `RSA_PAD` (OAEP+-style):**
   - Client selects a matching 64-bit RSA public key fingerprint from `server_public_key_fingerprints` and constructs `p_q_inner_data_dc#a9f55f95` (or `p_q_inner_data_temp_dc#56fddf88` with `expires_in` for PFS temporary keys), generating a 256-bit `new_nonce`.
   - Client pads and encrypts `p_q_inner_data` into 256-byte `encrypted_data` using the modern **`RSA_PAD`** algorithm (`SHA-256` + AES-256-IGE reversible whitening prior to `x^e mod N`, replacing legacy SHA-1 padding) ([Source](https://core.telegram.org/mtproto/auth_key)).
   - Server responds with `server_DH_params_ok#d0e8075c nonce:int128 server_nonce:int128 encrypted_answer:bytes`.
4. **Decrypt `server_DH_inner_data#b5890dba` & Verify Safe Prime `(g, dh_prime)`:**
   - Derive `tmp_aes_key` and `tmp_aes_iv` from `new_nonce` and `server_nonce` to decrypt `server_DH_inner_data`.
   - **Mandatory Client Security Checks ([Source](https://core.telegram.org/mtproto/auth_key)):**
     - Confirm `dh_prime` (`p`) is a 2048-bit safe prime (`2^2047 < p < 2^2048`) and `(p - 1) / 2` is also prime (or matches Telegram's known DH prime).
     - Confirm generator `g` is `2, 3, 4, 5, 6, or 7` with the required quadratic residue condition (`p mod 8 == 7` for `g=2`; `p mod 3 == 2` for `g=3`; `p mod 5 in {1,4}` for `g=5`, etc.).
     - Confirm `2^{2048-64} <= g_a <= p - 2^{2048-64}` and `2^{2048-64} <= g_b <= p - 2^{2048-64}`.
5. **`set_client_DH_params#f5045f1f` & Final Key Computation:**
   - Client picks random 2048-bit `b`, computes `g_b = g^b mod dh_prime` and `auth_key = (g_a)^b mod dh_prime` (padded with leading zeros to exactly **256 bytes**).
   - Client encrypts `client_DH_inner_data#6643b654` with `tmp_aes_key`/`tmp_aes_iv` and sends `set_client_DH_params`.
   - Server replies with `dh_gen_ok#3bcbf734` where `new_nonce_hash1 == substr(SHA1(new_nonce + [0x01] + substr(SHA1(auth_key), 0, 8)), 4, 16)`.
   - Initial `server_salt = substr(new_nonce, 0, 8) XOR substr(server_nonce, 0, 8)`.

---

## 5. Service Messages, Containers & Acknowledgments

Core MTProto service constructors ([Source](https://core.telegram.org/mtproto/service_messages)):

| Constructor | TL Signature | Purpose & Rules |
|---|---|---|
| `msg_container#73f1f8dc` | `messages:vector<%Message>` | Bundles multiple messages into a single encrypted envelope (up to 1020 messages, `< 1 MB`). Inner messages are bare `%Message` (`msg_id:long seqno:int bytes:int body:Object`) and must have strictly increasing `msg_id` values lower than the container's own `msg_id`. |
| `msgs_ack#62d6b459` | `msg_ids:Vector<long>` | Explicit receipt acknowledgment for content-related messages (up to 8192 IDs per ack). Always uses an **even** `seq_no`. |
| `rpc_result#f35c6d01` | `req_msg_id:long result:Object` | Wraps the response (or `rpc_error#2144ca19` / `gzip_packed#3072cfa1`) to a client RPC request (`req_msg_id`). |
| `rpc_error#2144ca19` | `error_code:int error_message:string` | Standard RPC error returned inside `rpc_result`. |
| `gzip_packed#3072cfa1` | `packed_data:bytes` | Standard gzip-compressed TL object. Used whenever compressed size is smaller by at least 64 bytes. |
| `bad_msg_notification#a7eff811` | `bad_msg_id:long bad_msg_seqno:int error_code:int` | Low-level framing/time/seqno error (`16`/`17`: `msg_id` too low/high -> sync clock; `32`/`33`: `seq_no` too low/high -> reset session; `48`: incorrect server salt). |
| `bad_server_salt#edab447b` | `bad_msg_id:long bad_msg_seqno:int error_code:int new_server_salt:long` | Server rejected the salt (`error_code = 48`). Client must save `new_server_salt` and immediately re-encrypt and resend `bad_msg_id`. |
| `new_session_created#9ec20908` | `first_msg_id:long unique_id:long server_salt:long` | Emitted by server on the first message of a new `session_id`; client should update `server_salt` and acknowledge this message. |
| `ping_delay_disconnect#f3427b8c` | `ping_id:long disconnect_delay:int` | Keepalive ping; if server receives no another ping within `disconnect_delay` seconds, it closes the TCP connection and switches to push notifications. |

---

## 6. MTProto Transports & Obfuscation

Before sending the first MTProto packet over a raw TCP or WebSocket connection, the client sends a protocol header (except for Full TCP) ([Source](https://core.telegram.org/mtproto/mtproto-transports)):

| Transport | Connection Header | Per-Packet Framing | Quick Ack Support | Notes |
|---|---|---|---|---|
| **Abridged** | `0xEF` (1 byte) | 1 byte `L = len / 4` (if `L < 127`) or `0x7F` + 3-byte little-endian `len / 4`. Payload only. | Set bit 7 of length (`L \| 0x80`); server replies with 4-byte reversed quick ack. | Lowest overhead (1–4 bytes per packet). |
| **Intermediate** | `0xEEEEEEEE` (4 bytes) | 4-byte little-endian `len` (in bytes), followed by payload. | Set MSB of length (`len \| 0x80000000`). | Simplest alignment; widely used by bots/userbots. |
| **Padded Intermediate** | `0xDDDDDDDD` (4 bytes) | 4-byte little-endian `len + pad_len`, followed by payload + `0..15` random padding bytes. | Set MSB of length (`len \| 0x80000000`). | Defeats packet-length fingerprinting; mandatory for fake-TLS MTProxy. |
| **Full** | None (starts at `seq=0`) | `len (4B)` + `seq_no (4B)` + `payload` + `crc32 (4B)` (`len` includes all 12 framing bytes). | Not supported. | Includes transport-level sequence number and CRC32 check. |

### 6.1 Transport Obfuscation (AES-256-CTR) & MTProxy
To bypass deep packet inspection (DPI) on TCP or WebSocket connections, clients prepend a **64-byte random initialization header** `init[0..63]` ([Source](https://core.telegram.org/mtproto/transports)):
1. Generate 64 random bytes `init` ensuring `init[0] != 0xEF` and `init[0..3]` is none of `0x44414548` (`HEAD`), `0x54534F50` (`POST`), `0x20544547` (`GET `), `0x4954504F` (`OPTI`), `0xEEEEEEEE`, `0xDDDDDDDD`, `0x02010316` (TLS), and `init[4..7] != 0x00000000`.
2. Write the chosen transport tag (`0xEFEFEFEF`, `0xEEEEEEEE`, or `0xDDDDDDDD`) into `init[56..59]` and the target signed 16-bit DC ID (e.g., `2` for DC2, `-2` for DC2 media, `10002` for test DC2) into `init[60..61]`.
3. Extract `encrypt_key = init[8..39]` (32 bytes) and `encrypt_iv = init[40..55]` (16 bytes).
4. Reverse the 48-byte slice `init[8..55]` to form `rev[0..47]`, and extract `decrypt_key = rev[0..31]` and `decrypt_iv = rev[32..47]`.
5. **(Optional MTProxy Secret):** If using an MTProxy with a 16-byte secret `S`:
   - `encrypt_key = SHA256(encrypt_key + S)`
   - `decrypt_key = SHA256(decrypt_key + S)`
   - If the secret starts with `dd` (`17 bytes`), force **Padded Intermediate** (`0xDDDDDDDD`). If the secret starts with `ee` (`17 + domain` bytes), wrap the connection in a Fake-TLS 1.3 ClientHello handshake using the embedded SNI domain.
6. Run `encrypt_cipher = AES_256_CTR(encrypt_key, encrypt_iv)` over all 64 bytes of `init` (`encrypted_init`), then overwrite bytes `56..63` of the transmitted header with `encrypted_init[56..63]`. All subsequent outgoing transport frames are encrypted with the continuing `encrypt_cipher` stream, and incoming frames are decrypted with `decrypt_cipher`.
