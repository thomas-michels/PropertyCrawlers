from typing import Optional
from pydantic import BaseModel, Field


class Street(BaseModel):

    id: int = Field(example=123)
    name: str = Field(example="Antonio da Veiga")
    neighborhood_id: int = Field(example=123)
    zip_code: Optional[str] = Field(default=None, example=123)
