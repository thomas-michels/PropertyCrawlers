"""
    Module for base Exception
"""


class BaseError(Exception):
    def __init__(self, detail) -> None:
        self.detail = detail

    def dict(self):
        return {"detail": self.detail}
