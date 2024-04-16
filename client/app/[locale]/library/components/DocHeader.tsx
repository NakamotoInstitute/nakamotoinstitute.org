import { TFunction } from "i18next";

import { AuthorsLinks } from "@/app/components/AuthorsLinks";
import { Document } from "@/lib/api/schemas/library";
import { formatDocDate, formatTimeAttr } from "@/utils/dates";

import { DocFormatLinks } from "./DocFormats";

type DocHeaderProps = {
  t: TFunction<string, string>;
  locale: Locale;
  doc: Document;
};

export async function DocHeader({ t, locale, doc }: DocHeaderProps) {
  return (
    <>
      <header className="mx-auto mt-6 max-w-4xl text-center">
        <h1
          className="mb-2 text-5xl font-medium"
          dangerouslySetInnerHTML={{ __html: doc.displayTitle ?? doc.title }}
        />
        {doc.subtitle ? (
          <p className="mb-6 text-xl italic">{doc.subtitle}</p>
        ) : null}
        <AuthorsLinks
          className="mb-2 text-3xl font-medium"
          itemClassName="text-gray-500 hover:text-gray-600"
          locale={locale}
          authors={doc.authors}
        />
        <p className="text-2xl font-medium">
          <time
            dateTime={formatTimeAttr(doc.date, doc.granularity)}
            dangerouslySetInnerHTML={{
              __html:
                doc.displayDate ??
                formatDocDate(locale, doc.date, doc.granularity),
            }}
          />
        </p>
        {doc.image ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            className="mx-auto block rounded-sm pt-6"
            src={doc.image}
            alt={doc.imageAlt ?? ""}
          />
        ) : null}
      </header>
      <hr className="mx-auto my-6 w-12 border border-opacity-40" />
      {doc.content ? (
        <>
          <DocFormatLinks
            t={t}
            classes={{ root: "justify-center gap-3 font-medium" }}
            doc={doc}
          />
          <hr className="mx-auto my-6 w-12 border-opacity-40" />
        </>
      ) : (
        <DocFormatLinks
          t={t}
          classes={{
            root: "text-center flex-col gap-3",
            link: "text-lg font-medium",
          }}
          doc={doc}
        />
      )}
    </>
  );
}
