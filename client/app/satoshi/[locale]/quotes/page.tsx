import { Metadata } from "next";
import Link from "next/link";
import { Trans } from "react-i18next/TransWithoutContext";

import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { getQuoteCategories } from "@/lib/api/quotes";
import { QuoteCategory } from "@/lib/api/schemas/quotes";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";

const generateHref = (l: Locale) => urls(l).satoshi.quotesIndex;

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const languages = generateHrefLangs([...locales], generateHref);

  return {
    alternates: {
      canonical: generateHref(locale),
      languages,
    },
  };
}

type LinkColumnProps = {
  locale: Locale;
  categories: QuoteCategory[];
};

function LinkColumn({ locale, categories }: LinkColumnProps) {
  return (
    <ul className="w-1/2">
      {categories.map((c) => (
        <li key={c.slug}>
          <Link href={urls(locale).satoshi.quoteCategory(c.slug)}>
            {c.name}
          </Link>
        </li>
      ))}
    </ul>
  );
}

export default async function QuotesIndex({
  params: { locale },
}: LocaleParams) {
  const { t } = await i18nTranslation(locale);
  const categories = await getQuoteCategories();

  const halfLength = Math.ceil(categories.length / 2);
  const firstColumn = categories.slice(0, halfLength);
  const secondColumn = categories.slice(halfLength);

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
        <figure>
          <blockquote>
            <Trans
              i18nKey="satoshi_quote_extended"
              components={{
                br: <br />,
                em: <em />,
              }}
            />
          </blockquote>
          <figcaption>
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
                date: formatDate(locale, new Date(Date.UTC(2008, 11, 14))),
              }}
            />
          </figcaption>
        </figure>
      </PageHeader>
      <section className="flex">
        <LinkColumn locale={locale} categories={firstColumn} />
        <LinkColumn locale={locale} categories={secondColumn} />
      </section>
      <hr className="my-4" />
      <footer className="text-center italic">
        <p>
          <Trans
            t={t}
            i18nKey="quotable_satoshi_acknowledgements"
            components={{
              a: <Link href="https://charts.bitbo.io" />,
            }}
          />
        </p>
        <p>
          <Trans
            t={t}
            i18nKey="add_quotation_request"
            components={{
              contact: <Link href={urls(locale).contact} />,
              github: <Link href={urls(locale).github} />,
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
