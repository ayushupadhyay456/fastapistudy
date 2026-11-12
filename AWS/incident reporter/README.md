# AWS Incident Investigator Agent

An AI agent that watches CloudWatch logs, investigates new errors, and sends a Slack DM
(with Approve / Reject buttons for risky fixes).

## Phase 1: the poller

Goal: read **only the new** ERROR logs since the last run and print them.

### How it works
1. Read the **checkpoint** (the last processed time).
2. Ask CloudWatch for ERROR logs between `checkpoint + 1` and `now - 2 minutes`.
3. Process them (Phase 1: print them).
4. Only if steps 2 and 3 worked, save the new checkpoint.

If anything fails, the checkpoint does not move, so the next run reads the same window again. No errors are lost.

### Files
- `poller/core.py` - the shared logic
- `poller/stores.py` - where the checkpoint lives (`FileStore` for local, `SsmStore` for Lambda)
- `poller/local_run.py` - run on your own machine (no Lambda)
- `poller/handler.py` + `template.yaml` - the AWS Lambda version (optional)
- `tests/test_core.py` - tests, no AWS needed
- `scripts/put_test_error.py` - writes a fake ERROR log for testing

### Setup
```
pip install -r requirements-dev.txt
pytest
aws configure
```

### Option A: run on your machine (no Lambda)
```
python scripts/put_test_error.py /demo/incident-app
```
Wait about 3 minutes (the poller stays 2 minutes behind "now"), then:
```
python poller/local_run.py --groups /demo/incident-app
```
You should see a `NEW ISSUE` line. Run the same command again: it should find 0 new errors. That proves the checkpoint works.

To keep it running and check every 30 minutes:
```
python poller/local_run.py --groups /demo/incident-app --every 30
```
Later phases replace this loop with Celery beat inside the agent service.

### Option B: deploy to AWS Lambda
```
sam build
sam deploy --guided
```
When it asks for `LogGroups`, type your log group(s). Never include `/aws/lambda/incident-agent-poller`.

### Known limits (fixed in later phases)
- No grouping of repeated errors yet (Phase 2).
- Lambda IAM read access is on all log groups; narrow it later.
- Very large error bursts are read in one run; add a cap later if needed.
