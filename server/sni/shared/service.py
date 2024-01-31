from sqlalchemy import select


async def get(model, *, db_session, **kwargs):
    return await db_session.scalar(select(model).filter_by(**kwargs))


async def get_or_create(model, *, db_session, **kwargs):
    instance = await get(model, db_session=db_session, **kwargs)
    if instance:
        return instance
    else:
        return model(**kwargs)
