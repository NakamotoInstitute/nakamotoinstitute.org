from sni.content.json import import_json_data
from sni.content.markdown.renderer import MDRenderer
from sni.models import ForumPost, ForumThread, Quote

from .schemas import ForumPostsJSONModel, ForumThreadsJSONModel


def import_forum_posts(
    db_session, force: bool = False, force_conditions: list[bool] | None = None
):
    def process_item_data(item_data):
        item_data["text"] = MDRenderer.process_html(item_data["text"])
        return item_data

    return import_json_data(
        db_session,
        model=ForumPost,
        schema=ForumPostsJSONModel,
        file_path="data/forum_posts.json",
        force=force or any(force_conditions or []),
        process_item=process_item_data,
    )


def import_forum_threads(
    db_session, force: bool = False, force_conditions: list[bool] | None = None
):
    return import_json_data(
        db_session,
        model=ForumThread,
        schema=ForumThreadsJSONModel,
        file_path="data/forum_threads.json",
        dependent_models=[Quote, ForumPost],
        force=force or any(force_conditions or []),
    )
