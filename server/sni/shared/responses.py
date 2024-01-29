from fastapi import Response


class RSSResponse(Response):
    media_type = "application/rss+xml"


class AtomResponse(Response):
    media_type = "application/atom+xml"
