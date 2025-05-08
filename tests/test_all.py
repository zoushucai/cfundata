from dataclasses import asdict
from pathlib import Path

from cfundata import datapath


def test_paths():
    print("Testing paths...")
    print(datapath)
    # 对每个属性检查
    for i, v in asdict(datapath).items():
        print(f"path: {i} = {v}")
        assert Path(v).exists(), f"Path {i} does not exist: {v}"


if __name__ == "__main__":
    test_paths()
    print("All tests passed!")
