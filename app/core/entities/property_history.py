from pydantic import BaseModel, Field
from datetime import datetime


class PropertyHistory(BaseModel):

    property_id: int = Field(example=123)
    price: float = Field(example=123.1)


class PropertyHistoryInDB(PropertyHistory):
    id: int = Field(example=123)
    created_at: datetime = Field(example=str(datetime.now()))
    updated_at: datetime = Field(example=str(datetime.now()))
