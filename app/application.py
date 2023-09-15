from app.core.configs import get_logger
from app.core.db import start_pool, close_pool
from app.core.dependencies.worker import (
    KombuWorker,
    RegisterQueues,
    start_connection_bus
)
import signal

_logger = get_logger(__name__)


class Application:

    def __init__(self) -> None:
        signal.signal(signal.SIGTERM, self.terminate)
        signal.signal(signal.SIGINT, self.terminate)

    def start(self):
        try:
            self.pool = start_pool()

            queues = RegisterQueues.register()

            _logger.info("Starting Worker")

            with start_connection_bus() as conn:
                worker = KombuWorker(conn, queues, self.pool)
                worker.run()

        except KeyboardInterrupt:
            _logger.info("Stopping Worker")
            close_pool(self.pool)
            quit()

    def terminate(self, *args):
        close_pool(self.pool)
        quit()
