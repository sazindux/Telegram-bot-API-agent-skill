#!/usr/bin/env python3
"""
UTF-16 code unit offset & length calculator for Telegram MessageEntity.
Source: https://core.telegram.org/bots/api#messageentity

Telegram counts entity `offset` and `length` in UTF-16 code units (2 bytes per unit),
NOT Unicode code points (Python len()) or UTF-8 bytes.
Characters >= U+10000 (such as emoji 🚀) use a surrogate pair (2 UTF-16 code units).
"""

from typing import Any


def utf16_length(text: str) -> int:
    """Returns the number of UTF-16 code units in `text`."""
    return len(text.encode("utf-16-le")) // 2


def utf16_slice(text: str, offset: int, length: int) -> str:
    """Extracts a substring from `text` using UTF-16 `offset` and `length`."""
    raw = text.encode("utf-16-le")
    byte_start = offset * 2
    byte_end = (offset + length) * 2
    return raw[byte_start:byte_end].decode("utf-16-le")


def build_entity(full_text: str, substring: str, entity_type: str, **extra: Any) -> dict[str, Any]:
    """Finds the first occurrence of `substring` in `full_text` and returns a MessageEntity dict."""
    py_idx = full_text.find(substring)
    if py_idx == -1:
        raise ValueError(f"Substring {substring!r} not found in text")
    prefix = full_text[:py_idx]
    entity: dict[str, Any] = {
        "type": entity_type,
        "offset": utf16_length(prefix),
        "length": utf16_length(substring),
    }
    entity.update(extra)
    return entity


if __name__ == "__main__":
    msg = "Hi 🚀👨‍👩‍👧‍👦! Click TON: UQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqEBI"
    ton_addr = "UQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqEBI"
    ent = build_entity(msg, ton_addr, "ton_address")
    extracted = utf16_slice(msg, ent["offset"], ent["length"])
    print("Message:", msg)
    print("Python len(msg):", len(msg), "| UTF-16 length:", utf16_length(msg))
    print("Computed Entity:", ent)
    print("Extracted via UTF-16 slice:", extracted)
    assert extracted == ton_addr, "UTF-16 slice mismatch!"
