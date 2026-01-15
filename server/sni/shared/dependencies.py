from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sni.constants import LocaleType
from sni.database import get_db

DB = Annotated[AsyncSession, Depends(get_db)]
Locale = Annotated[LocaleType, "en"]
