import tempfile
import os
from typing import Optional


class TmpFile:
    """
    临时文件封装

    实例属性:
    - path: 临时文件路径
    - keep: 结束后是否保留该文件
    - fd: 临时文件描述符

    用法:

        >>> with TmpFile() as tmp:
        ...     # ...
        ...     with tmp.open("w") as f:
        ...         ...
        ...     # ...
    """
    def __init__(
        self,
        prefix: Optional[str] = None, suffix: Optional[str] = None,
        keep: bool = False
    ) -> None:
        """
        初始化一个临时文件

        参数:
        - prefix: 自定义临时文件前缀
        - suffix: 自定义临时文件后缀
        - keep: 结束后是否保留该文件
        """
        self.fd, self.path = tempfile.mkstemp(prefix=prefix, suffix=suffix)
        self.keep = keep

    def __enter__(self):
        return self

    def __exit__(self, *_) -> None:
        if not self.keep:
            os.remove(self.path)

    def open(self, *args, **kwargs):
        """
        打开该文件

        除文件路径外，其余参数详见内置函数 `open()`
        """
        return open(self.path, *args, **kwargs)