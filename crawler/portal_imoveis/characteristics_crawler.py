from app.dependencies.worker.utils.event_schema import EventSchema
from app.entities import RawProperty
from app.configs import get_logger
from bs4 import BeautifulSoup, Comment
import requests
import re

_logger = get_logger(__name__)


def start_characteristics_crawler(message: EventSchema) -> RawProperty:
    try:
        url = message.payload["property_url"]
        code = message.payload["code"]
        company = message.payload["company"]

        page = requests.get(url=url)
        page.raise_for_status()

        html = page.text

        soup = BeautifulSoup(html, 'html.parser')

        image = soup.find("img", class_="thumb w-full lazy").attrs["data-src"]
        title = soup.find("h1", class_="title title-1 title-page").next
        room = soup.find("i", class_="fas fa-bed")

        if room:
            room = room.next.strip()

        else:
            room = 0

        bathroom = soup.find("i", class_="fas fa-bath")

        if bathroom:
            bathroom = bathroom.next.strip()

        else:
            bathroom = 0

        parking_space = soup.find("i", class_="fas fa-warehouse")

        if parking_space:
            parking_space = parking_space.next.strip()

        else:
            parking_space = 0

        size = soup.find("i", class_="fas fa-ruler")

        if size:
            size = size.next.strip()
            cleaned_size = re.sub(r'[^\d.]', '', size)

        else:
            cleaned_size = 0

        raw_type = re.search(r"/([^/]+)/([^/]+)", url)
        if raw_type:
            type = raw_type.group(2)
        else:
            type = "" 

        modality = soup.find("span", class_="type venda")

        if not modality:
            modality = soup.find("span", class_="type locacao").next

        else:
            modality = modality.next

        description = soup.find("div", class_="col-lg-8 col-md-8 col-sm-7 col-xs-12")

        if description:
            description = description.text.strip()

        else:
            description = ""

        price = soup.find("span", "title title-2 price")

        if price:
            raw_price = price.next.strip()

            try:
                price = re.sub(r'[^\d,]', '', raw_price)
                price = float(price.replace(',', '.'))

            except Exception:
                raw_price = raw_price.split("/")[0]
                price = re.sub(r'[^\d,]', '', raw_price)
                price = float(price.replace(',', '.'))

        else:
            price = 0

        comments = soup.find_all(text=lambda text: isinstance(text, Comment))

        street = ""
        number = ""
        neighborhood = ""

        for comment in comments:
            formated = str(comment).lower()
            if formated.__contains__(" rua ") or formated.__contains__(" r "):
                # arrumar essa parte nao ta vindo neighborhood as vezes
                street = formated
                neighborhood = comment.next.strip()

        if street:
            padrao_remover_r = r'^\s*r\s*(rua)?\s*TRV\s+(.*?)\s*,\s*s/n°'
            padrao_remover_hifen = r'\s*-\s*$'

            street = street.replace("ROD ", "rua ")
            street = street.replace("AL ", "rua ")
            street = street.replace("AER ", "rua ")
            street = street.replace("AV ", "rua ")

            string = re.sub(padrao_remover_r, '', street, flags=re.IGNORECASE)
            string = re.sub(padrao_remover_hifen, '', string)
            strings = re.split(r'\s*,\s*', string)

            if strings:
                street = strings[0]
                number = strings[1]

            number = number.replace(".", "")

            if not number.isdigit():
                number = ""

        raw_property = RawProperty(
            code=code,
            company=company,
            title=title,
            price=price,
            description=description,
            neighborhood=neighborhood,
            rooms=int(room),
            bathrooms=int(bathroom),
            size=float(cleaned_size),
            parking_space=int(parking_space),
            modality=modality,
            property_url=url,
            image_url=image,
            type=type,
            number=number,
            street=street
        )

        return raw_property

    except Exception as error:
        _logger.error(f"Error: {error}. Data: {message.model_dump_json()}")
        return False
