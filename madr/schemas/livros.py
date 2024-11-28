from pydantic import BaseModel


class LivroSchema(BaseModel):
    ano: int
    titulo: str
    romancista_id: int


class LivroResponse(BaseModel):
    id: int
    ano: int
    titulo: str
    romancista_id: int


class LivroList(BaseModel):
    livros: list[LivroResponse]
