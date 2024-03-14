from typing import IO


def open_r(path: str, **args) -> IO[str]:
    if isinstance(path, str):
        return open(path, "r", encoding="utf-8", **args)
    raise f"type error：must str, but got a {type(path)}"


def open_w(path: str, **args) -> IO[str]:
    if isinstance(path, str):
        return open(path, "w", encoding="utf-8", **args)
    raise f"type error：must str, but got a {type(path)}"


def open_a(path: str, **args) -> IO[str]:
    if isinstance(path, str):
        return open(path, "a", encoding="utf-8", **args)
    raise f"type error：must str, but got a {type(path)}"
