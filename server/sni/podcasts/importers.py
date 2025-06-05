from pathlib import Path

from sni.content.markdown import BasicHandler, create_basic_importer
from sni.database import SessionLocalSync
from sni.models import Episode, Podcast
from sni.shared.service import get

from .schemas import EpisodeMDModel, PodcastMDModel


def import_podcasts(directory: str, force: bool = False):
    with SessionLocalSync() as session:
        importer = create_basic_importer(
            directory=directory,
            session=session,
            canonical_model=Podcast,
            schema=PodcastMDModel,
            force=force,
        )
        importer.run()


class EpisodeHandler(BasicHandler):
    def process_canonical_data(self, canonical_data, fs_record):
        podcast_slug = Path(fs_record["filepath"]).parent.name
        canonical_data["podcast"] = get(
            Podcast, db_session=self.session, slug=podcast_slug
        )
        return canonical_data


def import_episodes(directory: str, force: bool = False):
    with SessionLocalSync() as session:
        importer = create_basic_importer(
            directory=directory,
            session=session,
            canonical_model=Episode,
            handler_class=EpisodeHandler,
            schema=EpisodeMDModel,
            force=force,
        )
        importer.run()
