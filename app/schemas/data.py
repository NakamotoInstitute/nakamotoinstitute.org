from pydantic import BaseModel


class AuthorMDSchema(BaseModel):
    name: str
    sort_name: str
