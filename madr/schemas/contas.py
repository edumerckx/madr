from pydantic import BaseModel, EmailStr


class ContaSchema(BaseModel):
    username: str
    email: EmailStr
    senha: str


class ContaResponse(BaseModel):
    id: int
    username: str
    email: EmailStr


class ContaList(BaseModel):
    contas: list[ContaResponse]
