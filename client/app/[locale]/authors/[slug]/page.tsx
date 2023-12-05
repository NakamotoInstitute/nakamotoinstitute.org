import { Metadata } from "next";
import { PageLayout } from "@/app/components/PageLayout";
import { PageHeader } from "@/app/components/PageHeader";
import { getAuthor, getAuthorParams } from "@/lib/api/authors";
import { urls } from "@/lib/urls";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { DocListing } from "@main/library/components/DocListing";
import { PostListing } from "@main/mempool/components/PostListing";

export const dynamicParams = false;

export async function generateMetadata({
  params: { locale, slug },
}: LocaleParams<{ slug: string }>): Promise<Metadata> {
  const { author } = await getAuthor(slug, locale);
  return {
    title: author.name,
  };
}

export default async function AuthorDetail({
  params: { slug, locale },
}: LocaleParams<{ slug: string }>) {
  const { t } = await i18nTranslation(locale);
  const { author, mempool, library } = await getAuthor(slug, locale);

  const generateHref = (l: Locale) => urls(l).authors.detail(slug);

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title={author.name} />
      {library.length > 0 ? (
        <section>
          <h2 className="text-3xl">{t("Library")}</h2>
          {library.map((doc) => (
            <DocListing key={doc.slug} doc={doc} locale={locale} />
          ))}
        </section>
      ) : null}
      {mempool.length > 0 ? (
        <section>
          <h2 className="text-3xl">{t("Mempool")}</h2>
          {mempool.map((post) => (
            <PostListing key={post.slug} post={post} locale={locale} />
          ))}
        </section>
      ) : null}
    </PageLayout>
  );
}

export async function generateStaticParams() {
  return getAuthorParams();
}
