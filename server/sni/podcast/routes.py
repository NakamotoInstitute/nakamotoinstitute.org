from typing import List

from sni import db
from sni.models import Episode
from sni.utils.decorators import response_model

from . import bp
from .schemas import EpisodeModel


@bp.route("/", methods=["GET"])
@response_model(List[EpisodeModel])
def get_episodes():
    episodes = db.session.scalars(
        db.select(Episode).order_by(Episode.date.desc())
    ).all()
    return episodes


@bp.route("/<string:slug>", methods=["GET"])
@response_model(EpisodeModel)
def get_episode(slug):
    episode = db.first_or_404(db.select(Episode).filter_by(slug=slug))
    return episode
