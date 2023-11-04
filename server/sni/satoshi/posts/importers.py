from sni.content.importers import JSONImporter
from sni.satoshi.posts.models import (
    ForumPost,
    ForumPostFile,
    ForumThread,
    ForumThreadFile,
)
from sni.satoshi.posts.schemas import ForumPostJSONModel, ForumThreadJSONModel


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
