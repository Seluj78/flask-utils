from typing import Optional


class _BaseFlaskException(Exception):
    name: Optional[str] = None
    msg: Optional[str] = None
    solution: Optional[str] = "Try again."
