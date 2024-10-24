from pydantic import BaseModel


class FiltersPage(BaseModel):
    offset: int = 0
    limit: int = 20
