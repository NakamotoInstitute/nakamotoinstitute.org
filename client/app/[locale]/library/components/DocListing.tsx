import { TFunction } from "i18next";
import Link from "next/link";

import { AuthorsLinks } from "@/app/components/AuthorsLinks";
import { DocumentIndex } from "@/lib/api/schemas/library";
import { urls } from "@/lib/urls";
import { formatDocDate, formatTimeAttr } from "@/utils/dates";

import { DocFormatChips } from "./DocFormats";

type DocListingProps = {
  doc: DocumentIndex;
  locale: Locale;
  t: TFunction<string, string>;
};

export async function DocListing({ doc, locale, t }: DocListingProps) {
  return (
    <article className="border-b border-solid py-4 first:pt-0 last:border-b-0">
      <header>
        <h2 className="text-xl font-bold">
          <Link href={urls(locale).library.doc(doc.slug)}>{doc.title}</Link>
        </h2>
        <p>
          <AuthorsLinks as="span" authors={doc.authors} locale={locale} />
          {" • "}
          <time dateTime={formatTimeAttr(doc.date, doc.granularity)}>
            {formatDocDate(locale, doc.date, doc.granularity)}
          </time>
        </p>
      </header>
      <section>
        <DocFormatChips t={t} className="pt-1" doc={doc} />
      </section>
    </article>
  );
}
