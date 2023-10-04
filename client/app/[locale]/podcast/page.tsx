import { PageLayout } from "@/app/components";
import { PageHeader } from "@/app/components/PageHeader";
import { getEpisodes } from "@/lib/api";
import { getLocaleParams, i18nTranslation } from "@/lib/i18n";
import { urls } from "@/lib/urls";
import { Metadata } from "next";
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
