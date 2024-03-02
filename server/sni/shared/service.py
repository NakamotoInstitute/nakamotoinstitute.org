from sqlalchemy import select


def get(model, *, db_session, **kwargs):
    return db_session.scalar(select(model).filter_by(**kwargs))


def get_or_create(model, *, db_session, **kwargs):
    instance = get(model, db_session=db_session, **kwargs)
    if instance:
        return instance
    else:
        return model(**kwargs)
