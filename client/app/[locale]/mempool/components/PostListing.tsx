import clsx from "clsx";
import { TFunction } from "i18next";
import Link from "next/link";
import { Trans } from "react-i18next/TransWithoutContext";

import { AuthorsLinks } from "@/app/components/AuthorsLinks";
import { MempoolPostIndex } from "@/lib/api/schemas/mempool";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";

import { TranslationLinks } from "../components/TranslationLinks";

type PostListingProps = {
  t: TFunction<string, string>;
  locale: Locale;
  post: MempoolPostIndex;
};

export async function PostListing({ t, locale, post }: PostListingProps) {
  const original = post.date.getTime() === post.added.getTime();

  return (
    <article className="border-b border-solid py-4 first:pt-0 last:border-b-0">
      <header>
        {post.series ? (
          <h3 className="text-md font-semibold">
            <Link href={urls(locale).mempool.seriesDetail(post.series.slug)}>
              {post.series.title}
            </Link>
            {!post.series.chapterTitle ? ` (#${post.seriesIndex})` : null}
          </h3>
        ) : null}
        <h2 className="text-xl font-bold">
          {post.series?.chapterTitle ? `Chapter ${post.seriesIndex}: ` : null}
          <Link href={urls(locale).mempool.post(post.slug)}>{post.title}</Link>
        </h2>
        <p>
          <AuthorsLinks authors={post.authors} locale={locale} as="span" />
          {" • "}
          <time dateTime={post.date.toISOString()}>
            {formatDate(locale, post.date)}
          </time>
        </p>
      </header>
      <section className="my-2">
        <p className="italic">&ldquo;{post.excerpt}&rdquo;</p>
      </section>
      {!original || post.translations.length > 0 ? (
        <footer
          className={clsx(
            "flex flex-wrap gap-4 gap-y-2 text-sm text-gray-600",
            post.translations.length > 0 ? "justify-between" : "justify-end",
          )}
        >
          {post.translations.length > 0 ? (
            <div>
              <Trans
                t={t}
                i18nKey="Read in <links />"
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
            </div>
          ) : null}
          {!original ? (
            <div>
              <Trans
                t={t}
                i18nKey="Added: <date>{{pubDate}}</date>"
                components={{
                  date: <time dateTime={post.added.toISOString()} />,
                }}
                values={{ pubDate: formatDate(locale, post.added) }}
              />
            </div>
          ) : null}
        </footer>
      ) : undefined}
    </article>
  );
}
