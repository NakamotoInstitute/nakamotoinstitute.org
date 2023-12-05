import { PageLayout } from "@/app/components/PageLayout";
import { PageHeader } from "@/app/components/PageHeader";
import { getQuoteCategories } from "@/lib/api/quotes";
import { QuoteCategory } from "@/lib/api/schemas/quotes";
import { getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import Link from "next/link";

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
  const categories = await getQuoteCategories();
  const generateHref = (l: Locale) => urls(l).satoshi.quotesIndex;

  const halfLength = Math.ceil(categories.length / 2);
  const firstColumn = categories.slice(0, halfLength);
  const secondColumn = categories.slice(halfLength);

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title="The Quotable Satoshi">
        <figure>
          <blockquote>
            It&lsquo;s very attractive to the libertarian viewpoint if we can
            explain it properly.
            <br />
            <em>I&lsquo;m better with code than with words though.</em>
          </blockquote>
          <figcaption>
            <Link href="">Satoshi Nakamoto</Link>, 11/14/2008
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
          Special thanks to{" "}
          <Link href="https://www.buybitcoinworldwide.com/">
            Jordan Tuwiner
          </Link>{" "}
          for indexing quotations.
        </p>
        <p>
          If there is a quotation or category you would like to add, please{" "}
          <Link href={urls(locale).contact}>contact us</Link> or submit a pull
          request on <Link href={urls(locale).github}>GitHub</Link>.
        </p>
      </footer>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
