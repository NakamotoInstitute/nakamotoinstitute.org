from sni.content.json import JSONImporter
from sni.models import (
    ForumPost,
    ForumPostFile,
    ForumThread,
    ForumThreadFile,
)

from .schemas import ForumPostJSONModel, ForumThreadJSONModel


class ForumThreadImporter(JSONImporter):
    filepath = "data/forum_threads.json"
    item_schema = ForumThreadJSONModel
    model = ForumThread
    file_model = ForumThreadFile
    content_type = "forum_threads"


class ForumPostImporter(JSONImporter):
    filepath = "data/forum_posts.json"
    item_schema = ForumPostJSONModel
    model = ForumPost
    file_model = ForumPostFile
    content_type = "forum_posts"
