from sni.content.importers import MarkdownImporter
from sni.models import Episode

from .schemas import EpisodeMDModel


class EpisodeImporter(MarkdownImporter):
    directory_path = "content/podcast"
    content_type = "Episode"
    model = Episode
    schema = EpisodeMDModel
    content_key = "episode"


def import_episode():
    episode_importer = EpisodeImporter()
    episode_importer.run_import()
