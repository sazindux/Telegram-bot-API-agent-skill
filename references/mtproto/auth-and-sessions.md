# MTProto Authorization, 2FA (SRP 6a), Sessions & Data Centers

- **Verified Against:** MTProto 2.0 (Layer 225)
- **Verification Date:** November 11, 2026
- **Primary Sources:**
  - [Obtaining `api_id` and `api_hash`](https://core.telegram.org/api/obtaining_api_id)
  - [User Authorization (`auth.*`)](https://core.telegram.org/api/auth)
  - [Two-Factor Authentication (SRP 6a)](https://core.telegram.org/api/srp)
  - [QR Code Login](https://core.telegram.org/api/qr-login)
  - [Data Centers & DC Migration](https://core.telegram.org/api/datacenter)
  - [API Layers & `invokeWithLayer`](https://core.telegram.org/api/layers)

---

## 1. Obtaining `api_id` & `api_hash`

Every MTProto client (userbot, custom client, or bot running over MTProto/TDLib/local `telegram-bot-api`) requires an `api_id` (32-bit integer) and `api_hash` (32-char hex string) issued at `https://my.telegram.org` under **API development tools** ([Source](https://core.telegram.org/api/obtaining_api_id)).
- Never hard-code `api_id` or `api_hash` in public source code; pass them via environment variables (`TELEGRAM_API_ID`, `TELEGRAM_API_HASH`).
- All clients must observe the [Telegram API Terms of Service](https://core.telegram.org/api/terms).

---

## 2. Layer Negotiation (`invokeWithLayer` + `initConnection`)

Immediately after creating an `auth_key` on any Data Center connection, the very first high-level RPC call **must** wrap the inner query inside `invokeWithLayer#da9b0d0d` and `initConnection#c1cd5ea9` so the server knows which TL schema layer to use for serialized updates and responses ([Source](https://core.telegram.org/api/layers)):

```tl
invokeWithLayer#da9b0d0d {X:Type} layer:int query:!X = X;
initConnection#c1cd5ea9 {X:Type} flags:# api_id:int device_model:string system_version:string app_version:string system_lang_code:string lang_pack:string lang_code:string proxy:flags.0?InputClientProxy params:flags.1?JSONValue query:!X = X;
```

- **Current Latest Layer:** **`225`** ([Source](https://core.telegram.org/api/layers)).
- Standard startup call:
  ```text
  invokeWithLayer(
    layer = 225,
    query = initConnection(
      api_id = YOUR_API_ID,
      device_model = "Server",
      system_version = "Linux",
      app_version = "1.0.0",
      system_lang_code = "en",
      lang_pack = "",
      lang_code = "en",
      query = help.getConfig()
    )
  )
  ```
- Once `invokeWithLayer(225, initConnection(..., help.getConfig()))` succeeds on a session (`session_id`), subsequent RPC calls on that **same `session_id`** do not need the wrapper again unless the `session_id` changes ([Source](https://core.telegram.org/api/layers)).

---

## 3. Data Centers (DC 1–5) & DC Migration

### 3.1 Production vs. Test Data Center IP Addresses ([Source](https://core.telegram.org/api/datacenter))

| DC ID | Region | Production IPv4 (Port 443 / 80 / 5222) | Test DC IPv4 |
|---|---|---|---|
| **DC 1** | Miami, US | `149.154.175.53` | `149.154.175.10` |
| **DC 2** | Amsterdam, NL | `149.154.167.50` | `149.154.167.40` |
| **DC 3** | Miami, US | `149.154.175.100` | `149.154.175.117` |
| **DC 4** | Amsterdam, NL | `149.154.167.91` | `149.154.167.40` (shares test host with DC2; fetch updated list via `help.getConfig`) |
| **DC 5** | Singapore, SG | `91.108.56.130` | — |

Always refresh the dynamic DC table (`dcOption` list, including IPv6, media-only, and CDN endpoints) via `help.getConfig#c4f9186b` after connecting ([Source](https://core.telegram.org/api/datacenter)).

### 3.2 Handling `*_MIGRATE_X` (`303 See Other`) & Cross-DC Auth Transfer
Each user/bot account has a single **Home DC** where its session state lives, while files (`FILE_MIGRATE_X`) or stats (`STATS_MIGRATE_X`) may reside on other DCs ([Source](https://core.telegram.org/api/datacenter)):
- **During Login (`PHONE_MIGRATE_X`, `USER_MIGRATE_X`, `NETWORK_MIGRATE_X`):**
  Close or switch the primary session to DC `X`, perform DH `auth_key` creation on DC `X`, and re-run `auth.sendCode` / `auth.importBotAuthorization` on DC `X`.
- **When Already Logged In (`FILE_MIGRATE_X`, `STATS_MIGRATE_X`):**
  Keep the primary session on the Home DC and copy authorization to DC `X`:
  1. On Home DC, call `auth.exportAuthorization#e5bfffcd(dc_id = X)` -> returns `auth.exportedAuthorization#df969c2d(id, bytes)`.
  2. Connect to DC `X` (create an `auth_key` on DC `X` if not cached).
  3. On DC `X`, call `invokeWithLayer(225, initConnection(..., auth.importAuthorization#a57a7dad(id = id, bytes = bytes)))`.

---

## 4. User & Bot Authorization Flows

### 4.1 Bot Login Flow (`auth.importBotAuthorization`) ([Source](https://core.telegram.org/api/auth))
Bots authenticate in a single call without SMS/phone codes:
```tl
auth.importBotAuthorization#67a3ff2c flags:int api_id:int api_hash:string bot_auth_token:string = auth.Authorization;
```
- If the bot's account lives on another DC, the server returns `303 USER_MIGRATE_X`; reconnect to DC `X` and call `auth.importBotAuthorization` again.

### 4.2 User Phone Login Flow (`auth.sendCode` -> `auth.signIn`) ([Source](https://core.telegram.org/api/auth))
1. **Request Verification Code:**
   Call `auth.sendCode#a677244f(phone_number, api_id, api_hash, settings: codeSettings#ad253d78)`.
   - Pass previously saved `future_auth_tokens` (up to 20 tokens stored from prior `auth.authorization#2ea2c0d4.future_auth_token` responses) inside `codeSettings.logout_tokens` to skip 2FA/SMS when re-authenticating on known devices ([Source](https://core.telegram.org/api/auth)).
   - Returns `auth.sentCode#5e002502(type, phone_code_hash, next_type, timeout)` (or `auth.sentCodeSuccess#2390fe44` if a future auth token matched).
2. **Submit Code:**
   Call `auth.signIn#8d52a951(phone_number, phone_code_hash, phone_code)`.
   - If the phone number is unregistered, returns `auth.authorizationSignUpRequired#44747e9a` (note: third-party unofficial apps can no longer call `auth.signUp`; sign-up must happen on official mobile clients, returning `PHONE_NUMBER_APP_SIGNUP_FORBIDDEN`) ([Source](https://core.telegram.org/api/auth)).
   - If Two-Factor Authentication (2FA) is enabled on the account, returns `401 SESSION_PASSWORD_NEEDED`. Proceed to the **SRP 6a 2FA flow** below.

### 4.3 Two-Factor Authentication (2FA) via SRP 6a ([Source](https://core.telegram.org/api/srp))
Telegram uses **SRP 6a** with PBKDF2-HMAC-SHA512 so the plaintext password is never transmitted over the network.
1. Call `account.getPassword#548a30f5()` -> returns `account.password#957b50fb` containing `srp_id:long`, `srp_B:bytes`, and `current_algo:PasswordKdfAlgo`.
2. Verify that `current_algo` is `passwordKdfAlgoSHA256SHA256PBKDF2HMACSHA512iter100000SHA256ModPow#3a912d4a(salt1, salt2, g, p)`.
3. **Verify Safe Prime `p` and Server Parameter `B`:**
   - Ensure `p` is the standard 2048-bit prime and `0 < B < p`.
   - Pad `p` and `g` (big-endian) to 256 bytes (`g_bytes`, `p_bytes`).
4. **Compute Password Hash & SRP Proof `(A, M1)` ([Source](https://core.telegram.org/api/srp)):**
   ```python
   import hashlib, os

   def H(data: bytes) -> bytes:
       return hashlib.sha256(data).digest()

   def SH(data: bytes, salt: bytes) -> bytes:
       return H(salt + data + salt)

   def PH1(password: bytes, salt1: bytes, salt2: bytes) -> bytes:
       return SH(SH(password, salt1), salt2)

   def PH2(password: bytes, salt1: bytes, salt2: bytes) -> bytes:
       return SH(hashlib.pbkdf2_hmac('sha512', PH1(password, salt1, salt2), salt1, 100000), salt2)

   # 1. Derive private exponent x and verifier v = g^x mod p
   x = int.from_bytes(PH2(password_utf8, salt1, salt2), 'big')
   p_int = int.from_bytes(p, 'big')
   g_bytes = g.to_bytes(256, 'big')
   v = pow(g, x, p_int)

   # 2. Compute multiplier k = H(p || g_bytes)
   k = int.from_bytes(H(p + g_bytes), 'big')

   # 3. Generate random 2048-bit client ephemeral secret a -> A = g^a mod p
   a = int.from_bytes(os.urandom(256), 'big')
   A_int = pow(g, a, p_int)
   A_bytes = A_int.to_bytes(256, 'big')

   # 4. Scrambling parameter u = H(A_bytes || B_bytes)
   B_int = int.from_bytes(srp_B, 'big')
   B_bytes = B_int.to_bytes(256, 'big')
   u = int.from_bytes(H(A_bytes + B_bytes), 'big')

   # 5. Shared secret S = (B - k * v)^(a + u * x) mod p, key K = H(S)
   g_b = (B_int - k * v) % p_int
   S_int = pow(g_b, a + u * x, p_int)
   K_bytes = H(S_int.to_bytes(256, 'big'))

   # 6. Client proof M1 = H( (H(p) XOR H(g_bytes)) || H(salt1) || H(salt2) || A_bytes || B_bytes || K_bytes )
   hp_xor_hg = bytes(b1 ^ b2 for b1, b2 in zip(H(p), H(g_bytes)))
   M1 = H(hp_xor_hg + H(salt1) + H(salt2) + A_bytes + B_bytes + K_bytes)
   ```
5. Call `auth.checkPassword#d18b4d16(password = inputCheckPasswordSRP#d27ff082(srp_id = srp_id, A = A_bytes, M1 = M1))` -> returns `auth.authorization#2ea2c0d4`.

### 4.4 QR Code Login (`auth.exportLoginToken`) ([Source](https://core.telegram.org/api/qr-login))
1. Unauthenticated client calls `auth.exportLoginToken#b7e085fe(api_id, api_hash, except_ids=[])`.
2. Server returns `auth.loginToken#629f1980(expires, token)`. Encode as `tg://login?token=<base64url_no_padding(token)>` and render QR code.
3. Logged-in mobile client scans QR and calls `auth.acceptLoginToken#e894ad4d(token)`.
4. Unauthenticated client receives `updateLoginToken#eb49081d`, calls `auth.exportLoginToken` again:
   - If it returns `auth.loginTokenMigrateTo#68e9916(dc_id, token)`, connect to `dc_id` and call `auth.importLoginToken#95ac5ce4(token)`.
   - Returns `auth.loginTokenSuccess#390d5c5e(authorization)` (or `401 SESSION_PASSWORD_NEEDED` if 2FA is active).

---

## 5. Session Safety, Parallel Connections & `AUTH_KEY_DUPLICATED`

- **`AUTH_KEY_DUPLICATED` (Error `406`):**
  If two separate processes or servers use the **same `auth_key`** from different IP addresses concurrently, Telegram immediately revokes the `auth_key` with `406 AUTH_KEY_DUPLICATED` (for userbots, repeated violations can terminate all active sessions or trigger account freezes) ([Source](https://core.telegram.org/api/errors)).
  - **Rule:** Never share a single `.session` file or string session across multiple servers/containers. Generate a separate session per worker/process.
- **Parallel Connections Within One Process (`tmp_sessions`):**
  To use multiple concurrent TCP connections for high-throughput file transfers or bot webhook handling on the same host, use dedicated `session_id` values or PFS temporary keys (`p_q_inner_data_temp_dc` + `auth.bindTempAuthKey#cdd42a05`) and configure `tmp_sessions` in BotFather when running multiple local `telegram-bot-api` instances ([Source](https://core.telegram.org/mtproto/auth_key)).
