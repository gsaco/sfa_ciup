#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen


REPO_ROOT = Path(__file__).resolve().parents[3]
RAW_DIR = REPO_ROOT / "data" / "external" / "raw" / "ubigeo"
RAW_DIR.mkdir(parents=True, exist_ok=True)

URL = "https://raw.githubusercontent.com/jmcastagnetto/ubigeo-peru-aumentado/master/ubigeo_distrito.csv"
OUT_PATH = RAW_DIR / "ubigeo_distrito.csv"
META_PATH = RAW_DIR / "metadata_fallback.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def should_skip() -> bool:
    if not OUT_PATH.exists() or not META_PATH.exists():
        return False
    try:
        meta = json.loads(META_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    if meta.get("sha256") != sha256(OUT_PATH):
        return False
    if meta.get("url") != URL:
        return False
    return True


def download() -> None:
    with urlopen(URL) as response:
        data = response.read()
    OUT_PATH.write_bytes(data)

    meta = {
        "url": URL,
        "accessed_at": dt.datetime.now().isoformat(timespec="seconds"),
        "sha256": sha256(OUT_PATH),
        "size_bytes": OUT_PATH.stat().st_size,
        "license": "see repository LICENSE",
    }
    META_PATH.write_text(json.dumps(meta, indent=2), encoding="utf-8")


def main() -> None:
    if should_skip():
        print(f"Cached fallback OK: {OUT_PATH}")
        return
    download()
    print(f"Downloaded fallback {OUT_PATH}")
    print(f"Wrote {META_PATH}")


if __name__ == "__main__":
    main()
