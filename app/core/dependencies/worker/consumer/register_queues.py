"""
    Module for register queues
"""
from .manager import QueueManager
from app.core.configs import get_logger, get_environment
from app.crawlers.portal_imoveis import PortalImoveisCrawlerIn, PortalImoveisCrawlerCharacteristics
from app.crawlers.zap_imoveis import ZapImoveisCrawlerIn, ZapImoveisCrawlerCharacteristics

_logger = get_logger(name=__name__)
_env = get_environment()


class RegisterQueues:
    """
    RegisterQueues class
    """

    @staticmethod
    def register() -> QueueManager:
        _logger.info("Starting QueueManager")
        queue_manager = QueueManager()

        queue_manager.register_callback(
            _env.PORTAL_IMOVEIS_IN_CHANNEL, PortalImoveisCrawlerIn
        )

        queue_manager.register_callback(
            _env.PORTAL_IMOVEIS_CHARACTERISTICS_CHANNEL, PortalImoveisCrawlerCharacteristics
        )

        queue_manager.register_callback(
            _env.ZAP_IMOVEIS_IN_CHANNEL, ZapImoveisCrawlerIn
        )

        queue_manager.register_callback(
            _env.ZAP_IMOVEIS_CHARACTERISTICS_CHANNEL, ZapImoveisCrawlerCharacteristics
        )

        _logger.info("All queues started")

        return queue_manager
