"""AWS Lambda entry point. The real work is in core.py."""
import logging
import os

from core import parse_groups, run_once
from stores import SsmStore

logging.getLogger().setLevel(logging.INFO)


def lambda_handler(event, context):
    # IMPORTANT: never put this poller's own log group in LOG_GROUPS.
    store = SsmStore(os.environ.get("CHECKPOINT_PARAM", "/incident-agent/checkpoint"))
    return run_once(store, parse_groups(os.environ.get("LOG_GROUPS", "")))
