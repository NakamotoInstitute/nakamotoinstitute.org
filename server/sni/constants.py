from enum import Enum, StrEnum, unique
from typing import Literal

STATIC_ROUTE = "/static"


class Environment(StrEnum):
    LOCAL = "LOCAL"
    PRODUCTION = "PRODUCTION"

    @property
    def is_debug(self) -> bool:
        return self in (self.LOCAL,)

    @property
    def is_deployed(self) -> bool:
        return self in (self.PRODUCTION,)


@unique
class Locale(StrEnum):
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


@unique
class EmailSource(StrEnum):
    CRYPTOGRAPHY = "cryptography"
    BITCOIN_LIST = "bitcoin-list"
    P2P_RESEARCH = "p2p-research"


@unique
class ForumPostSource(StrEnum):
    P2PFOUNDATION = "p2pfoundation"
    BITCOINTALK = "bitcointalk"


@unique
class Granularity(StrEnum):
    DAY = "DAY"
    MONTH = "MONTH"
    YEAR = "YEAR"
