import { Metadata } from "next";
import Link from "next/link";

import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { Rehype } from "@/app/components/Rehype";
import { locales } from "@/i18n";
import { getEpisode, getEpisodes } from "@/lib/api/podcast";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";

const generateHref = (slug: string) => (l: Locale) =>
  urls(l).podcast.episode(slug);

export async function generateMetadata({
  params: { locale, slug },
}: LocaleParams<{ slug: string }>): Promise<Metadata> {
  const episode = await getEpisode(slug);
  const languages = generateHrefLangs([...locales], generateHref(slug));

  return {
    title: episode.title,
    alternates: {
      canonical: generateHref(slug)(locale),
      languages,
    },
  };
}

export default async function PodcastDetail({
  params: { locale, slug },
}: LocaleParams<{ slug: string }>) {
  const { t } = await i18nTranslation(locale);
  const episode = await getEpisode(slug);

  return (
    <PageLayout t={t} locale={locale} generateHref={generateHref(slug)}>
      <PageHeader title={episode.title}>
        <p>
          <time dateTime={episode.date.toISOString()}>
            {formatDate(locale, episode.date)}
          </time>
        </p>
      </PageHeader>
      <section className="prose mx-auto">
        <Rehype>{episode.content}</Rehype>
        <iframe
          className="aspect-video w-full"
          src={`https://www.youtube.com/embed/${episode.youtubeId}?rel=0`}
          allowFullScreen
        ></iframe>
        <p className="text-center">
          <Link href={urls(locale).podcast.episodeMp3(episode.slug)}>
            {t("download_mp3")}
          </Link>
        </p>
      </section>
    </PageLayout>
  );
}

export async function generateStaticParams() {
  const episodes = await getEpisodes();
  return getLocaleParams((locale) =>
    episodes.map((e) => ({ locale, slug: e.slug })),
  );
}
