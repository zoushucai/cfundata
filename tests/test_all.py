from dataclasses import asdict
from pathlib import Path

from cfundata import cdata


def test_paths():
    print("Testing paths...")
    print(cdata)
    # 对每个属性检查
    # 每个属性都是一个Path对象
    for name, path in asdict(cdata).items():
        print(f"path: {name} = {path}")
        assert isinstance(path, Path), f"{name} is not a Path object: {path}"
        assert Path(path).exists(), f"Path {name} does not exist: {path}"


if __name__ == "__main__":
    test_paths()
    print("All tests passed!")
