from typing import List

from sqlalchemy import exists, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

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


async def get(slug: str, *, db_session: AsyncSession) -> Author:
    return await db_session.scalar(select(Author).filter_by(slug=slug))


async def get_all(*, db_session: AsyncSession) -> List[Author]:
    return (await db_session.scalars(select(Author))).all()


async def get_all_by_locale(
    *, db_session: AsyncSession, locale: LocaleType = "en"
) -> List[Author]:
    DocumentTranslationAlias = aliased(DocumentTranslation, flat=True)
    BlogPostTranslationAlias = aliased(BlogPostTranslation, flat=True)

    return (
        await db_session.scalars(
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
        )
    ).all()


async def get_all_author_locales(*, db_session: AsyncSession):
    return set(
        (
            await db_session.scalars(
                select(BlogPostTranslation.locale).union(
                    select(DocumentTranslation.locale)
                )
            )
        ).all()
    )


async def get_author_locales(
    author: Author, *, db_session: AsyncSession, locale: LocaleType = "en"
):
    BlogPostTranslationAlias = aliased(BlogPostTranslation, flat=True)
    DocumentTranslationAlias = aliased(DocumentTranslation, flat=True)

    return set(
        (
            await db_session.scalars(
                select(BlogPostTranslationAlias.locale)
                .join(BlogPost)
                .join(blog_post_authors)
                .join(Author)
                .filter(
                    Author.id == author.id, BlogPostTranslationAlias.locale != locale
                )
                .union(
                    select(DocumentTranslationAlias.locale)
                    .join(Document)
                    .join(document_authors)
                    .join(Author)
                    .filter(
                        Author.id == author.id,
                        DocumentTranslationAlias.locale != locale,
                    )
                )
            )
        ).all()
    )


async def get_blog_posts(
    author: Author, *, db_session: AsyncSession, locale: LocaleType = "en"
):
    BlogPostTranslationAlias = aliased(BlogPostTranslation, flat=True)

    return (
        await db_session.scalars(
            select(BlogPostTranslationAlias)
            .join(BlogPost)
            .join(blog_post_authors)
            .join(Author)
            .filter(Author.id == author.id, BlogPostTranslationAlias.locale == locale)
        )
    ).all()


async def get_documents(
    author: Author, *, db_session: AsyncSession, locale: LocaleType = "en"
):
    DocumentTranslationAlias = aliased(DocumentTranslation, flat=True)

    return (
        await db_session.scalars(
            select(DocumentTranslationAlias)
            .join(Document)
            .join(document_authors)
            .join(Author)
            .filter(Author.id == author.id, DocumentTranslationAlias.locale == locale)
        )
    ).all()


async def check_blog_posts_exist(
    author: Author, *, db_session: AsyncSession, locale: LocaleType
):
    BlogPostTranslationAlias = aliased(BlogPostTranslation, flat=True)

    return await db_session.scalar(
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


async def check_documents_exist(
    author: Author, *, db_session: AsyncSession, locale: LocaleType
):
    DocumentTranslationAlias = aliased(DocumentTranslation, flat=True)

    return await db_session.scalar(
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
