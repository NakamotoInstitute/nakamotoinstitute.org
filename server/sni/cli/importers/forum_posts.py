from sni.cli.utils import JSONImporter
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


def import_forum_thread():
    importer = ForumThreadImporter()
    importer.run_import()


class ForumPostImporter(JSONImporter):
    filepath = "data/forum_posts.json"
    item_schema = ForumPostJSONModel
    model = ForumPost
    file_model = ForumPostFile
    content_type = "forum_posts"


def import_forum_post():
    importer = ForumPostImporter()
    importer.run_import()
