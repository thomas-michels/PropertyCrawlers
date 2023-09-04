from app.dependencies.worker.utils.event_schema import EventSchema
from app.entities import RawProperty
from app.configs import get_logger
from datetime import datetime

_logger = get_logger(__name__)


def start_characteristics_crawler(message: EventSchema) -> RawProperty:
    try:
        url = message.payload["property_url"]
        code = message.payload["code"]
        company = message.payload["company"]

        data = message.payload["data"]

        modality = data["listing"]["pricingInfos"][0]["businessType"]

        if modality.lower() == "sale":
            modality = "venda"

        else:
            modality = "locação"

        property_type = str(data["listing"]["unitTypes"][0]).upper()

        if property_type == "RESIDENTIAL_ALLOTMENT_LAND":
            property_type = "loteterreno"

        elif property_type == "APARTMENT":
            property_type = "apartamento"

        elif property_type == "HOME":
            property_type = "casa"

        else:
            property_type = property_type.lower()

        image_url = data["link"].get("href", "").replace("/imovel/", "")
        
        if image_url:
            image_url = f"https://resizedimgs.zapimoveis.com.br/fit-in/800x360/named.images.sp/3cc9c0612d716d8631ffde3f7093852d/{image_url}.jpg"

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
            street=data["listing"]["address"]["street"] if data["listing"]["address"].get("street") else None,
            zip_code=data["listing"]["address"]["zipCode"] if data["listing"]["address"]["zipCode"] else None,
            created_at=datetime.fromisoformat(data["listing"]["createdAt"]),
            updated_at=datetime.fromisoformat(data["listing"]["updatedAt"])
        )

        return raw_property

    except Exception as error:
        _logger.error(f"Error: {error}. Data: {message.model_dump_json()}")
        return False
