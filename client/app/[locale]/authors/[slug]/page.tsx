import { Metadata } from "next";

import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { getAuthor, getAuthorParams } from "@/lib/api/authors";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { urls } from "@/lib/urls";

import { DocListing } from "@main/library/components/DocListing";
import { PostListing } from "@main/mempool/components/PostListing";

export const dynamicParams = false;

export async function generateMetadata(
  props: LocaleParams<{ slug: string }>,
): Promise<Metadata> {
  const params = await props.params;

  const { locale, slug } = params;

  const { author, locales } = await getAuthor(slug, locale);
  const languages = locales.reduce(
    (acc, loc) => {
      console.log(loc);
      acc[loc] = urls(loc).authors.detail(slug);
      return acc;
    },
    {} as Record<Locale, string>,
  );

  return {
    title: author.name,
    alternates: {
      canonical: urls(locale).authors.detail(slug),
      languages,
    },
  };
}

export default async function AuthorDetail(
  props: LocaleParams<{ slug: string }>,
) {
  const params = await props.params;

  const { slug, locale } = params;

  const { t } = await i18nTranslation(locale);
  const { author, mempool, library } = await getAuthor(slug, locale);

  const generateHref = (l: Locale) => urls(l).authors.detail(slug);

  return (
    <PageLayout
      t={t}
      locale={locale}
      generateHref={generateHref}
      breadcrumbs={[
        { label: t("authors"), href: urls(locale).authors.index },
        { label: author.name, href: urls(locale).authors.detail(author.slug) },
      ]}
    >
      <PageHeader title={author.name} />
      {library.length > 0 ? (
        <section>
          <h2 className="mb-5 text-2xl font-bold">{t("library")}</h2>
          {library.map((doc) => (
            <DocListing
              className="first-of-type:border-t-0 first-of-type:pt-0"
              key={doc.slug}
              t={t}
              doc={doc}
              locale={locale}
            />
          ))}
        </section>
      ) : null}
      {mempool.length > 0 ? (
        <section>
          <h2 className="mb-5 text-2xl font-bold">{t("mempool")}</h2>
          {mempool.map((post) => (
            <PostListing
              className="first-of-type:border-t-0 first-of-type:pt-0"
              key={post.slug}
              t={t}
              post={post}
              locale={locale}
            />
          ))}
        </section>
      ) : null}
    </PageLayout>
  );
}

export async function generateStaticParams() {
  return getAuthorParams();
}
