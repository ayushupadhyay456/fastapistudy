"""Create a demo log group and write one ERROR line into it (works on Windows too).

Usage:  python scripts/put_test_error.py [log-group-name]
"""
import sys
import time

import boto3

group = sys.argv[1] if len(sys.argv) > 1 else "/demo/incident-app"
stream = "test-stream"
client = boto3.client("logs")

for create, kwargs in (
    (client.create_log_group, {"logGroupName": group}),
    (client.create_log_stream, {"logGroupName": group, "logStreamName": stream}),
):
    try:
        create(**kwargs)
    except client.exceptions.ResourceAlreadyExistsException:
        pass

client.put_log_events(
    logGroupName=group,
    logStreamName=stream,
    logEvents=[{"timestamp": int(time.time() * 1000), "message": "ERROR payment service timeout after 30s"}],
)
print(f"Wrote 1 ERROR line to {group}. Wait ~3 minutes before invoking the poller.")
