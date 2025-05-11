"""使用pooch模块来下载和缓存数据文件

优点：
    在本地下载并缓存您的数据文件（因此只需下载一次）
    通过验证加密哈希，确保运行代码的每个人都具有相同版本的数据文件。
    ....

参考：
    [https://www.fatiando.org/pooch/latest/about.html](https://www.fatiando.org/pooch/latest/about.html)
"""

import importlib.resources as pkg_resources
import json
from dataclasses import dataclass
from pathlib import Path

import pooch


def _read_json(path: Path | str) -> list[dict]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


# 5. 构建数据类
@dataclass(frozen=True)
class DataPath:
    """数据路径类，包含该包的所有数据文件的路径

    该类用于存储数据文件的路径，提供了对数据文件的访问方式。
    该类的属性是不可变的，使用时请直接访问属性。
    默认会自动下载到缓存目录中，缓存目录中.由pooch模块管理。

    Attributes:
        DX_DET_ONNX (Path): DX检测模型的ONNX文件路径
        DX_CLS_ONNX (Path): DX分类模型的ONNX文件路径
        DX_DET_PT (Path): DX检测模型的PyTorch文件路径
        DX_CLS_PT (Path): DX分类模型的PyTorch文件路径
        FONT_SIMSUN (Path): SimSun字体文件路径
        FREQUENCY (Path): 频率数据文件路径
        FREQUENCY2 (Path): 频率数据文件路径2
        SFZ_DET_ONNX (Path): sfz检测模型的ONNX文件路径, 大约7000张图片训练的，返回四个类别框，0,3代表反面（国徽），1,2代表正面(头像)

    !!! note
        DX_* 的文件,是dx的点选和语序yzm训练而来的, 大约采用了1.4w张图片训练的.
        模型采用的是yolov11训练而来的, 目标检查和分类模型都含有两种格式的模型, 分别是pt和onnx格式,
        有些时候装ultralytics太慢, 使用onnx模型就快很多。

    !!! note
        SimSun字体文件是用于显示中文的字体文件, 该文件是从Windows系统中提取的, 可能会有版权问题,
        请在使用时注意版权问题。

    频率数据参考: [zoushucai/textfrequency](https://github.com/zoushucai/textfrequency)


    Example:
        ```python
        from cfundata import cdata
        # cdata 是一个DataPath对象, 包含了所有数据文件的路径
        print(cdata.DX_DET_ONNX)
        print(cdata.DX_CLS_ONNX)
        print(cdata)
        ```
    """

    DX_DET_ONNX: Path
    DX_CLS_ONNX: Path
    DX_DET_PT: Path
    DX_CLS_PT: Path
    FONT_SIMSUN: Path
    FREQUENCY: Path
    FREQUENCY2: Path
    SFZ_DET_ONNX: Path


def initialize_datapath() -> DataPath:
    """初始化数据路径

    该函数用于初始化数据路径, 包括下载数据文件和缓存数据文件.
    该函数会自动检测数据文件是否存在, 如果不存在, 则会自动下载数据文件.

    Args:
        None

    Returns:
        DataPath: 数据路径对象, 包含所有数据文件的路径.
    """
    try:
        import tqdm

        show_bar = True
    except ImportError:
        show_bar = False

    # 1. 读取资源描述文件
    sha256_path = pkg_resources.files("cfundata.data").joinpath("sha256.json")
    resources = _read_json(sha256_path)

    # 2. 构造 registry 和 urls
    registry = {r["name"]: r["sha256"] for r in resources}
    urls = {r["name"]: r["url"] for r in resources}

    # 3. 初始化 pooch
    pup = pooch.create(
        path=pooch.os_cache("cfundata"),
        base_url="",  # 每个文件有独立 URL
        registry=registry,
        urls=urls,
    )

    # 4. 加载路径：优先从包内加载，失败则从缓存中下载, 且强制返回Path对象
    paths: dict[str, Path] = {}
    for name in registry:
        package_path = pkg_resources.files("cfundata.data").joinpath(name)
        try:
            # 使用 with as_file
            with pkg_resources.as_file(package_path) as local_path:
                p = (
                    local_path
                    if local_path.exists()
                    else pup.fetch(name, progressbar=show_bar)
                )
                paths[name] = Path(p)
        except Exception:
            paths[name] = Path(pup.fetch(name, progressbar=show_bar))

    # 5. 显式验证需要的关键文件存在（防止 KeyError）
    field_map = {
        "DX_DET_ONNX": "dx_det.onnx",
        "DX_CLS_ONNX": "dx_cls.onnx",
        "DX_DET_PT": "dx_det.pt",
        "DX_CLS_PT": "dx_cls.pt",
        "FONT_SIMSUN": "simsun.ttc",
        "FREQUENCY": "frequency.parquet",
        "FREQUENCY2": "frequency2.parquet",
        "SFZ_DET_ONNX": "sfz_det.onnx",
    }
    missing = [fname for fname in field_map.values() if fname not in paths]
    if missing:
        raise ValueError(f"Missing required files: {missing}")

    # 6 自动构建 DataPath 对象
    return DataPath(**{field: paths[filename] for field, filename in field_map.items()})
