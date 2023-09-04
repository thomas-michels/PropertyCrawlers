from psycopg_pool import ConnectionPool
from app.core.configs import get_environment, get_logger

_env = get_environment()
_logger = get_logger(__name__)


def start_pool() -> ConnectionPool:
    _logger.info("Openning connection pool")
    pool = ConnectionPool(
        conninfo=(
            f"host={_env.DATABASE_HOST} "
            f"port={_env.DATABASE_PORT} "
            f"user={_env.DATABASE_USER} "
            f"password={_env.DATABASE_PASSWORD} "
            f"dbname={_env.DATABASE_NAME}"),
        min_size=_env.DATABASE_MIN_CONNECTIONS,
        max_size=_env.DATABASE_MAX_CONNECTIONS
    )
    pool.open()
    return pool


def close_pool(pool: ConnectionPool):
    _logger.info("Closing connection pool")
    pool.close()
