import { Metadata } from "next";
import Link from "next/link";
import { Trans } from "react-i18next/TransWithoutContext";

import { Markdown } from "@/app/components/Markdown";
import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { Price } from "@/lib/api/schemas/skeptics";
import { fetchPriceHistory, getSkeptics } from "@/lib/api/skeptics";
import { getPage } from "@/lib/content";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { externalUrls, urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";

import { SkepticListing } from "./components/SkepticListing";

const generateHref = (l: Locale) => urls(l).skeptics;

export async function generateMetadata(props: LocaleParams): Promise<Metadata> {
  const params = await props.params;

  const { locale } = params;

  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs([...locales], generateHref);

  return {
    title: t("the_skeptics"),
    alternates: {
      canonical: generateHref(locale),
      languages,
    },
  };
}

export default async function TheSkepticsPage(props: LocaleParams) {
  const params = await props.params;

  const { locale } = params;

  const content = await getPage("the-skeptics", locale);
  const { t } = await i18nTranslation(locale);
  let error = false;
  let prices: Price[] = [];
  let lastUpdated;
  const skeptics = await getSkeptics();
  try {
    prices = await fetchPriceHistory(60 * 60);
    lastUpdated = prices[prices.length - 1].date;
  } catch {
    error = true;
  }

  return (
    <PageLayout t={t} locale={locale} generateHref={generateHref}>
      <PageHeader
        title={t("the_skeptics")}
        subtitle={t("skeptics_tribute_capitalized")}
      >
        <Markdown className="page-content">{content}</Markdown>
        <div className="mt-4">
          <p>
            <Trans
              t={t}
              i18nKey="submit_github_link"
              components={{
                a: (
                  <Link
                    className="text-cardinal hover:underline"
                    href={externalUrls.github}
                  />
                ),
              }}
            />
          </p>
          <p>
            <Trans
              t={t}
              i18nKey="coinmetrics_data"
              components={{
                a: (
                  <Link
                    className="text-cardinal hover:underline"
                    href="https://coinmetrics.io"
                  />
                ),
              }}
            />
          </p>
          {lastUpdated ? (
            <p>
              <Trans
                t={t}
                i18nKey="last_updated"
                values={{ lastUpdated: formatDate(locale, lastUpdated) }}
                components={{
                  date: <time dateTime={lastUpdated.toISOString()} />,
                }}
              />
            </p>
          ) : null}
        </div>
      </PageHeader>
      {error ? <div>{t("price_loading_error")}</div> : null}
      <section>
        {skeptics.map((s) => (
          <SkepticListing
            key={s.slug}
            t={t}
            locale={locale}
            skeptic={s}
            prices={prices}
          />
        ))}
      </section>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
