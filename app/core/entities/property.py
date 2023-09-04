from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class RawProperty(BaseModel):
    code: int = Field(example=123)
    company: str = Field(example="Portal imoveis")
    title: str = Field(example="house")
    price: float = Field(example=123.3)
    description: str = Field(example="description")
    neighborhood: str = Field(example="Itoupava Central")
    rooms: int = Field(example=123)
    bathrooms: int = Field(example=123)
    size: float = Field(example=123)
    parking_space: int = Field(example=123)
    modality: str = Field(example="buy")
    property_url: str = Field(example="www.url.com")
    image_url: str = Field(example="www.url.com")
    type: str = Field(example="House")
    number: str = Field(example="123")
    street: Optional[str] = Field(default=None, example="Rua Antonio da Veiga")
    zip_code: Optional[str] = Field(default=None, example="12312")
    created_at: Optional[datetime] = Field(default=None, example=str(datetime.now()))
    updated_at: Optional[datetime] = Field(default=None, example=str(datetime.now()))


class Property(BaseModel):
    code: int = Field(default=None, example=123)
    company_id: int = Field(default=None, example=123)
    title: str = Field(default=None, example="house")
    price: float = Field(default=None, example=123.3)
    description: str = Field(default=None, example="description")
    neighborhood_id: int = Field(default=None, example=123)
    rooms: int = Field(default=None, example=123)
    bathrooms: int = Field(default=None, example=123)
    size: float = Field(default=None, example=123)
    parking_space: int = Field(default=None, example=123)
    modality_id: int = Field(default=None, example=123)
    image_url: str = Field(default=None, example="www.url.com")
    property_url: str = Field(default=None, example="www.url.com")
    type: str = Field(default=None, example="House")
    number: str = Field(default=None, example="123")
    street_id: Optional[int] = Field(default=None, example=123)
    created_at: datetime = Field(default=None, example=str(datetime.now()))
    updated_at: datetime = Field(default=None, example=str(datetime.now()))


class PropertyInDB(Property):
    id: int = Field(example=123)
    is_active: bool = Field(example=True)


class SimpleProperty(BaseModel):
    id: int = Field(example=123)
    code: int = Field(example=123)
    company_id: int = Field(example=123)
    property_url: str = Field(example="www.url.com")
