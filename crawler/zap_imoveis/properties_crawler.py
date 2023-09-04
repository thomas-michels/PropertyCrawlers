import requests
from time import sleep
from random import randint
from app.configs import get_environment, get_logger
from app.dependencies.worker.utils.event_schema import EventSchema
from app.dependencies.worker.producer import KombuProducer
from app.db import RawPGConnection
from uuid import uuid4
from datetime import datetime


_env = get_environment()
_logger = get_logger(__name__)

def start_crawler():
    
    _logger.info("Starting Zap imoveis crawler")
    offset = -15
    page_size = 15
    headers = {
        "domain": ".zapimoveis.com.br",
        "X-Domain": ".zapimoveis.com.br",
        "Cookie": "__cfruid=72ab1a4d676a1b254f1c31fcdceee752d70655ef-1692746103",
        "User-Agent": "PostmanRuntime/7.32.3"
    }
    error_count = 0

    size = 10000
    percent = 100 / size
    last_percent = 1
    i = -1

    with RawPGConnection() as conn:
        while offset <= 10000 or error_count < 5:
            time_sleep = randint(5, 15)
            _logger.info(f"Sleeping: {time_sleep}")
            sleep(time_sleep)

            try:
                offset += page_size

                current_percent: float = i * percent
                if current_percent >= last_percent:
                    _logger.info(f"ZAP IMOVEIS EXTRACTION: {round(current_percent, 2)}%")
                    last_percent += 1

                url = _env.ZAP_IMOVEIS_URL.replace("$$OFFSET", str(offset))

                page = requests.request("GET", url, headers=headers)
                page.raise_for_status()

                json = page.json()

            except Exception as error:
                _logger.error(f"Error: {str(error)}. Status_code: {page.status_code}")
                error_count += 1

                if error_count == 5:
                    _logger.fatal(f"Stopping crawler because had too many errors to search properties")

                continue

            for item in json["search"]["result"]["listings"]:
                try:
                    raw_property = item["listing"]

                    code = int(raw_property["id"])
                    property_url = f"{_env.ZAP_IMOVEIS_BASE_URL}{item['link']['href']}"
                    _logger.info(f"ZAP Imoveis: New property found: {property_url}")

                    data = {
                            "property_url": property_url,
                            "company": "zap_imoveis",
                            "code": code,
                            "data": item,
                            "is_new_property": True
                    }

                    event = EventSchema(
                        id=str(uuid4()),
                        origin="zap_imoveis",
                        sent_to=_env.PROPERTY_IN_CHANNEL,
                        payload=data,
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )

                    KombuProducer.send_messages(conn=conn, message=event)

                except Exception as error:
                    _logger.error(f"Error: {str(error)}")
