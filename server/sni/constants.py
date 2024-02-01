from enum import Enum, unique
from typing import Literal


class Environment(str, Enum):
    LOCAL = "LOCAL"
    PRODUCTION = "PRODUCTION"

    @property
    def is_debug(self):
        return self in (self.LOCAL,)

    @property
    def is_deployed(self) -> bool:
        return self in (self.PRODUCTION)


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
    PORTUGUESE = "pt"
    RUSSIAN = "ru"
    CHINESE_SIMPLIFIED = "zh-cn"


LocaleType = Literal[
    Locales.ARABIC.value,
    Locales.GERMAN.value,
    Locales.ENGLISH.value,
    Locales.SPANISH.value,
    Locales.PERSIAN.value,
    Locales.FINNISH.value,
    Locales.FRENCH.value,
    Locales.HEBREW.value,
    Locales.ITALIAN.value,
    Locales.KOREAN.value,
    Locales.PORTUGUESE.value,
    Locales.RUSSIAN.value,
    Locales.CHINESE_SIMPLIFIED.value,
]


@unique
class DocumentFormats(Enum):
    PDF = "pdf"
    EPUB = "epub"
    MOBI = "mobi"
    TXT = "txt"
