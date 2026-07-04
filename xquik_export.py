"""Utilities for reading Xquik export files."""

from __future__ import annotations

import csv
import io
import json
from collections.abc import Iterable
from typing import Any

TEXT_FIELDS = ("Tweets", "tweet", "text", "full_text", "tweet_text", "content", "body")


def _iter_records(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        for key in ("data", "results", "tweets", "items"):
            nested = value.get(key)
            if isinstance(nested, list):
                yield from _iter_records(nested)
                return
        yield value
        return

    if isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                yield from _iter_records(item)


def _read_json_or_jsonl(raw: str) -> list[dict[str, Any]]:
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        rows: list[dict[str, Any]] = []
        for line in raw.splitlines():
            candidate = line.strip()
            if not candidate:
                continue
            rows.extend(_iter_records(json.loads(candidate)))
        return rows
    return list(_iter_records(parsed))


def _read_csv(raw: str) -> list[dict[str, Any]]:
    return list(csv.DictReader(io.StringIO(raw)))


def _first_text(row: dict[str, Any]) -> str:
    for field in TEXT_FIELDS:
        value = row.get(field)
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return ""


def load_xquik_tweets(payload: bytes) -> list[str]:
    """Return tweet texts from JSON, JSONL, or CSV export bytes."""
    raw = payload.decode("utf-8-sig").strip()
    if not raw:
        return []

    records = _read_json_or_jsonl(raw) if raw[:1] in "[{" else _read_csv(raw)
    tweets: list[str] = []
    for record in records:
        text = _first_text(record)
        if text:
            tweets.append(text)
    return tweets
