from typing import List

from sqlalchemy import exists, or_, select
from sqlalchemy.orm import Session, aliased

from sni.config import LocaleType
from sni.models import (
    Author,
    BlogPost,
    BlogPostTranslation,
    Document,
    DocumentTranslation,
    blog_post_authors,
    document_authors,
)


def get(slug: str, *, db_session: Session) -> Author:
    return db_session.scalar(select(Author).filter_by(slug=slug))


def get_all(*, db_session: Session) -> List[Author]:
    return db_session.scalars(select(Author)).all()


def get_all_by_locale(
    *, db_session: Session, locale: LocaleType = "en"
) -> List[Author]:
    DocumentTranslationAlias = aliased(DocumentTranslation, flat=True)
    BlogPostTranslationAlias = aliased(BlogPostTranslation, flat=True)

    return db_session.scalars(
        select(Author)
        .outerjoin(document_authors)
        .outerjoin(Document)
        .outerjoin(DocumentTranslationAlias)
        .outerjoin(blog_post_authors)
        .outerjoin(BlogPost)
        .outerjoin(BlogPostTranslationAlias)
        .filter(
            or_(
                DocumentTranslationAlias.locale == locale,
                BlogPostTranslationAlias.locale == locale,
            )
        )
        .order_by(Author.sort_name)
        .distinct()
    ).all()


def get_author_locales(*, db_session: Session):
    return set(
        db_session.scalars(
            select(BlogPostTranslation.locale).union(select(DocumentTranslation.locale))
        ).all()
    )


def get_blog_posts(author: Author, *, db_session: Session, locale: LocaleType = "en"):
    BlogPostTranslationAlias = aliased(BlogPostTranslation, flat=True)

    return db_session.scalars(
        select(BlogPostTranslationAlias)
        .join(BlogPost)
        .join(blog_post_authors)
        .join(Author)
        .filter(Author.id == author.id, BlogPostTranslationAlias.locale == locale)
    ).all()


def get_documents(author: Author, *, db_session: Session, locale: LocaleType = "en"):
    DocumentTranslationAlias = aliased(DocumentTranslation, flat=True)

    return db_session.scalars(
        select(DocumentTranslationAlias)
        .join(Document)
        .join(document_authors)
        .join(Author)
        .filter(Author.id == author.id, DocumentTranslationAlias.locale == locale)
    ).all()


def check_blog_posts_exist(author: Author, *, db_session: Session, locale: LocaleType):
    BlogPostTranslationAlias = aliased(BlogPostTranslation, flat=True)

    return db_session.scalar(
        select(
            exists(
                select(1)
                .select_from(BlogPostTranslationAlias)
                .join(BlogPost)
                .join(blog_post_authors)
                .where(BlogPostTranslationAlias.locale == locale)
                .where(blog_post_authors.c.author_id == author.id)
            )
        )
    )


def check_documents_exist(author: Author, *, db_session: Session, locale: LocaleType):
    DocumentTranslationAlias = aliased(DocumentTranslation, flat=True)

    return db_session.scalar(
        select(
            exists(
                select(1)
                .select_from(DocumentTranslationAlias)
                .join(Document)
                .join(document_authors)
                .where(DocumentTranslationAlias.locale == locale)
                .where(document_authors.c.author_id == author.id)
            )
        )
    )
