import json, os
from pathlib import Path
from datetime import datetime, timedelta, timezone
from authlib.jose import JsonWebKey

KEYS_FILE = Path(os.getenv("KEYS_FILE", "keys.json"))
ROTATION_DAYS = int(os.getenv("JWT_ROTATION_DAYS", 30))


def utcnow():
    return datetime.now(timezone.utc)


def _load():
    if not KEYS_FILE.exists():
        return None
    return json.loads(KEYS_FILE.read_text())


def _save(data):
    KEYS_FILE.write_text(json.dumps(data, indent=2))


def _generate():
    key = JsonWebKey.generate_key("RSA", 2048, is_private=True)
    kid = key.thumbprint()
    return kid, key


def get_active_key():
    now = utcnow()
    data = _load()

    if not data:
        kid, key = _generate()
        data = {
            "kid": kid,
            "created": now.isoformat(),
            "private": key.as_dict(True),
            "public": key.as_dict(False),
        }
        _save(data)
        return kid, key

    created = datetime.fromisoformat(data["created"])
    if now - created > timedelta(days=ROTATION_DAYS):
        kid, key = _generate()
        data = {
            "kid": kid,
            "created": now.isoformat(),
            "private": key.as_dict(True),
            "public": key.as_dict(False),
        }
        _save(data)
        return kid, key

    return data["kid"], JsonWebKey.import_key(data["private"])


def get_jwks():
    data = _load()
    if not data:
        return {"keys": []}

    pub = data["public"]
    pub.update({"kid": data["kid"], "use": "sig", "alg": "RS256"})
    return {"keys": [pub]}
