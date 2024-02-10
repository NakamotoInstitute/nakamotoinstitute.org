from typing import List

from sqlalchemy import or_, select, union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, joinedload, selectinload

from sni.constants import LocaleType
from sni.models import (
    Author,
    BlogPost,
    BlogPostTranslation,
    BlogSeries,
    Document,
    DocumentTranslation,
    blog_post_authors,
    document_authors,
)


async def get(
    slug: str, *, db_session: AsyncSession, locale: LocaleType = "en"
) -> Author:
    query = (
        select(Author)
        .filter_by(slug=slug)
        .options(
            selectinload(Author.posts).options(
                selectinload(BlogPost.authors),
                selectinload(
                    BlogPost.translations.and_(BlogPostTranslation.locale == locale)
                ),
            ),
            selectinload(Author.docs).options(
                selectinload(Document.authors),
                selectinload(
                    Document.translations.and_(DocumentTranslation.locale == locale)
                ).options(selectinload(DocumentTranslation.formats)),
            ),
        )
    )

    return await db_session.scalar(query)


async def get_documents(
    author_id: int, *, db_session: AsyncSession, locale: LocaleType = "en"
):
    DocumentTranslationAlias = aliased(DocumentTranslation, flat=True)

    query = (
        select(DocumentTranslationAlias)
        .join(Document)
        .join(document_authors)
        .filter(
            document_authors.c.author_id == author_id,
            DocumentTranslationAlias.locale == locale,
        )
        .order_by(DocumentTranslationAlias.sort_title)
    )

    result = await db_session.scalars(query)
    return result.all()


async def get_blog_posts(
    author_id: int, *, db_session: AsyncSession, locale: LocaleType = "en"
):
    BlogPostTranslationAlias = aliased(BlogPostTranslation, flat=True)

    query = (
        select(BlogPostTranslationAlias)
        .options(
            joinedload(BlogPostTranslationAlias.blog_post).options(
                selectinload(BlogPost.authors),
                selectinload(BlogPost.translations),
                joinedload(BlogPost.series).selectinload(BlogSeries.translations),
            )
        )
        .join(BlogPost)
        .join(blog_post_authors)
        .filter(
            blog_post_authors.c.author_id == author_id,
            BlogPostTranslationAlias.locale == locale,
        )
        .order_by(BlogPost.date.desc())
    )

    result = await db_session.scalars(query)
    return result.all()


async def get_all_by_locale(
    *, db_session: AsyncSession, locale: LocaleType = "en"
) -> List[Author]:
    DocumentTranslationAlias = aliased(DocumentTranslation, flat=True)
    BlogPostTranslationAlias = aliased(BlogPostTranslation, flat=True)

    query = (
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
        .distinct()
        .order_by(Author.sort_name)
    )

    result = await db_session.scalars(query)
    return result.all()


async def get_params(*, db_session: AsyncSession):
    DocumentTranslationAlias = aliased(DocumentTranslation)
    BlogPostTranslationAlias = aliased(BlogPostTranslation)

    document_query = (
        select(Author.slug, DocumentTranslationAlias.locale)
        .join(Author.docs)
        .join(DocumentTranslationAlias)
        .distinct()
    )

    blog_post_query = (
        select(Author.slug, BlogPostTranslationAlias.locale)
        .join(Author.posts)
        .join(BlogPostTranslationAlias)
        .distinct()
    )

    combined_query = union(document_query, blog_post_query)

    result = await db_session.execute(combined_query)
    combined_result = result.all()

    all_params = set(combined_result)
    return [dict(slug=slug, locale=locale) for slug, locale in all_params]


async def get_author_locales(
    author_id: int, *, db_session: AsyncSession, locale: LocaleType = "en"
):
    BlogPostTranslationAlias = aliased(BlogPostTranslation, flat=True)
    DocumentTranslationAlias = aliased(DocumentTranslation, flat=True)

    document_query = (
        select(DocumentTranslationAlias.locale)
        .join(Document)
        .join(document_authors)
        .distinct()
        .filter(
            document_authors.c.author_id == author_id,
            DocumentTranslationAlias.locale != locale,
        )
    )

    blog_post_query = (
        select(BlogPostTranslationAlias.locale)
        .join(BlogPost)
        .join(blog_post_authors)
        .distinct()
        .filter(
            blog_post_authors.c.author_id == author_id,
            BlogPostTranslationAlias.locale != locale,
        )
    )

    combined_query = union(document_query, blog_post_query)
    result = await db_session.execute(combined_query)
    return [locale for (locale,) in result]
