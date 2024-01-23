import { Metadata } from "next";
import Link from "next/link";
import { Trans } from "react-i18next/TransWithoutContext";
import { Rehype } from "@/app/components/Rehype";
import { getMempoolPost, getMempoolParams } from "@/lib/api/mempool";
import { PageLayout } from "@/app/components/PageLayout";
import { getDir } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { PostHeader } from "../components/PostHeader";
import { TranslationLinks } from "../components/TranslationLinks";

export const dynamicParams = false;

export async function generateMetadata({
  params: { locale, slug },
}: LocaleParams<{ slug: string }>): Promise<Metadata> {
  const post = await getMempoolPost(slug, locale);
  return {
    title: post.title,
  };
}

export default async function MempoolPost({
  params: { slug, locale },
}: LocaleParams<{ slug: string }>) {
  const { t } = await i18nTranslation(locale);
  const post = await getMempoolPost(slug, locale);

  const backHref = urls(locale).mempool.index;
  const backLabel = t("Back to the Memory Pool");

  const generateHref = (l: Locale) => {
    const translation = post.translations?.find((t) => t.locale === l);
    if (translation) {
      return urls(l).mempool.post(translation.slug);
    }
    return urls(l).mempool.index;
  };

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <Link className="mb-4 block text-center" href={backHref}>
        {backLabel}
      </Link>
      <article>
        <PostHeader locale={locale} post={post} />
        <section className="prose mx-auto" dir={getDir(locale)}>
          <Rehype hasMath={post.hasMath}>{post.content}</Rehype>
          <hr />
          {post.translations.length > 0 ? (
            <p>
              <Trans
                t={t}
                i18nKey="Read in <links />"
                components={{
                  links: (
                    <TranslationLinks
                      locale={locale}
                      translations={post.translations}
                      urlFunc={(item) =>
                        urls(item.locale as Locale).mempool.post(item.slug)
                      }
                    />
                  ),
                }}
              />
            </p>
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
            i18nKey="Back to {{title}}"
            values={{
              title: post.series.title,
            }}
          />
        </Link>
      ) : null}
      <Link className="mt-4 block text-center" href={backHref}>
        {backLabel}
      </Link>
    </PageLayout>
  );
}

export async function generateStaticParams() {
  return getMempoolParams();
}
