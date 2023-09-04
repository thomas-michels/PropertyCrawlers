from pydantic import BaseModel, Field


class Modality(BaseModel):

    id: int = Field(example=123)
    name: str = Field(example="Compra")
