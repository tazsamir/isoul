#!/usr/bin/env python3
"""Build static, multi-country evening TV data from TVmaze.

TVmaze data is CC BY-SA 4.0. The output is deliberately labelled as a
partial discovery guide rather than a complete electronic programme guide.
"""

from __future__ import annotations

import argparse
import json
import os
import tempfile
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

API = "https://api.tvmaze.com/schedule"
MAX_CHANNELS = 5
MAX_PROGRAMMES_PER_CHANNEL = 4
EVENING_START = 18 * 60
EVENING_END = 24 * 60

REGIONS = {
    "GB": {"label": "United Kingdom", "timezone": "Europe/London", "channels": ["BBC One", "BBC Two", "ITV1", "Channel 4", "Channel 5"]},
    "US": {"label": "United States", "timezone": "America/New_York", "channels": ["ABC", "CBS", "NBC", "FOX", "PBS"]},
}

CHANNEL_ALIASES = {"5": "Channel 5", "Fox": "FOX"}


def _minutes(value: str) -> int:
    try:
        hour, minute = value.split(":", 1)
        return int(hour) * 60 + int(minute)
    except (AttributeError, TypeError, ValueError):
        return -1


def _programme(record: dict) -> dict:
    show = record.get("show") or {}
    episode_number = record.get("number")
    season = record.get("season")
    opening = episode_number == 1
    descriptor = "New series" if opening and season == 1 else ("Series return" if opening else "New episode")
    genres = [str(genre) for genre in (show.get("genres") or [])[:2]]
    if genres:
        descriptor += " · " + " · ".join(genres)
    return {
        "time": str(record.get("airtime") or ""),
        "title": str(show.get("name") or record.get("name") or "Untitled programme"),
        "episode": str(record.get("name") or ""),
        "blurb": descriptor,
        "source_url": str(record.get("url") or show.get("url") or ""),
    }


def select_channels(records: list[dict], config: dict) -> list[dict]:
    """Return up to five actual broadcast networks, each with evening shows."""
    grouped: dict[str, list[dict]] = {}
    for record in records:
        show = record.get("show") or {}
        network = show.get("network") or {}
        channel = network.get("name")
        airtime = str(record.get("airtime") or "")
        if not channel or not (EVENING_START <= _minutes(airtime) < EVENING_END):
            continue
        channel = CHANNEL_ALIASES.get(str(channel), str(channel))
        grouped.setdefault(channel, []).append(_programme(record))

    preferred = [CHANNEL_ALIASES.get(name, name) for name in config.get("channels", [])]
    preferred_rank = {name: index for index, name in enumerate(preferred)}
    ordered_names = sorted(
        grouped,
        key=lambda name: (
            0 if name in preferred_rank else 1,
            preferred_rank.get(name, 999),
            -len(grouped[name]),
            name.casefold(),
        ),
    )[:MAX_CHANNELS]

    channels = []
    for name in ordered_names:
        programmes = sorted(grouped[name], key=lambda item: (_minutes(item["time"]), item["title"].casefold()))
        channels.append({"name": name, "programmes": programmes[:MAX_PROGRAMMES_PER_CHANNEL]})
    return channels


def build_region(code: str, date: str, records: list[dict]) -> dict:
    config = REGIONS[code]
    channels = select_channels(records, config)
    if len(channels) >= MAX_CHANNELS:
        status = "ready"
        note = "Five selected broadcast channels. This is a discovery view, not a complete TV guide."
    elif channels:
        status = "limited"
        note = f"TVmaze currently has incomplete coverage here: {len(channels)} broadcast channel{'s' if len(channels) != 1 else ''} found tonight."
    else:
        status = "unavailable"
        note = "TVmaze has no evening broadcast listings for this country tonight. No programmes have been invented or scraped from another guide."
    return {
        "code": code,
        "label": config["label"],
        "date": date,
        "timezone": config["timezone"],
        "status": status,
        "note": note,
        "channels": channels,
    }


def failed_region(code: str, date: str, previous: dict | None, _error: str) -> dict:
    if previous and previous.get("channels"):
        stale = dict(previous)
        stale["status"] = "stale"
        stale["note"] = "The latest refresh failed, so the last successful listings are shown with their original date."
        return stale
    config = REGIONS[code]
    return {
        "code": code,
        "label": config["label"],
        "date": date,
        "timezone": config["timezone"],
        "status": "unavailable",
        "note": "The listings source could not be reached. Try again later.",
        "channels": [],
    }


def fetch_schedule(code: str, date: str) -> list[dict]:
    query = urllib.parse.urlencode({"country": code, "date": date})
    request = urllib.request.Request(
        f"{API}?{query}",
        headers={"Accept": "application/json", "User-Agent": "isoul.uk-discover-prototype/2.0"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if not isinstance(payload, list):
        raise ValueError("TVmaze schedule response was not a list")
    return payload


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=path.name, suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as output:
            json.dump(payload, output, indent=2, ensure_ascii=False)
            output.write("\n")
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def load_previous(path: Path) -> dict[str, dict]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return {region.get("code"): region for region in payload.get("regions", []) if region.get("code")}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", help="ISO date override; otherwise each country's local date")
    parser.add_argument("--output", default="data/discover/tonight.json")
    parser.add_argument("--region", action="append", choices=REGIONS, help="Only fetch this region; repeat as needed")
    args = parser.parse_args()

    output = Path(args.output)
    previous = load_previous(output)
    codes = args.region or list(REGIONS)
    now = datetime.now(ZoneInfo("UTC"))
    regions = []
    for code in codes:
        local_date = args.date or now.astimezone(ZoneInfo(REGIONS[code]["timezone"])).date().isoformat()
        try:
            regions.append(build_region(code, local_date, fetch_schedule(code, local_date)))
        except Exception as error:
            regions.append(failed_region(code, local_date, previous.get(code), str(error)))

    payload = {
        "generated": now.isoformat(timespec="seconds"),
        "source_name": "TVmaze",
        "source_url": "https://www.tvmaze.com/api",
        "licence": "CC BY-SA 4.0",
        "licence_url": "https://creativecommons.org/licenses/by-sa/4.0/",
        "note": "New episodes from up to five broadcast networks per country. This is not a complete EPG; coverage varies by country.",
        "regions": regions,
    }
    write_json(output, payload)
    counts = ", ".join(f"{r['code']}:{len(r['channels'])}" for r in regions)
    print(f"Wrote {len(regions)} regions ({counts}) to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
