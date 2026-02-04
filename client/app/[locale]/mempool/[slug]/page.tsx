import { Metadata } from "next";
import Link from "next/link";
import { Trans } from "react-i18next/TransWithoutContext";

import { PageLayout } from "@/app/components/PageLayout";
import { Rehype } from "@/app/components/Rehype";
import { RenderedItemsList } from "@/app/components/RenderedItemsList";
import { openGraphImages } from "@/app/shared-metadata";
import { TranslationSchema, api, getOrNotFound } from "@/lib/api";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { getDir } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";

import { PostHeader } from "../components/PostHeader";
import { TranslationLinks } from "../components/TranslationLinks";

export const dynamicParams = false;

export async function generateMetadata(
  props: LocaleParams<{ slug: string }>,
): Promise<Metadata> {
  const params = await props.params;

  const { locale, slug } = params;

  const post = await getOrNotFound(
    api.mempool.getMempoolPost({
      path: { slug },
      query: { locale },
    }),
  );

  const languages = Object.fromEntries(
    post.translations.map((t: TranslationSchema) => [
      t.locale,
      urls(t.locale).mempool.post(t.slug),
    ]),
  );

  return {
    title: post.title,
    description: post.excerpt,
    alternates: {
      canonical: urls(locale).mempool.post(slug),
      languages,
    },
    openGraph: { type: "article", images: post.image ?? openGraphImages },
    twitter: { images: post.image ?? openGraphImages },
  };
}

export default async function MempoolPost(
  props: LocaleParams<{ slug: string }>,
) {
  const params = await props.params;

  const { slug, locale } = params;

  const { t } = await i18nTranslation(locale);
  const post = await getOrNotFound(
    api.mempool.getMempoolPost({
      path: { slug },
      query: { locale },
    }),
  );

  const generateHref = (l: Locale) => {
    const translation = post.translations.find(
      (t: TranslationSchema) => t.locale === l,
    );
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
        <section className="prose md:prose-lg mx-auto" dir={getDir(locale)}>
          <Rehype hasMath={post.hasMath}>{post.content}</Rehype>
          {post.translators.length > 0 || post.translations.length > 0 ? (
            <hr />
          ) : null}
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
  const { data } = await api.mempool.getMempoolParams();
  return data ?? [];
}
