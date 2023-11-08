import sqlalchemy as sa

from sni.extensions import db


def model_exists(model_class):
    engine = db.get_engine()
    insp = sa.inspect(engine)
    return insp.has_table(model_class.__tablename__)


def get(model, **kwargs):
    return db.session.scalar(db.select(model).filter_by(**kwargs))


# See if object already exists for uniqueness
def get_or_create(model, **kwargs):
    instance = get(model, **kwargs)
    if instance:
        return instance
    else:
        return model(**kwargs)
