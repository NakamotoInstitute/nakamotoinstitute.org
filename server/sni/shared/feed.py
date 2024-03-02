from enum import Enum


class FeedFormat(str, Enum):
    rss = "rss"
    atom = "atom"
