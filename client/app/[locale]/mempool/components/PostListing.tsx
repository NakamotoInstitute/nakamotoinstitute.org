import Link from "next/link";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";
import { AuthorsLinks } from "@/app/components";
import { i18nTranslation } from "@/lib/i18n";
import { Trans } from "react-i18next/TransWithoutContext";
import { MempoolPost } from "@/lib/api/schemas";

export async function PostListing({
  locale,
  post,
}: {
  locale: Locale;
  post: MempoolPost;
}) {
  const { t } = await i18nTranslation(locale);
  const original = post.date.getTime() === post.added.getTime();

  return (
    <article className="border-b border-solid border-night py-4 first:pt-0 last:border-b-0">
      <header>
        {post.series ? (
          <h3 className="text-xl">
            <Link href={urls(locale).mempool.seriesDetail(post.series.slug)}>
              {post.series.title}
            </Link>
            {!post.series.chapterTitle ? ` (#${post.seriesIndex})` : null}
          </h3>
        ) : null}
        <h2 className="text-2xl">
          <Link href={urls(locale).mempool.post(post.slug)}>{post.title}</Link>
        </h2>
        <p>
          <AuthorsLinks authors={post.authors} locale={locale} as="span" />
          {" • "}
          <time dateTime={post.added.toISOString()}>
            {formatDate(locale, post.added)}
          </time>
        </p>
      </header>
      <section className="my-2">
        <p className="italic">&ldquo;{post.excerpt}&rdquo;</p>
      </section>
      {!original ? (
        <footer className="text-right">
          <p>
            <Trans
              t={t}
              i18nKey="Originally published: <date>{{pubDate}}</date>"
              components={{
                date: <time dateTime={post.date.toISOString()} />,
              }}
              values={{ pubDate: formatDate(locale, post.date) }}
            />
          </p>
        </footer>
      ) : undefined}
    </article>
  );
}
