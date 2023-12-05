import Link from "next/link";
import { AuthorsLinks } from "@/app/components/AuthorsLinks";
import { DocumentIndex } from "@/lib/api/schemas/library";
import { urls } from "@/lib/urls";
import { formatDocDate, formatTimeAttr } from "@/utils/dates";
import { DocFormats } from "./DocFormats";

export async function DocListing({
  doc,
  locale,
}: {
  doc: DocumentIndex;
  locale: Locale;
}) {
  return (
    <article className="border-b border-solid border-night py-4 first:pt-0 last:border-b-0">
      <header>
        <h2 className="text-2xl">
          <Link href={urls(locale).library.doc(doc.slug)}>{doc.title}</Link>
        </h2>
        <AuthorsLinks authors={doc.authors} locale={locale} />
        <p>
          <time dateTime={formatTimeAttr(doc.date, doc.granularity)}>
            {formatDocDate(locale, doc.date, doc.granularity)}
          </time>
        </p>
      </header>
      <section>
        <DocFormats className="pt-1" locale={locale} doc={doc} />
      </section>
    </article>
  );
}
