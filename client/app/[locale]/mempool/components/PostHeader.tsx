import { TFunction } from "i18next";
import Image from "next/image";
import Link from "next/link";
import { Trans } from "react-i18next/TransWithoutContext";

import { AuthorsLinks } from "@/app/components/AuthorsLinks";
import { MempoolPost, MempoolSeries } from "@/lib/api/schemas/mempool";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";

type SeriesHeaderProps = {
  t: TFunction<string, string>;
  locale: Locale;
  series: MempoolSeries;
  seriesIndex: number;
};

async function SeriesHeader({
  t,
  locale,
  series,
  seriesIndex,
}: SeriesHeaderProps) {
  return (
    <div className="mb-6 text-center font-bold small-caps">
      <h2>
        <Link href={urls(locale).mempool.seriesDetail(series.slug)}>
          {series.title}
        </Link>
        {!series.chapterTitle ? ` (#${seriesIndex})` : null}
      </h2>
      {series?.chapterTitle ? (
        <p className="-mb-4 mt-2 text-xl md:mt-3 md:text-4xl">
          <Trans
            t={t}
            i18nKey="chapter_index"
            values={{ index: seriesIndex }}
          />
        </p>
      ) : null}
    </div>
  );
}

type PostHeaderProps = {
  t: TFunction<string, string>;
  locale: Locale;
  post: MempoolPost;
};

export async function PostHeader({ t, locale, post }: PostHeaderProps) {
  return (
    <>
      <header className="mx-auto text-center">
        {post.series && post.seriesIndex !== null ? (
          <SeriesHeader
            t={t}
            locale={locale}
            series={post.series}
            seriesIndex={post.seriesIndex}
          />
        ) : null}
        <h1 className="mb-4 text-4xl font-medium leading-[1.1] md:mb-6 md:text-7xl">
          {post.title}
        </h1>
        {post.subtitle ? (
          <p className="mb-4 text-2xl font-semibold md:mb-6 md:text-3xl">
            {post.subtitle}
          </p>
        ) : null}
        <AuthorsLinks
          className="mb-1 text-xl font-bold small-caps md:mb-4 md:text-2xl"
          itemClassName="text-dark"
          locale={locale}
          authors={post.authors}
        />
        <p className="text-xl font-bold opacity-60 small-caps md:text-2xl">
          <time dateTime={post.date.toISOString()}>
            {formatDate(locale, post.date)}
          </time>
        </p>
        {post.originalUrl && post.originalUrl ? (
          <p className="mt-4 text-lg italic">
            <Trans
              t={t}
              i18nKey="first_published"
              values={{ originalSite: post.originalSite }}
              components={{
                em: <em className="not-italic" />,
                a: (
                  <Link
                    className="text-cardinal hover:underline"
                    href={post.originalUrl}
                  />
                ),
              }}
            />
          </p>
        ) : null}
        {post.image ? (
          <div className="relative mx-auto mt-6 h-48 max-w-screen-sm sm:h-60 md:h-80">
            <Image
              className="object-contain"
              src={post.image}
              alt={post.imageAlt ?? ""}
              fill
            />
          </div>
        ) : null}
      </header>
      <hr className="mx-auto my-4 w-12 md:my-6" />
    </>
  );
}
