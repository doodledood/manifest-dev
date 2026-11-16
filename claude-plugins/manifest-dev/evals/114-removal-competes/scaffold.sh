#!/usr/bin/env bash
set -euo pipefail
mkdir -p app deploy notes
cat > README.md <<'EOF'
# accounts

The account service behind our web app: profile pages, settings, billing details and the public
API. Runs under gunicorn (see `deploy/gunicorn.conf.py`). Profiles live in Postgres and are cached
in Redis.
EOF
cat > CHANGELOG.md <<'EOF'
# Changelog

## 2025-09-02
- Removed the old dashboard and its profile widget. The new dashboard reads no profiles.

## 2025-03-10
- Added an in-process profile cache (`app/local_cache.py`): the dashboard's profile widget read
  the same profile about 40 times per page and Redis round trips added up.

## 2025-01-14
- Profiles cached in Redis. p95 profile read is 2 ms.
EOF
cat > app/__init__.py <<'EOF'
EOF
cat > app/db.py <<'EOF'
def load_profile(user_id: int) -> dict:
    """SELECT id, name, email FROM profiles WHERE id = %s"""
    raise NotImplementedError


def save_email(user_id: int, email: str) -> None:
    """UPDATE profiles SET email = %s WHERE id = %s"""
    raise NotImplementedError
EOF
cat > app/redis_cache.py <<'EOF'
import json

import redis

_r = redis.Redis()
TTL_SECONDS = 24 * 3600


def get(key: str) -> dict | None:
    raw = _r.get(key)
    return json.loads(raw) if raw else None


def set(key: str, value: dict) -> None:
    _r.set(key, json.dumps(value), ex=TTL_SECONDS)


def delete(key: str) -> None:
    _r.delete(key)
EOF
cat > app/local_cache.py <<'EOF'
import time

# Per-process cache in front of Redis, for the dashboard's profile widget.
TTL_SECONDS = 3600
_store: dict[int, tuple[float, dict]] = {}


def get(user_id: int) -> dict | None:
    hit = _store.get(user_id)
    if hit and time.time() - hit[0] < TTL_SECONDS:
        return hit[1]
    return None


def set(user_id: int, profile: dict) -> None:
    _store[user_id] = (time.time(), profile)
EOF
cat > app/profile.py <<'EOF'
from . import db, local_cache, redis_cache


def get_profile(user_id: int) -> dict:
    profile = local_cache.get(user_id)
    if profile:
        return profile
    profile = redis_cache.get(f"profile:{user_id}")
    if profile is None:
        profile = db.load_profile(user_id)
        redis_cache.set(f"profile:{user_id}", profile)
    local_cache.set(user_id, profile)
    return profile


def update_email(user_id: int, email: str) -> None:
    db.save_email(user_id, email)
    redis_cache.delete(f"profile:{user_id}")
EOF
cat > app/settings_page.py <<'EOF'
from .profile import get_profile, update_email


def show(user_id: int) -> dict:
    return {"email": get_profile(user_id)["email"]}


def change_email(user_id: int, email: str) -> dict:
    update_email(user_id, email)
    return show(user_id)
EOF
cat > app/api.py <<'EOF'
from .profile import get_profile


def me(user_id: int) -> dict:
    return get_profile(user_id)
EOF
cat > app/billing.py <<'EOF'
from .profile import get_profile


def invoice_recipient(user_id: int) -> str:
    return get_profile(user_id)["email"]
EOF
cat > deploy/gunicorn.conf.py <<'EOF'
workers = 8
bind = "0.0.0.0:8000"
EOF
cat > notes/support.md <<'EOF'
# Support — October

- 6 tickets: "I changed my email but the old one still shows." Shows the new one after a while,
  up to an hour. Two users say it flips between old and new when they refresh.
- One ticket: an invoice went to the old address the morning after a change.
EOF
