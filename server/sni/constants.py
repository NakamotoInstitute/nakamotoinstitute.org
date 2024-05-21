from enum import Enum, unique
from typing import Literal

STATIC_ROUTE = "/static"


class Environment(str, Enum):
    LOCAL = "LOCAL"
    PRODUCTION = "PRODUCTION"

    @property
    def is_debug(self) -> bool:
        return self in (self.LOCAL,)

    @property
    def is_deployed(self) -> bool:
        return self in (self.PRODUCTION,)


@unique
class Locales(str, Enum):
    ARABIC = "ar"
    GERMAN = "de"
    ENGLISH = "en"
    SPANISH = "es"
    PERSIAN = "fa"
    FINNISH = "fi"
    FRENCH = "fr"
    HEBREW = "he"
    ITALIAN = "it"
    KOREAN = "ko"
    PORTUGUESE_BRAZILIAN = "pt-br"
    RUSSIAN = "ru"
    TURKISH = "tr"
    VIETNAMESE = "vi"
    CHINESE_SIMPLIFIED = "zh-cn"


LocaleType = Literal[
    "ar",
    "de",
    "en",
    "es",
    "fa",
    "fi",
    "fr",
    "he",
    "it",
    "ko",
    "pt-br",
    "ru",
    "tr",
    "vi",
    "zh-cn",
]


@unique
class DocumentFormats(Enum):
    PDF = "pdf"
    EPUB = "epub"
    MOBI = "mobi"
    TXT = "txt"
