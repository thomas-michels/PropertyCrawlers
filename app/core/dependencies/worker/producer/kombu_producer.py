
from kombu.mixins import Producer
from app.core.dependencies.worker.utils import start_connection_bus, connect_on_exchange
from app.core.dependencies.worker.utils.event_schema import EventSchema
from app.core.configs import get_logger, get_environment
from app.core.db.repositories.event_repository import EventRepository
from app.core.db import DBConnection

_env = get_environment()
_logger = get_logger(name=__name__)


class KombuProducer:
    """
    Class for Producer to send messages in queues
    """

    @classmethod
    def send_messages(cls, conn: DBConnection, message: EventSchema) -> bool:
        """
        Method to send messages

        :param message: EventSchema

        :return: bool
        """
        try:
            with start_connection_bus() as bus_conn:
                producer = Producer(bus_conn)
                producer.publish(
                    body=message.model_dump(),
                    exchange=connect_on_exchange(_env.RBMQ_EXCHANGE),
                    routing_key=message.sent_to,
                )

            _logger.info(f"Sent message to {message.sent_to}")

            event_repository = EventRepository(connection=conn)
            event_repository.insert(event=message)

            return True

        except Exception as error:
            _logger.error(
                f"Error on send message to {message.sent_to}. Error: {error}"
            )
