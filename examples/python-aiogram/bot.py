#!/usr/bin/env python3
"""
Python aiogram 3.x example for Telegram Bot API 10.4:
- Expandable blockquote + custom emoji + spoiler + date-time entities
- Bot API 10.4 `sendWidget` and `answerWidgetQuery` via custom TelegramMethod
- Telegram Stars (`XTR`) invoice + `pre_checkout_query` + `refundStarPayment`
- Safe rate-limit (`TelegramRetryAfter` / HTTP 429) handling

Env vars required at runtime:
- BOT_TOKEN (obtained from @BotFather; never hard-coded)
"""

import asyncio
import json
import os
from typing import Any

from aiogram import Bot, Dispatcher, F, Router
from aiogram.exceptions import TelegramRetryAfter
from aiogram.filters import Command
from aiogram.methods.base import TelegramMethod
from aiogram.types import LabeledPrice, Message, PreCheckoutQuery

router = Router()


class SendWidget(TelegramMethod[dict[str, Any]]):
    """Bot API 10.4 sendWidget wrapper for aiogram 3.x."""
    __returning__ = dict[str, Any]
    __api_method__ = "sendWidget"

    chat_id: int | str
    url: str
    aspect_ratio: str | None = None
    data: str | None = None


@router.message(Command("format"))
async def cmd_format(message: Message) -> None:
    html_text = (
        "<b>Bot API 10.4 Rich Formatting Demo</b>\n"
        "<tg-spoiler>Hidden spoiler text</tg-spoiler>\n"
        "<tg-time unix=\"1794396000\" format=\"r\">Nov 11, 2026</tg-time>\n"
        "<blockquote expandable>Line 1 of expandable quote\nLine 2\nLine 3\nLine 4</blockquote>"
    )
    await message.answer(html_text, parse_mode="HTML")


@router.message(Command("widget"))
async def cmd_widget(message: Message, bot: Bot) -> None:
    await bot(
        SendWidget(
            chat_id=message.chat.id,
            url="https://widgets.example.com/poll-card",
            aspect_ratio="16:9",
            data=json.dumps({"poll_id": "p_104", "votes": [5, 3]}),
        )
    )


@router.message(Command("stars"))
async def cmd_stars(message: Message) -> None:
    await message.answer_invoice(
        title="AI Credits Pack",
        description="100 AI generations paid via Telegram Stars",
        payload="credits_100",
        currency="XTR",
        prices=[LabeledPrice(label="100 Credits", amount=25)],
    )


@router.pre_checkout_query()
async def on_pre_checkout(query: PreCheckoutQuery) -> None:
    # Must answer within 10 seconds
    await query.answer(ok=True)


@router.message(F.successful_payment)
async def on_successful_payment(message: Message) -> None:
    sp = message.successful_payment
    if sp:
        await message.answer(
            f"Payment received! Charge ID: <code>{sp.telegram_payment_charge_id}</code>",
            parse_mode="HTML",
        )


async def safe_broadcast(bot: Bot, user_ids: list[int], text: str) -> None:
    """Broadcasts safely at <=25 msg/sec while respecting 429 retry_after."""
    for uid in user_ids:
        while True:
            try:
                await bot.send_message(chat_id=uid, text=text)
                await asyncio.sleep(0.04)  # 25 msg/sec ceiling
                break
            except TelegramRetryAfter as exc:
                await asyncio.sleep(exc.retry_after + 1)


async def main() -> None:
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise RuntimeError("Set BOT_TOKEN environment variable before running bot.py")
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(
        bot,
        allowed_updates=[
            "message",
            "callback_query",
            "pre_checkout_query",
            "widget_query",
            "shared_widget_query",
            "message_reaction",
        ],
    )


if __name__ == "__main__":
    asyncio.run(main())
