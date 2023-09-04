"""
Module to load all Environment variables
"""

from pydantic_settings import BaseSettings


class Environment(BaseSettings):
    """
    Environment, add the variable and its type here matching the .env file
    """

    # RABBIT
    RBMQ_HOST: str
    RBMQ_USER: str
    RBMQ_PASS: str
    RBMQ_PORT: int
    RBMQ_EXCHANGE: str
    RBMQ_VHOST: str
    PREFETCH_VALUE: int

    # DATABASE
    DATABASE_URL: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    ENVIRONMENT: str
    DATABASE_MIN_CONNECTIONS: int
    DATABASE_MAX_CONNECTIONS: int

    # REDIS
    REDIS_HOST: str
    REDIS_PORT: str
    TIMED_CACHE: int

    # QUEUES
    PROPERTY_IN_CHANNEL: str
    INACTIVE_PROPERTY_CHANNEL: str
    PORTAL_IMOVEIS_IN_CHANNEL: str
    PORTAL_IMOVEIS_CHARACTERISTICS_CHANNEL: str
    ZAP_IMOVEIS_IN_CHANNEL: str
    ZAP_IMOVEIS_CHARACTERISTICS_CHANNEL: str

    # PORTAIS
    PORTAL_IMOVEIS_URL: str
    ZAP_IMOVEIS_URL: str
    ZAP_IMOVEIS_BASE_URL: str

    class Config:
        """Load config file"""

        env_file = ".env"
        extra='ignore'
