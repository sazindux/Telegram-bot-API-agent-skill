#!/usr/bin/env python3
"""
Context-aware Telegram MarkdownV2 escaper.
Source: https://core.telegram.org/bots/api#markdownv2-style

Rules:
- Outside code/links: escape all 18 special characters: _ * [ ] ( ) ~ ` > # + - = | { } . ! and \\
- Inside inline `code` or ```pre``` blocks: escape only ` and \\
- Inside (...) inline link URL or custom emoji URL: escape only ) and \\
"""

import re
import sys

SPECIAL_CHARS_OUTSIDE = "_*[]()~`>#+-=|{}.!\\"
ESCAPE_OUTSIDE_RE = re.compile(r"([_\*\[\]\(\)~`>#\+\-=\|\{\}\.!\\])")
ESCAPE_CODE_RE = re.compile(r"([`\\])")
ESCAPE_URL_RE = re.compile(r"([\)\\])")


def escape_markdown_v2(text: str) -> str:
    """Escapes plain text for safe inclusion in a MarkdownV2 message body."""
    return ESCAPE_OUTSIDE_RE.sub(r"\\\1", text)


def escape_markdown_v2_code(code_text: str) -> str:
    """Escapes text inside `inline code` or ```pre``` blocks in MarkdownV2."""
    return ESCAPE_CODE_RE.sub(r"\\\1", code_text)


def escape_markdown_v2_url(url: str) -> str:
    """Escapes a URL inside [label](url) in MarkdownV2."""
    return ESCAPE_URL_RE.sub(r"\\\1", url)


if __name__ == "__main__":
    sample = sys.argv[1] if len(sys.argv) > 1 else "Price: $19.99 (save 20%!) -> #deal_2026 [1+1=2]"
    escaped = escape_markdown_v2(sample)
    code_sample = escape_markdown_v2_code("const x = `hello \\ world`;")
    url_sample = escape_markdown_v2_url("https://en.wikipedia.org/wiki/Telegram_(software)")
    print("Original:", sample)
    print("Escaped body:", escaped)
    print("Escaped code:", f"`{code_sample}`")
    print("Escaped link:", f"[{escape_markdown_v2('Telegram Wiki')}]({url_sample})")
    assert "\\." in escaped and "\\!" in escaped and "\\=" in escaped
    assert url_sample.endswith("\\)")
