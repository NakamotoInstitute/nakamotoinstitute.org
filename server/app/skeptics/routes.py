from typing import List

from app import db
from app.models import Skeptic
from app.utils.decorators import response_model

from . import bp
from .schemas import SkepticModel


@bp.route("/", methods=["GET"])
@response_model(List[SkepticModel])
def get_skeptics():
    skeptics = db.session.scalars(db.select(Skeptic).order_by(Skeptic.date)).all()
    return skeptics
