import clsx from "clsx";
import { TFunction } from "i18next";
import Link from "next/link";
import { Trans } from "react-i18next/TransWithoutContext";

import { AuthorsLinks } from "@/app/components/AuthorsLinks";
import { MempoolPostIndex } from "@/lib/api/schemas/mempool";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";

type PostListingProps = {
  t: TFunction<string, string>;
  className?: string;
  locale: Locale;
  post: MempoolPostIndex;
};

export async function PostListing({
  t,
  className,
  locale,
  post,
}: PostListingProps) {
  const original = post.date.getTime() === post.added.getTime();

  return (
    <article
      className={clsx(
        "grid-col-1 md:grid-col-2 grid border-t border-dashed border-taupe-light py-4 last:border-b md:grid-cols-[7fr,3fr]",
        className,
      )}
    >
      <header className="order-1">
        {post.series ? (
          <h3 className="text-sm small-caps">
            <Link href={urls(locale).mempool.seriesDetail(post.series.slug)}>
              {post.series.title}
            </Link>
            {!post.series.chapterTitle ? ` (#${post.seriesIndex})` : null}
          </h3>
        ) : null}
        <h2 className="font-bold md:text-xl">
          {post.series?.chapterTitle ? `Chapter ${post.seriesIndex}: ` : null}
          <Link
            className="text-cardinal hover:underline"
            href={urls(locale).mempool.post(post.slug)}
          >
            {post.title}
          </Link>
        </h2>
        <p className="small-caps">
          <AuthorsLinks authors={post.authors} locale={locale} as="span" />
          <span className="mx-1">•</span>
          <time dateTime={post.date.toISOString()}>
            {formatDate(locale, post.date)}
          </time>
        </p>
      </header>
      <section className="order-2 my-2 md:order-3">
        <p className="italic">&ldquo;{post.excerpt}&rdquo;</p>
      </section>

      <footer className="order-3 text-sm text-dark/70 small-caps md:order-2 md:text-right">
        {!original ? (
          <span>
            <Trans
              t={t}
              i18nKey="added_date"
              components={{
                date: <time dateTime={post.added.toISOString()} />,
              }}
              values={{ pubDate: formatDate(locale, post.added) }}
            />
          </span>
        ) : null}
      </footer>
    </article>
  );
}
