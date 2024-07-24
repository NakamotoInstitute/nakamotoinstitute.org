import { TFunction } from "i18next";
import { Metadata } from "next";
import Link from "next/link";

import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { RenderedItemsList } from "@/app/components/RenderedItemsList";
import { locales } from "@/i18n";
import { getQuoteCategories, getQuoteCategory } from "@/lib/api/quotes";
import { Quote } from "@/lib/api/schemas/quotes";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";
import { formatEmailSource, formatPostSource } from "@/utils/strings";

import { ContentBox, ContentBoxBody } from "@satoshi/components/ContentBox";

const generateHref = (slug: string) => (l: Locale) =>
  urls(l).satoshi.quoteCategory(slug);

export async function generateMetadata({
  params: { locale, slug },
}: LocaleParams<{ slug: string }>): Promise<Metadata> {
  const { category } = await getQuoteCategory(slug);
  const languages = generateHrefLangs([...locales], generateHref(slug));

  return {
    title: category.name,
    alternates: {
      canonical: generateHref(slug)(locale),
      languages,
    },
  };
}

type SatoshiQuoteProps = {
  t: TFunction<string, string>;
  locale: Locale;
  quote: Quote;
};

async function SatoshiQuote({ t, locale, quote }: SatoshiQuoteProps) {
  let source: string;
  let subject: string | undefined = undefined;
  let url: string;
  let label: string;

  if (quote.whitepaper) {
    source = t("bitcoin_title");
    url = urls("en").library.doc("bitcoin");
    label = t("view_whitepaper");
  } else if (quote.post) {
    source = formatPostSource(quote.post.source);
    subject = quote.post.subject;
    url = urls(locale).satoshi.posts.sourcePost(
      quote.post.source,
      quote.post.satoshiId.toString(),
    );
    label = t("view_post");
  } else if (quote.email) {
    source = formatEmailSource(quote.email.source);
    subject = quote.email.subject;
    url = urls(locale).satoshi.emails.sourceEmail(
      quote.email.source,
      quote.email.satoshiId.toString(),
    );
    label = t("view_email");
  } else {
    return null;
  }

  return (
    <ContentBox as="article" className="mb-3 last:mb-0">
      <header className="border-b border-dashed border-taupe bg-dandelion font-mono">
        <div className="border-b border-dashed border-taupe px-8 py-2">
          {source ? <div className="font-bold">{source}</div> : null}
        </div>
        <div className="grid grid-cols-[auto_1fr] gap-x-4 px-8 py-2">
          {subject ? (
            <>
              <div>{t("subject")}</div>
              <div className="font-bold">{subject}</div>
            </>
          ) : null}
          <div>{t("date_colon")}</div>
          <div>
            <time dateTime={quote.date.toISOString()}>
              {formatDate(locale, quote.date, {
                dateStyle: "long",
                timeStyle: quote.whitepaper ? undefined : "long",
                hourCycle: "h24",
              })}
            </time>
          </div>
        </div>
      </header>
      <ContentBoxBody mono={!!quote.email}>{quote.text}</ContentBoxBody>
      <footer className="flex flex-col justify-between gap-2 border-t border-dashed border-taupe px-8 py-4 font-mono text-sm md:flex-row">
        <Link className="text-cardinal hover:underline" href={url}>
          {label}
        </Link>
        <RenderedItemsList
          className="text-xs"
          locale={locale}
          items={quote.categories}
          renderItem={(item) => (
            <Link
              key={item.slug}
              className="text-cardinal hover:underline"
              href={urls(locale).satoshi.quoteCategory(item.slug)}
            >
              {item.name}
            </Link>
          )}
          options={{ type: "unit" }}
        />
      </footer>
    </ContentBox>
  );
}

export default async function QuotesCategoryPage({
  params: { locale, slug },
}: LocaleParams<{ slug: string }>) {
  const { t } = await i18nTranslation(locale);
  const { category, quotes } = await getQuoteCategory(slug);

  return (
    <PageLayout
      t={t}
      locale={locale}
      generateHref={generateHref(slug)}
      breadcrumbs={[
        {
          label: t("complete_satoshi"),
          href: urls(locale).satoshi.index,
        },
        {
          label: t("quotable_satoshi"),
          href: urls(locale).satoshi.quotesIndex,
        },
        {
          label: category.name,
          href: urls(locale).satoshi.quoteCategory(category.slug),
        },
      ]}
    >
      <PageHeader title={category.name} superTitle={t("quotable_satoshi")} />
      <section>
        {quotes.map((q) => (
          <SatoshiQuote key={q.text} t={t} locale={locale} quote={q} />
        ))}
      </section>
    </PageLayout>
  );
}

export async function generateStaticParams() {
  const categories = await getQuoteCategories();
  return getLocaleParams((locale) =>
    categories.map((c) => ({ locale, slug: c.slug })),
  );
}
