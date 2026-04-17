"""Command-line entry point for openric-validate.

Exit codes:
    0 — all checks passed
    1 — one or more violations
    2 — warnings only
    3 — server unreachable
    4 — invalid invocation
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .http_client import fetch_json, ServerUnreachable
from .schema_check import validate_against_schema, SchemaCheckError
from .shape_check import validate_against_shapes
from .report import Report, Finding, Severity

SPEC_ROOT = Path(__file__).resolve().parent.parent.parent
SCHEMAS_DIR = SPEC_ROOT / "schemas"
SHAPES_PATH = SPEC_ROOT / "shapes" / "openric.shacl.ttl"


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="openric-validate",
        description="Validate an OpenRiC-conformant server or response against the specification.",
    )
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "server",
        nargs="?",
        help="Base URL of an OpenRiC server (e.g. https://archives.example.org/api/ric/v1)",
    )
    mode.add_argument(
        "--record",
        metavar="URL",
        help="Validate a single /records/{id} response at this URL",
    )
    mode.add_argument(
        "--file",
        metavar="PATH",
        type=Path,
        help="Validate a local JSON-LD file against shapes + schemas",
    )

    p.add_argument(
        "--level",
        choices=["L1", "L2", "L3", "L4"],
        default="L2",
        help="Conformance level to validate against (default: L2)",
    )
    p.add_argument(
        "--schemas",
        type=Path,
        default=SCHEMAS_DIR,
        help=f"Path to JSON Schemas directory (default: {SCHEMAS_DIR})",
    )
    p.add_argument(
        "--output",
        choices=["human", "json", "junit"],
        default="human",
        help="Report format (default: human)",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    report = Report()

    try:
        if args.record:
            _run_record_check(args.record, args.schemas, report)
        elif args.server:
            report.add(Finding(
                check="server-walk",
                severity=Severity.INFO,
                message=f"Server-level validation not yet implemented; use --record <url> for now.",
                target=args.server,
            ))
        elif args.file:
            report.add(Finding(
                check="file-check",
                severity=Severity.INFO,
                message="--file mode not yet implemented.",
                target=str(args.file),
            ))
    except ServerUnreachable as e:
        print(f"error: {e}", file=sys.stderr)
        return 3
    except Exception as e:  # top-level catchall — bugs return code 4
        print(f"internal error: {e}", file=sys.stderr)
        return 4

    report.emit(args.output)
    return report.exit_code()


def _run_record_check(url: str, schemas_dir: Path, report: Report) -> None:
    """Fetch one /records/{id} URL and validate against record.schema.json + SHACL."""
    response = fetch_json(url)
    report.add(Finding(
        check="http-fetch",
        severity=Severity.INFO,
        message=f"Fetched {url}",
        target=url,
    ))

    schema_path = schemas_dir / "record.schema.json"
    if not schema_path.exists():
        report.add(Finding(
            check="schema-load",
            severity=Severity.VIOLATION,
            message=f"Schema not found: {schema_path}",
            target=str(schema_path),
        ))
        return

    schema = json.loads(schema_path.read_text())
    try:
        validate_against_schema(response, schema)
        report.add(Finding(
            check="record-schema",
            severity=Severity.PASS,
            message="Response conforms to record.schema.json",
            target=url,
        ))
    except SchemaCheckError as e:
        for err in e.errors:
            report.add(Finding(
                check="record-schema",
                severity=Severity.VIOLATION,
                message=err.message,
                target=err.json_path,
            ))

    # SHACL validation against RiC-O shapes
    if SHAPES_PATH.exists():
        conforms, results_text = validate_against_shapes(response, SHAPES_PATH)
        if conforms:
            report.add(Finding(
                check="record-shacl",
                severity=Severity.PASS,
                message="Response conforms to openric.shacl.ttl",
                target=url,
            ))
        else:
            # Split pyshacl's multi-line text into one Finding per violation
            for block in _split_pyshacl_results(results_text):
                report.add(Finding(
                    check="record-shacl",
                    severity=Severity.VIOLATION,
                    message=block.strip()[:500],
                    target=url,
                ))
    else:
        report.add(Finding(
            check="record-shacl",
            severity=Severity.WARNING,
            message=f"SHACL shapes not found at {SHAPES_PATH}; skipping shape check",
            target=str(SHAPES_PATH),
        ))


def _split_pyshacl_results(text: str) -> list[str]:
    """Split pyshacl's human-readable report into per-violation blocks."""
    if "Constraint Violation" not in text:
        return [text]
    blocks = []
    current: list[str] = []
    for line in text.splitlines():
        if line.startswith("Constraint Violation") and current:
            blocks.append("\n".join(current))
            current = [line]
        else:
            current.append(line)
    if current:
        blocks.append("\n".join(current))
    return blocks
