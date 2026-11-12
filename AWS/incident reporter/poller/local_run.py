"""
Run the poller on your own machine. No Lambda needed.

  python poller/local_run.py --groups /demo/incident-app              # run once
  python poller/local_run.py --groups /demo/incident-app --every 30   # repeat every 30 minutes

It uses the credentials from `aws configure` to read CloudWatch Logs.
The checkpoint is saved in checkpoint.json in the folder where you run the command.
"""
import argparse
import logging
import time

from core import parse_groups, run_once
from stores import FileStore


def main():
    parser = argparse.ArgumentParser(description="CloudWatch error poller (local)")
    parser.add_argument("--groups", required=True, help="comma-separated log group names")
    parser.add_argument("--every", type=int, default=0, help="repeat every N minutes (0 = run once)")
    parser.add_argument("--checkpoint-file", default="checkpoint.json")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    groups = parse_groups(args.groups)
    store = FileStore(args.checkpoint_file)

    while True:
        try:
            result = run_once(store, groups)
            logging.info("Result: %s", result)
        except Exception:
            if args.every <= 0:
                raise  # single run: show the error and stop
            logging.exception("Run failed. Checkpoint not moved, will retry next time.")
        if args.every <= 0:
            break
        time.sleep(args.every * 60)


if __name__ == "__main__":
    main()
