import logging
from contextlib import contextmanager

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = async_sessionmaker(bind=engine)

engine_sync = create_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocalSync = sessionmaker(autocommit=False, autoflush=False, bind=engine_sync)


async def get_db():
    async with SessionLocal() as session:
        yield session


@contextmanager
def session_scope():
    db_session = SessionLocalSync()
    try:
        yield db_session
        db_session.commit()
    except Exception as e:
        logging.error(f"Error during update: {e}")
        db_session.rollback()
        raise
    finally:
        db_session.close()


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )
