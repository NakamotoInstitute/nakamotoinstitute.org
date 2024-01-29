import { Metadata } from "next";

import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { getEpisodes } from "@/lib/api/podcast";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";

import { EpisodeListing } from "./components/EpisodeListing";

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  return {
    title: t("The Crypto-Mises Podcast"),
  };
}

export default async function PodcastIndex({
  params: { locale },
}: LocaleParams) {
  const { t } = await i18nTranslation(locale);
  const episodes = await getEpisodes();
  const generateHref = (l: Locale) => urls(l).podcast.index;

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title={t("The Crypto-Mises Podcast")} />
      <section>
        {episodes.map((e) => (
          <EpisodeListing key={e.slug} locale={locale} episode={e} />
        ))}
      </section>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
