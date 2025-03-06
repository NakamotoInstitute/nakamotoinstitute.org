from abc import ABC, abstractmethod

from sni.config import settings


class BaseURLGenerator(ABC):
    def __init__(self, locale_str: str) -> None:
        if locale_str == "en":
            self.base_url = settings.BASE_URL
        else:
            self.base_url = f"{settings.BASE_URL}/{locale_str}"
        self.base_cdn_url = settings.CDN_BASE_URL

    @property
    @abstractmethod
    def index(self) -> str:
        pass

    @property
    def donate(self) -> str:
        return f"{self.base_url}/donate/"
