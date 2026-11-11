#!/usr/bin/env python3
"""
MTProto Peer ID <-> Bot API Dialog ID (`chat_id`) converter (Layer 225 / Bot API 10.4).
Source: https://core.telegram.org/api/bots/ids
Source: https://core.telegram.org/api/monoforum

Ranges in Bot API 10.4 / MTProto Layer 225:
- User / Bot (`peerUser`):          1 <= chat_id <= 1099511627775
- Basic Group (`peerChat`):         -999999999999 <= chat_id <= -1
- Supergroup/Channel (`peerChannel`): -1997852516352 <= chat_id <= -1000000000001
- Secret Chat (TDLib):              -2002147483648 <= chat_id <= -1997852516353
- Monoforum (`peerChannel` DM):     -4000000000000 <= chat_id <= -2002147483649
"""

from typing import Tuple

MAX_USER_ID = 1099511627775
MAX_CHAT_ID = 999999999999
CHANNEL_ZERO = -1000000000000
SECRET_ZERO = -2000000000000


def mtproto_to_bot_api_id(peer_type: str, raw_id: int) -> int:
    """Converts an MTProto (peer_type, raw_id) pair to a signed Bot API chat_id."""
    if peer_type == "user":
        if not (1 <= raw_id <= MAX_USER_ID):
            raise ValueError(f"Invalid MTProto user_id: {raw_id}")
        return raw_id
    elif peer_type == "chat":
        if not (1 <= raw_id <= MAX_CHAT_ID):
            raise ValueError(f"Invalid MTProto chat_id: {raw_id}")
        return -raw_id
    elif peer_type in ("channel", "monoforum"):
        if not (1 <= raw_id <= 997852516352 or 1002147483649 <= raw_id <= 3000000000000):
            raise ValueError(f"Invalid MTProto channel_id: {raw_id}")
        return CHANNEL_ZERO - raw_id
    elif peer_type == "secret":
        return SECRET_ZERO + raw_id
    raise ValueError(f"Unknown peer_type: {peer_type!r}")


def bot_api_to_mtproto_id(bot_dialog_id: int) -> Tuple[str, int]:
    """Converts a signed Bot API chat_id to (peer_type, raw_mtproto_id)."""
    if 1 <= bot_dialog_id <= MAX_USER_ID:
        return ("user", bot_dialog_id)
    if -MAX_CHAT_ID <= bot_dialog_id <= -1:
        return ("chat", -bot_dialog_id)
    if -1997852516352 <= bot_dialog_id <= -1000000000001:
        return ("channel", CHANNEL_ZERO - bot_dialog_id)
    if -2002147483648 <= bot_dialog_id <= -1997852516353:
        return ("secret", bot_dialog_id - SECRET_ZERO)
    if -4000000000000 <= bot_dialog_id <= -2002147483649:
        return ("monoforum", CHANNEL_ZERO - bot_dialog_id)
    raise ValueError(f"Out-of-range Bot API dialog ID: {bot_dialog_id}")


if __name__ == "__main__":
    cases = [
        ("user", 543210987),
        ("chat", 987654321),
        ("channel", 1234567890),
        ("monoforum", 1500000000000),
    ]
    for ptype, rid in cases:
        bot_id = mtproto_to_bot_api_id(ptype, rid)
        recovered_type, recovered_id = bot_api_to_mtproto_id(bot_id)
        print(f"MTProto ({ptype}, {rid}) <-> Bot API chat_id={bot_id} -> ({recovered_type}, {recovered_id})")
        assert recovered_type == ptype and recovered_id == rid
