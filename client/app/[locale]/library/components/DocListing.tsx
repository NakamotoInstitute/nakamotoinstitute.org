import clsx from "clsx";
import { TFunction } from "i18next";
import Link from "next/link";

import { AuthorsLinks } from "@/app/components/AuthorsLinks";
import { DocumentIndex } from "@/lib/api/schemas/library";
import { urls } from "@/lib/urls";
import { formatDocDate, formatTimeAttr } from "@/utils/dates";

import { DocFormatChips } from "./DocFormats";

type DocListingProps = {
  doc: DocumentIndex;
  className?: string;
  locale: Locale;
  t: TFunction<string, string>;
};

export async function DocListing({
  doc,
  className,
  locale,
  t,
}: DocListingProps) {
  return (
    <article
      className={clsx(
        "border-t border-dashed border-taupe-light py-4 last:border-b",
        className,
      )}
    >
      <header className="mb-1 md:mb-2">
        <h2 className="font-bold md:text-xl">
          <Link
            className="text-cardinal hover:underline"
            href={urls(locale).library.doc(doc.slug)}
          >
            {doc.title}
          </Link>
        </h2>
        <p className="small-caps max-sm:text-sm">
          <AuthorsLinks as="span" authors={doc.authors} locale={locale} />
          <span className="mx-1">•</span>
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
