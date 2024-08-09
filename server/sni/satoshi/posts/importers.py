from sni.content.json import JSONImporter
from sni.content.markdown.renderer import MDRender
from sni.models import (
    ForumPost,
    ForumPostFile,
    ForumThread,
    ForumThreadFile,
)
from sni.satoshi.quotes.importers import QuoteImporter

from .schemas import ForumPostsJSONModel, ForumThreadsJSONModel


class ForumPostImporter(JSONImporter):
    file_path = "data/forum_posts.json"
    schema = ForumPostsJSONModel
    model = ForumPost
    file_model = ForumPostFile
    content_type = "forum_posts"

    def process_item_data(self, item_data):
        item_data["text"] = MDRender.process_html(item_data["text"])
        return item_data


class ForumThreadImporter(JSONImporter):
    file_path = "data/forum_threads.json"
    schema = ForumThreadsJSONModel
    model = ForumThread
    file_model = ForumThreadFile
    content_type = "forum_threads"
    dependent_importers = [QuoteImporter, ForumPostImporter]
