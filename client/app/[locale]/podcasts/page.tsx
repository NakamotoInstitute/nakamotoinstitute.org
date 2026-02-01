import { Metadata } from "next";

import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { PodcastBase, api } from "@/lib/api";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";

import { PodcastListing } from "./components/PodcastListing";

export const dynamicParams = false;

const generateHref = (l: Locale) => urls(l).podcasts.index;

export async function generateMetadata(props: LocaleParams): Promise<Metadata> {
  const params = await props.params;

  const { locale } = params;

  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs(locales, generateHref);

  return {
    title: t("podcasts"),
    alternates: {
      canonical: generateHref(locale),
      languages,
    },
  };
}

export default async function PodcastsIndex(props: LocaleParams) {
  const params = await props.params;

  const { locale } = params;

  const { t } = await i18nTranslation(locale);
  const { data: podcasts = [] } = await api.podcasts.getPodcasts();

  return (
    <PageLayout t={t} locale={locale} generateHref={generateHref}>
      <PageHeader title={t("podcasts")}>
        <p className="text-lg">{t("podcast_description")}</p>
      </PageHeader>
      <section>
        {podcasts.map((podcast: PodcastBase) => (
          <PodcastListing
            key={podcast.slug}
            podcast={podcast}
            locale={locale}
            t={t}
          />
        ))}
      </section>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
