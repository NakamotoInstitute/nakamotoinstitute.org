import { Metadata } from "next";

import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { getAuthor, getAuthorParams } from "@/lib/api/authors";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { urls } from "@/lib/urls";

import { DocListing } from "@main/library/components/DocListing";
import { PostListing } from "@main/mempool/components/PostListing";

export const dynamicParams = false;

export async function generateMetadata({
  params: { locale, slug },
}: LocaleParams<{ slug: string }>): Promise<Metadata> {
  const { author, locales } = await getAuthor(slug, locale);
  const languages = locales.reduce(
    (acc, loc) => {
      acc[loc] = urls(loc).authors.detail(slug);
      return acc;
    },
    {} as Record<Locale, string>,
  );

  return {
    title: author.name,
    alternates: { languages },
  };
}

export default async function AuthorDetail({
  params: { slug, locale },
}: LocaleParams<{ slug: string }>) {
  const { t } = await i18nTranslation(locale);
  const { author, mempool, library } = await getAuthor(slug, locale);

  const generateHref = (l: Locale) => urls(l).authors.detail(slug);

  return (
    <PageLayout t={t} locale={locale} generateHref={generateHref}>
      <PageHeader title={author.name} />
      {library.length > 0 ? (
        <section>
          <h2 className="text-3xl">{t("library")}</h2>
          {library.map((doc) => (
            <DocListing key={doc.slug} t={t} doc={doc} locale={locale} />
          ))}
        </section>
      ) : null}
      {mempool.length > 0 ? (
        <section>
          <h2 className="text-3xl">{t("mempool")}</h2>
          {mempool.map((post) => (
            <PostListing key={post.slug} t={t} post={post} locale={locale} />
          ))}
        </section>
      ) : null}
    </PageLayout>
  );
}

export async function generateStaticParams() {
  return getAuthorParams();
}
