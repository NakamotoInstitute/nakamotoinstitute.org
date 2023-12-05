import { PageLayout } from "@/app/components/PageLayout";
import { LinkedItemsList } from "@/app/components/LinkedItemsList";
import { PageHeader } from "@/app/components/PageHeader";
import { getQuoteCategories, getQuoteCategory } from "@/lib/api/quotes";
import { Quote } from "@/lib/api/schemas/quotes";
import { getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";
import Link from "next/link";

export async function generateMetadata({
  params: { slug },
}: LocaleParams<{ slug: string }>) {
  const { category } = await getQuoteCategory(slug);
  return {
    title: category.name,
  };
}

type SatoshiQuoteProps = {
  locale: Locale;
  quote: Quote;
};

function SatoshiQuote({ locale, quote }: SatoshiQuoteProps) {
  let subject: string;
  let url: string;
  let label: string;

  if (quote.whitepaper) {
    subject = "Bitcoin: A Peer-to-Peer Electronic Cash System";
    url = urls("en").library.doc("bitcoin");
    label = "View whitepaper";
  } else if (quote.post) {
    subject = quote.post.subject;
    url = urls(locale).satoshi.posts.sourcePost(
      quote.post.source,
      quote.post.satoshiId.toString(),
    );
    label = "View post";
  } else if (quote.email) {
    subject = quote.email.subject;
    url = urls(locale).satoshi.emails.sourceEmail(
      quote.email.source,
      quote.email.satoshiId.toString(),
    );
    label = "View email";
  } else {
    return null;
  }

  return (
    <article className="border-b border-night py-4 first:pt-0 last:border-b-0">
      <h2 className="text-2xl">{subject}</h2>
      <p>
        <time>{formatDate(locale, quote.date)}</time> -{" "}
        <Link href={url}>{label}</Link>
      </p>
      <p className="py-2">{quote.text}</p>
      <LinkedItemsList
        classes={{ root: "text-sm" }}
        locale={locale}
        items={quote.categories}
        urlFunc={(_locale, _slug) => urls(_locale).satoshi.quoteCategory(_slug)}
        options={{ type: "unit" }}
      />
    </article>
  );
}

export default async function QuotesCategoryPage({
  params: { locale, slug },
}: LocaleParams<{ slug: string }>) {
  const { category, quotes } = await getQuoteCategory(slug);
  const generateHref = (l: Locale) => urls(l).satoshi.quoteCategory(slug);

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title={category.name} superTitle="The Quotable Satoshi" />
      <section>
        {quotes.map((q) => (
          <SatoshiQuote key={q.text} locale={locale} quote={q} />
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
