from .base_exceptions import BaseError


class RedisNotConnected(BaseError):
    """
    Raised when some error happen to connect on redis
    """

    def __init__(self, detail=None) -> None:
        if not detail:
            detail = "some error happen to connect on redis"

        super().__init__(detail)
