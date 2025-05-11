from .utils import initialize_datapath

# 初始化全局变量
cdata = initialize_datapath()


__all__ = [
    "cdata",
]
