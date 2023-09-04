from pydantic import BaseModel, Field


class Company(BaseModel):
    id: int = Field(example=123)
    name: str = Field(example="PORTAL IMOVEIS")
