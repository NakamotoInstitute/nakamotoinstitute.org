from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from sni.models import Skeptic


def get_all(*, db_session: Session) -> List[Skeptic]:
    return db_session.scalars(select(Skeptic).order_by(Skeptic.date)).all()
