from app.core.db import DBConnection
from app.core.dependencies.redis_client import RedisClient
from app.core.dependencies.worker.utils.event_schema import EventSchema
from app.crawlers.base_crawler import Crawler
from app.core.entities import RawProperty
from app.core.configs import get_logger, get_environment
from datetime import datetime
from app.core.dependencies.worker import KombuProducer
from time import sleep
from random import randint
import requests
from requests.exceptions import HTTPError
import pendulum


_logger = get_logger(__name__)
_env = get_environment()


class ZapImoveisCrawlerCharacteristics(Crawler):

    def __init__(self, conn: DBConnection, redis_conn: RedisClient) -> None:
        super().__init__(conn, redis_conn)
    
    def handle(self, message: EventSchema) -> bool:
        try:
            url = message.payload["property_url"]
            company = message.payload["company"]

            data = message.payload.get("data")
            if not data:
                sleep(randint(3, 7))
                try:
                    response = requests.get(url=url)
                    response.raise_for_status()

                except HTTPError:
                    new_message = EventSchema(
                        id=message.id,
                        origin=message.sent_to,
                        sent_to=_env.INACTIVE_PROPERTY_CHANNEL,
                        payload=message.payload,
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                    return KombuProducer.send_messages(conn=self.conn, message=new_message)

            code = message.payload["code"]

            modality = data["listing"]["pricingInfos"][0]["businessType"]

            if modality.lower() == "sale":
                modality = "venda"

            else:
                modality = "locação"

            property_type = str(data["listing"]["unitTypes"][0]).upper()

            if property_type == "RESIDENTIAL_ALLOTMENT_LAND" or property_type == "ALLOTMENT_LAND":
                property_type = "loteterreno"

            elif property_type == "APARTMENT":
                property_type = "apartamento"

            elif property_type == "HOME" or property_type == "FARM":
                property_type = "casa"

            else:
                property_type = property_type.lower()

            image_url = data["link"].get("href", "").replace("/imovel/", "")
            
            if image_url:
                image_url = f"https://resizedimgs.zapimoveis.com.br/fit-in/800x360/named.images.sp/3cc9c0612d716d8631ffde3f7093852d/{image_url}.jpg"

            if data["listing"]["address"].get("street"):
                street = data["listing"]["address"]["street"]
                street = street.replace("ROD ", "")
                street = street.replace("AL ", "")
                street = street.replace("AER ", "")
                street = street.replace("AV ", "")
                street = street.replace(" r ", "")
                street = street.replace("rua ", "")

            else:
                street = None

            created_at = pendulum.parse(data["listing"]["createdAt"])
            updated_at = pendulum.parse(data["listing"]["updatedAt"])

            raw_property = RawProperty(
                code=code,
                company=company,
                title=data["listing"]["title"],
                price=float(data["listing"]["pricingInfos"][0].get("price", 0)) if data["listing"]["pricingInfos"] else 0,
                description=data["listing"]["description"],
                neighborhood=data["listing"]["address"]["neighborhood"],
                rooms=int(data["listing"]["bedrooms"][0]) if data["listing"]["bedrooms"] else 0,
                bathrooms=int(data["listing"]["bathrooms"][0]) if data["listing"]["bathrooms"] else 0,
                size=float(data["listing"]["usableAreas"][0]) if data["listing"]["usableAreas"] else 0,
                parking_space=int(data["listing"]["parkingSpaces"][0]) if data["listing"]["parkingSpaces"] else 0,
                modality=modality,
                property_url=url,
                image_url=image_url,
                type=property_type,
                number="",
                street=street,
                zip_code=data["listing"]["address"]["zipCode"] if data["listing"]["address"]["zipCode"] else None,
                created_at=created_at,
                updated_at=updated_at
            )

            new_message = EventSchema(
                id=message.id,
                origin=message.sent_to,
                sent_to=_env.PROPERTY_IN_CHANNEL,
                payload=raw_property.model_dump_json(),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

            _logger.info(f"New property: {raw_property.property_url}")

            return KombuProducer.send_messages(conn=self.conn, message=new_message)

        except Exception as error:
            _logger.error(f"Error: {error}. Data: {message.model_dump_json()}")
            return False
