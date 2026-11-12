"""Places to keep the checkpoint. Each store has get() and set(timestamp_ms)."""
import json
import os


class FileStore:
    """Keeps the checkpoint in a small local JSON file. Good for running on your own machine."""

    def __init__(self, path="checkpoint.json"):
        self.path = path

    def get(self):
        try:
            with open(self.path) as f:
                return int(json.load(f)["checkpoint_ms"])
        except FileNotFoundError:
            return None

    def set(self, timestamp_ms):
        tmp_path = self.path + ".tmp"
        with open(tmp_path, "w") as f:
            json.dump({"checkpoint_ms": timestamp_ms}, f)
        os.replace(tmp_path, self.path)  # replace in one step, so a crash cannot leave half a file


class SsmStore:
    """Keeps the checkpoint in AWS SSM Parameter Store. Used by the Lambda version."""

    def __init__(self, name="/incident-agent/checkpoint"):
        import boto3

        self.name = name
        self.client = boto3.client("ssm")

    def get(self):
        try:
            response = self.client.get_parameter(Name=self.name)
            return int(response["Parameter"]["Value"])
        except self.client.exceptions.ParameterNotFound:
            return None

    def set(self, timestamp_ms):
        self.client.put_parameter(
            Name=self.name, Value=str(timestamp_ms), Type="String", Overwrite=True
        )
