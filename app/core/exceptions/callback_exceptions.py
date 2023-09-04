"""
Module for callback expeptions
"""
from .base_exceptions import BaseError


class CallbackNotMethod(BaseError):
    """
    Raised when attribute function is not a function
    """

    def __init__(self, detail=None) -> None:
        if not detail:
            detail = "Callback needs to be a function"

        super().__init__(detail)


class FunctionAnnotation(BaseError):
    """
    Raised when annotation of function is not a bool
    """

    def __init__(self, detail=None) -> None:
        if not detail:
            detail = "Annotation is not retuning a boolean"

        super().__init__(detail)


class QueueNotFound(BaseError):
    """
    Raised when queue not found
    """

    def __init__(self, detail=None) -> None:
        if not detail:
            detail = "queue not found"

        super().__init__(detail)


class CallbackAlreadyCreated(BaseError):
    """
    Raise when callback already created
    """

    def __init__(self, detail=None) -> None:
        if not detail:
            detail = "callback already created"

        super().__init__(detail)
