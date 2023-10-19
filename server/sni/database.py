from typing import List

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from config import ALLOWED_FORMATS, ALLOWED_LOCALES


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


def string_literal_check(lst: List[str]) -> str:
    check = ", ".join([f"'{item}'" for item in lst])
    return f"({check})"


locale_check = string_literal_check(ALLOWED_LOCALES)
format_check = string_literal_check(ALLOWED_FORMATS)
