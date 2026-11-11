#!/usr/bin/env python3
"""
Cryptographic validator for Telegram Mini App `initData` AND Telegram Login Widget payloads.
Sources:
- Mini Apps initData: https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
- Login Widget: https://core.telegram.org/widgets/login#checking-authorization

Key difference:
- Mini App secret_key = HMAC_SHA256(key=b"WebAppData", msg=bot_token.encode("utf-8"))
- Login Widget secret_key = SHA256(bot_token.encode("utf-8"))
"""

import hashlib
import hmac
import time
import urllib.parse
from typing import Dict


def validate_webapp_init_data(init_data_raw: str, bot_token: str, max_age_seconds: int = 86400) -> Dict[str, str]:
    """Validates Telegram.WebApp.initData using HMAC-SHA256 and checks auth_date freshness."""
    parsed = dict(urllib.parse.parse_qsl(init_data_raw, keep_blank_values=True))
    received_hash = parsed.pop("hash", None)
    if not received_hash:
        raise ValueError("Missing 'hash' parameter in initData")

    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))
    secret_key = hmac.new(b"WebAppData", bot_token.encode("utf-8"), hashlib.sha256).digest()
    computed_hash = hmac.new(secret_key, data_check_string.encode("utf-8"), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(computed_hash, received_hash):
        raise ValueError("Invalid Mini App initData HMAC signature")

    auth_date = int(parsed.get("auth_date", "0"))
    if max_age_seconds > 0 and (time.time() - auth_date) > max_age_seconds:
        raise ValueError(f"Expired initData (auth_date={auth_date})")

    return parsed


def validate_login_widget_data(params: Dict[str, str], bot_token: str, max_age_seconds: int = 86400) -> Dict[str, str]:
    """Validates Telegram Login Widget callback parameters using SHA256(bot_token) as the HMAC key."""
    data = dict(params)
    received_hash = data.pop("hash", None)
    if not received_hash:
        raise ValueError("Missing 'hash' parameter in Login Widget payload")

    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))
    secret_key = hashlib.sha256(bot_token.encode("utf-8")).digest()
    computed_hash = hmac.new(secret_key, data_check_string.encode("utf-8"), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(computed_hash, received_hash):
        raise ValueError("Invalid Login Widget HMAC signature")

    auth_date = int(data.get("auth_date", "0"))
    if max_age_seconds > 0 and (time.time() - auth_date) > max_age_seconds:
        raise ValueError(f"Expired Login Widget payload (auth_date={auth_date})")

    return data


if __name__ == "__main__":
    # Self-test with a synthetic test token (never a real token)
    dummy_token = "000000000:TEST_SYNTHETIC_TOKEN_FOR_VALIDATION_ONLY"
    now_str = str(int(time.time()))
    sample_fields = {"auth_date": now_str, "query_id": "AAHdF6IQAAAAAN0XohDhrOrc", "user": '{"id":12345,"first_name":"Test"}'}
    check_str = "\n".join(f"{k}={v}" for k, v in sorted(sample_fields.items()))
    sk = hmac.new(b"WebAppData", dummy_token.encode(), hashlib.sha256).digest()
    sig = hmac.new(sk, check_str.encode(), hashlib.sha256).hexdigest()
    query = urllib.parse.urlencode({**sample_fields, "hash": sig})
    verified = validate_webapp_init_data(query, dummy_token)
    print("Verified Mini App initData successfully:", verified["user"])
