# Copyright (C) 2026 Johan Pieterse
# Plain Sailing Information Systems
# Email: johan@plansailingisystems.co.za
#
# This file is part of OpenRiC.
#
# OpenRiC is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Freeze a live OpenRiC server response as a conformance fixture.

Usage:
    python tools/freeze_fixture.py <case-name> <url> [--notes="..."]

Example:
    python tools/freeze_fixture.py agent-person-simple \
        https://heratio.theahg.co.za/api/ric/v1/agents/d6mh-ktzy-h6qz

Writes:
    fixtures/<case-name>/expected.jsonld
    fixtures/<case-name>/source-url.txt
    fixtures/<case-name>/notes.md   (if --notes given and file does not exist)

Does NOT write input.json — that's the AtoM-shape input, which for v0.1-draft
we capture manually on a per-case basis (see existing fonds-minimal).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import requests

FIXTURES_DIR = Path(__file__).resolve().parent.parent.parent / "fixtures"


def freeze(case: str, url: str, notes: str | None) -> int:
    case_dir = FIXTURES_DIR / case
    case_dir.mkdir(parents=True, exist_ok=True)

    try:
        resp = requests.get(
            url,
            headers={"Accept": "application/ld+json, application/json;q=0.9"},
            timeout=20,
        )
    except requests.exceptions.RequestException as e:
        print(f"fetch failed: {e}", file=sys.stderr)
        return 3

    # 4xx responses are valid for error-fixture capture; we still parse JSON below.
    if resp.status_code >= 500:
        print(f"{url} returned HTTP {resp.status_code}", file=sys.stderr)
        return 3
    if resp.status_code >= 400:
        print(f"note: capturing {resp.status_code} response from {url}", file=sys.stderr)

    try:
        payload = resp.json()
    except json.JSONDecodeError as e:
        print(f"response was not valid JSON: {e}", file=sys.stderr)
        return 3

    expected_path = case_dir / "expected.jsonld"
    expected_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=False) + "\n"
    )

    (case_dir / "source-url.txt").write_text(url + "\n")

    notes_path = case_dir / "notes.md"
    if not notes_path.exists():
        body = notes or f"Auto-frozen from `{url}`."
        notes_path.write_text(
            f"# Fixture: `{case}`\n\n"
            f"**Source:** [`{url}`]({url})\n\n"
            f"{body}\n\n"
            f"**Validation:** `expected.jsonld` MUST validate against the "
            f"schema selected by its `@type`.\n"
        )

    print(f"Frozen {case} ({len(json.dumps(payload))} bytes) -> {case_dir}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("case", help="Fixture folder name (e.g. agent-person-simple)")
    p.add_argument("url", help="Live URL to fetch")
    p.add_argument("--notes", default=None, help="Optional notes body")
    args = p.parse_args()
    return freeze(args.case, args.url, args.notes)


if __name__ == "__main__":
    raise SystemExit(main())
