from pydantic import BaseModel


class RomancistaSchema(BaseModel):
    nome: str


class RomancistaResponse(BaseModel):
    id: int
    nome: str


class RomancistaList(BaseModel):
    romancistas: list[RomancistaResponse]
