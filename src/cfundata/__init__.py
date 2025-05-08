from .utils import initialize_datapath

# 初始化全局变量
datapath = initialize_datapath()


__all__ = [
    "datapath",
]
