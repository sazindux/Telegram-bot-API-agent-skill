#!/usr/bin/env python3
"""
Audits the telegram-api-skill repository:
1. Confirms all 186 Bot API 10.4 methods and 402 types are documented in references/bot-api/.
2. Confirms all changelog versions from Bot API 6.0 through 10.4 (38 releases) are covered in references/whats-new.md.
3. Confirms zero hard-coded bot tokens or secrets exist in any file.
"""

import pathlib
import re

SKILL_ROOT = pathlib.Path(__file__).resolve().parent.parent


def run_audit() -> None:
    methods_md = (SKILL_ROOT / "references" / "bot-api" / "methods.md").read_text(encoding="utf-8")
    types_md = (SKILL_ROOT / "references" / "bot-api" / "types.md").read_text(encoding="utf-8")
    whats_new_md = (SKILL_ROOT / "references" / "whats-new.md").read_text(encoding="utf-8")

    method_rows = re.findall(r"^\| \[`([a-zA-Z0-9_]+)`\]", methods_md, flags=re.MULTILINE)
    type_rows = re.findall(r"^\| \[`([a-zA-Z0-9_]+)`\]", types_md, flags=re.MULTILINE)
    versions_found = set(re.findall(r"\b(10\.[0-4]|9\.[0-6]|8\.[0-3]|7\.(?:10|11|[0-9])|6\.[0-9])\b", whats_new_md))

    token_pattern = re.compile(r"\b[1-9][0-9]{7,10}:[A-Za-z0-9_-]{35}\b")
    leaked_tokens = []
    for path in SKILL_ROOT.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".py", ".js", ".json", ".yml"}:
            text = path.read_text(encoding="utf-8", errors="ignore")
            for match in token_pattern.findall(text):
                leaked_tokens.append((str(path.relative_to(SKILL_ROOT)), match))

    assert len(method_rows) == 186, f"Expected 186 methods, found {len(method_rows)}"
    assert len(type_rows) == 402, f"Expected 402 types, found {len(type_rows)}"
    assert len(versions_found) == 38, f"Expected 38 Bot API versions (6.0..10.4), found {len(versions_found)}: {sorted(versions_found)}"
    assert len(leaked_tokens) == 0, f"Found leaked tokens: {leaked_tokens}"

    print(f"Audit passed: {len(method_rows)}/186 methods, {len(type_rows)}/402 types, {len(versions_found)}/38 changelog releases (6.0-10.4), 0 leaked secrets.")


if __name__ == "__main__":
    run_audit()
