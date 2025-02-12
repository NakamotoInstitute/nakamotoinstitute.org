import { Metadata } from "next";
import Link from "next/link";
import { Trans } from "react-i18next/TransWithoutContext";

import { ListColumnLayout } from "@/app/components/ListColumnLayout";
import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { getQuoteCategories } from "@/lib/api/quotes";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { externalUrls, urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";

const generateHref = (l: Locale) => urls(l).satoshi.quotesIndex;

export async function generateMetadata(props: LocaleParams): Promise<Metadata> {
  const params = await props.params;

  const { locale } = params;

  const languages = generateHrefLangs([...locales], generateHref);

  return {
    alternates: {
      canonical: generateHref(locale),
      languages,
    },
  };
}

export default async function QuotesIndex(props: LocaleParams) {
  const params = await props.params;

  const { locale } = params;

  const { t } = await i18nTranslation(locale);
  const categories = await getQuoteCategories();

  return (
    <PageLayout
      t={t}
      locale={locale}
      generateHref={generateHref}
      breadcrumbs={[
        {
          label: t("complete_satoshi"),
          href: urls(locale).satoshi.index,
        },
        {
          label: t("quotable_satoshi"),
          href: urls(locale).satoshi.quotesIndex,
        },
      ]}
    >
      <PageHeader title={t("quotable_satoshi")}>
        <figure className="border-l-1 border-dashed border-cardinal">
          <blockquote className="px-4 italic">
            <Trans
              i18nKey="satoshi_quote_extended"
              components={{
                br: <br />,
                em: <em />,
              }}
            />
          </blockquote>
          <figcaption className="mt-3 px-4 text-lg font-medium small-caps">
            <Trans
              i18nKey="satoshi_citation"
              components={{
                a: (
                  <Link
                    href={urls(locale).authors.detail("satoshi-nakamoto")}
                  />
                ),
              }}
              values={{
                date: formatDate(locale, new Date(Date.UTC(2008, 10, 14))),
              }}
            />
          </figcaption>
        </figure>
      </PageHeader>
      <ListColumnLayout
        items={categories}
        hrefFunc={(slug: string) => urls(locale).satoshi.quoteCategory(slug)}
      />
      <footer>
        <p>
          <Trans
            t={t}
            i18nKey="quotable_satoshi_acknowledgements"
            components={{
              a: (
                <Link
                  className="text-cardinal hover:underline"
                  href="https://charts.bitbo.io"
                />
              ),
            }}
          />
        </p>
        <p>
          <Trans
            t={t}
            i18nKey="add_quotation_request"
            components={{
              contact: (
                <Link
                  className="text-cardinal hover:underline"
                  href={urls(locale).contact}
                />
              ),
              github: (
                <Link
                  className="text-cardinal hover:underline"
                  href={externalUrls.github}
                />
              ),
            }}
          />
        </p>
      </footer>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
