"""
Kombu worker class module
"""

from psycopg_pool import ConnectionPool
from app.core.db import PGConnection
from kombu import Connection
from kombu.mixins import ConsumerMixin
from app.core.configs import get_logger, get_environment
from app.core.exceptions import QueueNotFound
from app.core.dependencies.worker.consumer.manager import QueueManager
from app.core.dependencies.worker.utils.validate_event import payload_conversor
from app.core.dependencies.redis_client import RedisClient
import json

_logger = get_logger(name=__name__)
_env = get_environment()


class KombuWorker(ConsumerMixin):

    def __init__(self, connection: Connection, queues: QueueManager, pool: ConnectionPool):
        self.queues = queues
        self.connection = connection
        self.pool = pool

    def get_consumers(self, Consumer, channel):
        return [
            Consumer(
                queues=self.queues.get_queues(),
                callbacks=[self.process_task],
                prefetch_count=_env.PREFETCH_VALUE
            )
        ]

    def process_task(self, body, message):
        try:
            infos = message.delivery_info
            _logger.info(f"Message received at {infos['routing_key']}")
            callback = self.queues.get_function(infos["routing_key"])
            redis_conn = RedisClient()
            with self.pool.connection() as conn:
                pg_connection = PGConnection(conn=conn)
                callback = callback(pg_connection, redis_conn)
                event_schema = payload_conversor(body)
                if event_schema:
                    if isinstance(event_schema.payload, str):
                        event_schema.payload = json.loads(event_schema.payload)

                    callback.handle(event_schema)

                message.ack()
            
            redis_conn.close()
            _logger.info(f"Message consumed at {event_schema.id}")

        except QueueNotFound:
            _logger.error("Callback not found!")

        except Exception as error:
            _logger.error(f"Error on process_task - {error}")
