from pydantic import BaseModel


class SlugParamResponse(BaseModel):
    slug: str
    locale: str
