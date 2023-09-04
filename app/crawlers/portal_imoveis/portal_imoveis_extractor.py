from bs4 import BeautifulSoup
import requests
from time import sleep
from random import randint
from app.core.configs import get_environment, get_logger
from app.core.dependencies.worker.utils.event_schema import EventSchema
from app.core.dependencies.worker.producer import KombuProducer
from app.core.db import RawPGConnection
from uuid import uuid4
from datetime import datetime


_env = get_environment()
_logger = get_logger(__name__)

def start_portal_imoveis_extractor():

    _logger.info("Starting Portal imoveis crawler")
    url = _env.PORTAL_IMOVEIS_URL
    page_size = 16

    page = requests.get(url=url)
    html = page.text

    soup = BeautifulSoup(html, 'html.parser')

    raw_quantity = soup.find("h1", class_="title title-1 title-page")
    raw_quantity = raw_quantity.next
    quantity = int(raw_quantity[:-19])

    _logger.info(f"{quantity} properties found")

    pages = quantity // page_size

    with RawPGConnection() as conn:

        for i in range(1, pages + 1):
            time_sleep = randint(5, 15)
            _logger.info(f"Sleeping: {time_sleep}")
            sleep(time_sleep)

            offset = page_size * i
            url = f"{_env.PORTAL_IMOVEIS_URL}?page={offset}"

            page = requests.get(url=url)
            html = page.text

            soup = BeautifulSoup(html, 'html.parser')

            buttons = soup.find_all("a", class_="btn btn-primary")

            if buttons:
                for button in buttons:
                    url = button.attrs['href']
                    _logger.info(f"New property found: {url}")

                    code = int(url.split("/")[-1])

                    event = EventSchema(
                        id=str(uuid4()),
                        origin="PORTAL_IMOVEIS",
                        sent_to=_env.PORTAL_IMOVEIS_IN_CHANNEL,
                        payload={
                            "property_url": url,
                            "company": "portal_imoveis",
                            "code": code
                        },
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )

                    KombuProducer.send_messages(conn=conn, message=event)
