import hashlib
import json
from pathlib import Path
from typing import Union


def calculate_sha256(file_path: Union[str, Path]) -> str:
    """
    Calculate the sha256 hash of a file.
    """
    sha256_hash = hashlib.sha256()
    with open(str(file_path), "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


if __name__ == "__main__":
    # 不计算_开头的文件和.py 文件
    data = Path("src/cfundata/data")
    jsonname = "sha256.json"
    use_suffix = [".pt", ".onnx", ".json", ".bin", ".parquet", ".ttc", ".ttf"]
    exclude = [jsonname, "README.md", "LICENSE"]
    # 筛选需要的文件
    files = [f for f in data.rglob("*") if f.is_file() and f.suffix in use_suffix]
    # 排除以. 或者 _ 开头的文件
    files = [f for f in files if not f.name.startswith((".", "_"))]
    # 排除指定文件
    files = [f for f in files if f.name not in exclude]

    result = []
    baseURL = "https://modelscope.cn/datasets/zscmmm/cfundata/resolve/master/"
    for file in files:
        sha256 = calculate_sha256(file)
        name = file.name
        result.append(
            {
                "name": name,
                "url": baseURL + file.parent.name + "/" + name,
                "sha256": sha256,
            }
        )
    # 写为 json 文件
    # print(result)
    json_path = jsonname  # 手动移动到目标目录 data / jsonname
    result = sorted(result, key=lambda x: x["name"])

    with open(str(json_path), "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False, sort_keys=True)

    print(f"{jsonname} saved to {json_path}")
