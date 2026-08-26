#!/usr/bin/env python3
"""Replay an ADK JSONL event recording as a fresh Google Cloud trace."""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from typing import Any


def load_events(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"Line {line_number} is not a JSON object")
            records.append(value)
    return records


def event_types(event: dict[str, Any]) -> str:
    kinds: list[str] = []
    for part in (event.get("content") or {}).get("parts") or []:
        if not isinstance(part, dict):
            continue
        if "text" in part:
            kinds.append("text")
        if "functionCall" in part:
            kinds.append("function_call")
        if "functionResponse" in part:
            kinds.append("function_response")
        if "inlineData" in part:
            kinds.append("inline_data")
    state_delta = ((event.get("actions") or {}).get("stateDelta") or {})
    if state_delta:
        kinds.append("state_delta")
    return ",".join(dict.fromkeys(kinds)) or "event"


def attributes(event: dict[str, Any], sequence: int) -> dict[str, Any]:
    actions = event.get("actions") or {}
    state_delta = actions.get("stateDelta") or {}
    return {
        "replay.telemetry_only": True,
        "recorded.event.sequence": sequence,
        "recorded.event.id": str(event.get("id") or ""),
        "recorded.event.author": str(event.get("author") or "unknown"),
        "recorded.event.type": event_types(event),
        "recorded.invocation_id": str(event.get("invocationId") or ""),
        "recorded.state_delta.keys": ",".join(sorted(state_delta)),
    }


def planned_timestamps(events: list[dict[str, Any]], speed: float) -> list[int]:
    raw = [float(event.get("timestamp") or 0.0) for event in events]
    first = raw[0]
    relative = [max(0.0, timestamp - first) / speed for timestamp in raw]
    anchor = time.time_ns() - int(relative[-1] * 1_000_000_000) - 1_000_000_000
    return [anchor + int(delta * 1_000_000_000) for delta in relative]


def emit(events: list[dict[str, Any]], project_id: str, speed: float) -> None:
    os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
    os.environ["OTEL_SERVICE_NAME"] = "class-02c-replay"
    os.environ["OTEL_RESOURCE_ATTRIBUTES"] = (
        "deployment.environment=classroom,class.name=02C,replay.mode=telemetry_only"
    )

    from google.adk.telemetry.google_cloud import get_gcp_exporters
    from google.adk.telemetry.setup import maybe_set_otel_providers
    from opentelemetry import trace

    exporters = get_gcp_exporters(enable_cloud_tracing=True)
    maybe_set_otel_providers([exporters])

    provider = trace.get_tracer_provider()
    tracer = trace.get_tracer("class-02c.event-replay")
    timestamps = planned_timestamps(events, speed)

    root = tracer.start_span(
        "replay.adk.session",
        start_time=timestamps[0],
        attributes={
            "replay.telemetry_only": True,
            "replay.event_count": len(events),
            "replay.source_invocation_id": str(events[0].get("invocationId") or ""),
        },
    )
    parent_context = trace.set_span_in_context(root)

    try:
        for sequence, (event, start_time) in enumerate(
            zip(events, timestamps, strict=True), start=1
        ):
            event_attributes = attributes(event, sequence)
            author = event_attributes["recorded.event.author"]
            span = tracer.start_span(
                f"replay.event.{author}",
                context=parent_context,
                start_time=start_time,
                attributes=event_attributes,
            )
            span.add_event(
                "recorded.adk.event",
                attributes=event_attributes,
                timestamp=start_time,
            )
            span.end(end_time=start_time + 1_000_000)
    finally:
        root.end(end_time=timestamps[-1] + 10_000_000)
        force_flush = getattr(provider, "force_flush", None)
        if callable(force_flush):
            force_flush()
        shutdown = getattr(provider, "shutdown", None)
        if callable(shutdown):
            shutdown()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("recording", type=Path, nargs="?", default=Path(__file__).with_name("events.jsonl"))
    parser.add_argument("--project-id", default=os.getenv("GOOGLE_CLOUD_PROJECT"))
    parser.add_argument("--speed", type=float, default=4.0)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.speed <= 0:
        parser.error("--speed must be greater than zero")

    events = load_events(args.recording)
    if not events:
        raise SystemExit("The recording contains no events")

    if args.dry_run:
        print(f"Would replay {len(events)} events")
        for sequence, event in enumerate(events, start=1):
            print(
                f"{sequence:03d} "
                f"{event.get('author', 'unknown')}: "
                f"{event_types(event)}"
            )
        return

    if not args.project_id:
        raise SystemExit("Set GOOGLE_CLOUD_PROJECT or pass --project-id")

    emit(events, args.project_id, args.speed)
    print(
        f"Replayed {len(events)} events to Google Cloud Trace "
        f"in project {args.project_id}"
    )


if __name__ == "__main__":
    main()
