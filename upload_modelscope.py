import os

from modelscope.hub.api import HubApi

api = HubApi()
token = os.getenv("MS_TOKEN")
assert token, "Please set MS_TOKEN in your environment variables."

api.login(token)


owner_name = "zscmmm"
dataset_name = "cfundata"

api.upload_folder(
    repo_id=f"{owner_name}/{dataset_name}",
    folder_path="src/cfundata",
    commit_message="upload dataset folder to repo",
    repo_type="dataset",
    allow_patterns=["data/*"],
    # allow_patterns=["*.ttc", "*.parquet", "*.onnx", "*.pt", "*.json"],
    ignore_patterns=["*/_*", "*.py"],
)

print("Upload completed!")
