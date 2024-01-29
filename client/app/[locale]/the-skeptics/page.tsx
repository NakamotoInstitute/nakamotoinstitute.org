import { Metadata } from "next";
import Link from "next/link";
import { Trans } from "react-i18next/TransWithoutContext";

import { Markdown } from "@/app/components/Markdown";
import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { Price } from "@/lib/api/schemas/skeptics";
import { fetchPriceHistory, getSkeptics } from "@/lib/api/skeptics";
import { getPage } from "@/lib/content";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";

import { SkepticListing } from "./components/SkepticListing";

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  return {
    title: t("The Skeptics"),
  };
}

export default async function TheSkepticsPage({
  params: { locale },
}: LocaleParams) {
  const content = await getPage("the-skeptics", locale);
  const { t } = await i18nTranslation(locale);
  let error = false;
  let prices: Price[] = [];
  let lastUpdated;
  const skeptics = await getSkeptics();
  try {
    prices = await fetchPriceHistory(60 * 60);
    lastUpdated = prices[prices.length - 1].date;
  } catch (err) {
    error = true;
  }

  const generateHref = (l: Locale) => urls(l).skeptics;

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title={t("The Skeptics")}>
        <Markdown>{content}</Markdown>
        <p>
          <Trans
            t={t}
            i18nKey="Submit a link via <a>GitHub</a>"
            components={{
              a: <Link href={urls(locale).github}>GitHub</Link>,
            }}
          />
        </p>
        <div>
          <p>
            <Trans
              t={t}
              i18nKey="Price data by <a>CoinMetrics.io</a>"
              components={{
                a: <Link href="https://coinmetrics.io" />,
              }}
            />
          </p>
          {lastUpdated ? (
            <p>
              <Trans
                t={t}
                i18nKey="Last updated: <date>{{lastUpdated}}</date>"
                values={{ lastUpdated: formatDate(locale, lastUpdated) }}
                components={{
                  date: <time dateTime={lastUpdated.toISOString()} />,
                }}
              />
            </p>
          ) : null}
        </div>
      </PageHeader>
      {error ? <div>{t("Error loading prices")}</div> : null}
      <section>
        {skeptics.map((s) => (
          <SkepticListing
            key={s.slug}
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
