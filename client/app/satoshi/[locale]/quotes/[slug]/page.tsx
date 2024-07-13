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
  let subject: string;
  let url: string;
  let label: string;

  if (quote.whitepaper) {
    subject = t("bitcoin_title");
    url = urls("en").library.doc("bitcoin");
    label = t("view_whitepaper");
  } else if (quote.post) {
    subject = quote.post.subject;
    url = urls(locale).satoshi.posts.sourcePost(
      quote.post.source,
      quote.post.satoshiId.toString(),
    );
    label = t("view_post");
  } else if (quote.email) {
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
    <article className="border-b py-4 first:pt-0 last:border-b-0">
      <h2 className="text-2xl">{subject}</h2>
      <p>
        <time>{formatDate(locale, quote.date)}</time> -{" "}
        <Link href={url}>{label}</Link>
      </p>
      <p className="py-2">{quote.text}</p>
      <RenderedItemsList
        className="text-sm"
        locale={locale}
        items={quote.categories}
        renderItem={(item) => (
          <Link
            key={item.slug}
            href={urls(locale).satoshi.quoteCategory(item.slug)}
          >
            {item.name}
          </Link>
        )}
        options={{ type: "unit" }}
      />
    </article>
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
