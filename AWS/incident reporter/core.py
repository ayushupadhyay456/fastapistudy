"""
Shared logic for the CloudWatch error poller.

Two entry points use it:
  - poller/handler.py    -> runs inside AWS Lambda
  - poller/local_run.py  -> runs as a normal Python program on your own machine

The "store" is where the checkpoint (last processed time) is kept. Any object with
get() and set(timestamp_ms) works, so the same logic runs with a file, SSM, or later Postgres.
"""
import functools
import logging
import os
import time
from datetime import datetime, timezone

import boto3

logger = logging.getLogger(__name__)

FILTER_PATTERN = os.environ.get("FILTER_PATTERN", "ERROR")
FIRST_RUN_LOOKBACK_MINUTES = int(os.environ.get("FIRST_RUN_LOOKBACK_MINUTES", "30"))
# CloudWatch can be a little late in showing logs, so we stay a bit behind "now".
INGESTION_DELAY_SECONDS = int(os.environ.get("INGESTION_DELAY_SECONDS", "120"))


def parse_groups(text):
    """'a, b' -> ['a', 'b']"""
    return [g.strip() for g in (text or "").split(",") if g.strip()]


@functools.lru_cache(maxsize=1)
def _logs_client():
    return boto3.client("logs")


def fetch_errors(log_group, start_ms, end_ms):
    """Read all matching log events of one log group between start_ms and end_ms."""
    client = _logs_client()
    paginator = client.get_paginator("filter_log_events")
    found = []
    try:
        for page in paginator.paginate(
            logGroupName=log_group,
            startTime=start_ms,
            endTime=end_ms,
            filterPattern=FILTER_PATTERN,
        ):
            for event in page["events"]:
                found.append(
                    {
                        "log_group": log_group,
                        "log_stream": event["logStreamName"],
                        "timestamp": event["timestamp"],
                        "event_id": event["eventId"],
                        "message": event["message"].rstrip(),
                    }
                )
    except client.exceptions.ResourceNotFoundException:
        logger.warning("Log group not found, skipping: %s", log_group)
    return found


def process_errors(errors):
    """
    Phase 1: just print the errors.
    Phase 2 will group them and send a Slack DM.
    Phase 3 will hand them to the LangGraph agent.
    """
    for err in errors:
        when = datetime.fromtimestamp(err["timestamp"] / 1000, tz=timezone.utc).isoformat()
        logger.info("NEW ISSUE | %s | %s | %s", err["log_group"], when, err["message"][:500])


def run_once(store, log_groups, fetch_fn=None, process_fn=None, now_ms=None):
    """One polling round. Returns a small dict describing what happened."""
    fetch_fn = fetch_fn or fetch_errors
    process_fn = process_fn or process_errors
    if now_ms is None:
        now_ms = int(time.time() * 1000)
    end_ms = now_ms - INGESTION_DELAY_SECONDS * 1000

    checkpoint = store.get()
    if checkpoint is None:
        start_ms = end_ms - FIRST_RUN_LOOKBACK_MINUTES * 60 * 1000
    else:
        start_ms = checkpoint + 1  # +1 so the last log we already read is not read twice

    if start_ms > end_ms:
        logger.info("Nothing to do yet, window is empty")
        return {"status": "skipped", "error_count": 0}

    errors = []
    for group in log_groups:
        errors.extend(fetch_fn(group, start_ms, end_ms))

    process_fn(errors)

    # Move the checkpoint ONLY after everything above worked. If anything fails,
    # the exception stops us here and the next run reads the same window again.
    store.set(end_ms)

    logger.info("Run finished: %d new error(s) in %d log group(s)", len(errors), len(log_groups))
    return {
        "status": "ok",
        "error_count": len(errors),
        "window": {"start_ms": start_ms, "end_ms": end_ms},
    }
