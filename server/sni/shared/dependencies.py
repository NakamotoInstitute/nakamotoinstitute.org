from typing import Annotated

from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from sni.constants import LocaleType
from sni.database import get_db

DB = Annotated[AsyncSession, Depends(get_db)]
Locale = Annotated[LocaleType, Query()]
