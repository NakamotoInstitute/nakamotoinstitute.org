import { Metadata } from "next";
import Link from "next/link";
import { Trans } from "react-i18next/TransWithoutContext";

import { PageLayout } from "@/app/components/PageLayout";
import { Rehype } from "@/app/components/Rehype";
import { RenderedItemsList } from "@/app/components/RenderedItemsList";
import { openGraphImages } from "@/app/shared-metadata";
import { getMempoolParams, getMempoolPost } from "@/lib/api/mempool";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { getDir } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";

import { PostHeader } from "../components/PostHeader";
import { TranslationLinks } from "../components/TranslationLinks";

export const dynamicParams = false;

export async function generateMetadata({
  params: { locale, slug },
}: LocaleParams<{ slug: string }>): Promise<Metadata> {
  const post = await getMempoolPost(slug, locale);

  const languages = Object.fromEntries(
    post.translations.map((t) => [
      t.locale,
      urls(t.locale).mempool.post(t.slug),
    ]),
  );

  if (post.image) {
    openGraphImages.push(post.image);
  }

  return {
    title: post.title,
    description: post.excerpt,
    alternates: {
      canonical: urls(locale).mempool.post(slug),
      languages,
    },
    openGraph: { images: openGraphImages },
    twitter: { images: openGraphImages },
  };
}

export default async function MempoolPost({
  params: { slug, locale },
}: LocaleParams<{ slug: string }>) {
  const { t } = await i18nTranslation(locale);
  const post = await getMempoolPost(slug, locale);

  const generateHref = (l: Locale) => {
    const translation = post.translations.find((t) => t.locale === l);
    if (translation) {
      return urls(l).mempool.post(translation.slug);
    }
    return urls(l).mempool.index;
  };

  return (
    <PageLayout
      t={t}
      locale={locale}
      generateHref={generateHref}
      breadcrumbs={[
        { label: t("mempool"), href: urls(locale).mempool.index },
        { label: post.title, href: urls(locale).mempool.post(post.slug) },
      ]}
      size="lg"
    >
      <article>
        <PostHeader t={t} locale={locale} post={post} />
        <section className="prose mx-auto md:prose-lg" dir={getDir(locale)}>
          <Rehype hasMath={post.hasMath}>{post.content}</Rehype>
          <hr />
          {post.translators.length > 0 ? (
            <p>
              <Trans
                t={t}
                i18nKey="translated_by"
                components={{
                  links: (
                    <RenderedItemsList
                      as="span"
                      locale={locale}
                      items={post.translators}
                      renderItem={(item) =>
                        item.url ? (
                          <Link key={item.slug} href={item.url}>
                            {item.name}
                          </Link>
                        ) : (
                          item.name
                        )
                      }
                    />
                  ),
                }}
              />
            </p>
          ) : null}
          {post.translations.length > 0 ? (
            <>
              {post.translators.length > 0 ? <hr /> : null}
              <p>
                <Trans
                  t={t}
                  i18nKey="translation_links"
                  components={{
                    links: (
                      <TranslationLinks
                        locale={locale}
                        translations={post.translations}
                        urlFunc={(item) =>
                          urls(item.locale).mempool.post(item.slug)
                        }
                      />
                    ),
                  }}
                />
              </p>
            </>
          ) : null}
        </section>
      </article>

      {post.series ? (
        <Link
          className="mt-4 block text-center"
          href={urls(locale).mempool.seriesDetail(post.series.slug)}
        >
          <Trans
            t={t}
            i18nKey="back_to_title"
            values={{
              title: post.series.title,
            }}
          />
        </Link>
      ) : null}
    </PageLayout>
  );
}

export async function generateStaticParams() {
  return getMempoolParams();
}
