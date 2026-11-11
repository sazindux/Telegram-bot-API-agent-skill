#!/usr/bin/env python3
"""
Telethon MTProto example demonstrating:
1. User login with 2FA (SRP 6a handled by Telethon `SessionPasswordNeededError`)
2. Catching `FloodWaitError` and sleeping for `e.seconds`
3. Refreshing expired `file_reference` on `FileReferenceExpiredError`

Env vars required at runtime:
- TELEGRAM_API_ID
- TELEGRAM_API_HASH
"""

import asyncio
import os
from telethon import TelegramClient
from telethon.errors import (
    FileReferenceExpiredError,
    FloodWaitError,
    SessionPasswordNeededError,
)


async def login_and_run() -> None:
    api_id = int(os.environ["TELEGRAM_API_ID"])
    api_hash = os.environ["TELEGRAM_API_HASH"]
    phone = os.environ["TELEGRAM_PHONE"]

    # Always use a dedicated session per host/IP to avoid 406 AUTH_KEY_DUPLICATED
    client = TelegramClient("production_worker_1", api_id, api_hash)
    await client.connect()

    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        code = input("Enter the login code: ").strip()
        try:
            await client.sign_in(phone=phone, code=code)
        except SessionPasswordNeededError:
            password = os.environ.get("TELEGRAM_2FA_PASSWORD") or input("Enter 2FA password: ")
            await client.sign_in(password=password)

    # Example: download media with automatic FILE_REFERENCE_EXPIRED recovery
    async def download_from_message(chat_id: int, msg_id: int, target_path: str) -> str:
        msg = await client.get_messages(chat_id, ids=msg_id)
        try:
            return await client.download_media(msg, file=target_path)
        except FileReferenceExpiredError:
            # Re-fetch container message to obtain fresh file_reference bytes
            fresh_msg = await client.get_messages(chat_id, ids=msg_id)
            return await client.download_media(fresh_msg, file=target_path)
        except FloodWaitError as exc:
            await asyncio.sleep(exc.seconds + 1)
            fresh_msg = await client.get_messages(chat_id, ids=msg_id)
            return await client.download_media(fresh_msg, file=target_path)

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(login_and_run())
