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
class Locale(str, Enum):
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
class EmailSource(str, Enum):
    CRYPTOGRAPHY = "cryptography"
    BITCOIN_LIST = "bitcoin-list"
    P2P_RESEARCH = "p2p-research"


@unique
class ForumPostSource(str, Enum):
    P2PFOUNDATION = "p2pfoundation"
    BITCOINTALK = "bitcointalk"


@unique
class Granularity(str, Enum):
    DAY = "DAY"
    MONTH = "MONTH"
    YEAR = "YEAR"
