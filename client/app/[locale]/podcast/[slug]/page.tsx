import { Markdown, PageLayout } from "@/app/components";
import { PageHeader } from "@/app/components/PageHeader";
import { getEpisode, getEpisodes } from "@/lib/api";
import { getLocaleParams, i18nTranslation } from "@/lib/i18n";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";
import { Metadata } from "next";
import Link from "next/link";

export async function generateMetadata({
  params: { slug },
}: LocaleParams<{ slug: string }>): Promise<Metadata> {
  const episode = await getEpisode(slug);
  return {
    title: episode.title,
  };
}

export default async function PodcastDetail({
  params: { locale, slug },
}: LocaleParams<{ slug: string }>) {
  const { t } = await i18nTranslation(locale);
  const episode = await getEpisode(slug);
  const generateHref = (l: Locale) => urls(l).podcast.episode(slug);

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title={episode.title}>
        <p>
          <time dateTime={episode.date.toISOString()}>
            {formatDate(locale, episode.date)}
          </time>
        </p>
      </PageHeader>
      <section className="prose mx-auto">
        <Markdown>{episode.content}</Markdown>
        <iframe
          className="aspect-video w-full"
          src={`https://www.youtube.com/embed/${episode.youtubeId}?rel=0`}
          allowFullScreen
        ></iframe>
        <p className="text-center">
          <Link href={urls(locale).podcast.episodeMp3(episode.slug)}>
            {t("Download .mp3")}
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
