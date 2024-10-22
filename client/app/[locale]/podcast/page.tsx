import { Metadata } from "next";

import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { getEpisodes } from "@/lib/api/podcast";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";

import { EpisodeListing } from "./components/EpisodeListing";

const generateHref = (l: Locale) => urls(l).podcast.index;

export async function generateMetadata(props: LocaleParams): Promise<Metadata> {
  const params = await props.params;

  const { locale } = params;

  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs([...locales], generateHref);

  return {
    title: t("crypto_mises_podcast"),
    alternates: {
      canonical: generateHref(locale),
      languages,
    },
  };
}

export default async function PodcastIndex(props: LocaleParams) {
  const params = await props.params;

  const { locale } = params;

  const { t } = await i18nTranslation(locale);
  const episodes = await getEpisodes();

  return (
    <PageLayout t={t} locale={locale} generateHref={generateHref}>
      <PageHeader title={t("crypto_mises_podcast")} />
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
