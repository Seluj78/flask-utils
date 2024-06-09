from typing import Optional


class BaseFlaskException(Exception):
    name: Optional[str] = None
    msg: Optional[str] = None
    solution: str = "Try again."
    pass
