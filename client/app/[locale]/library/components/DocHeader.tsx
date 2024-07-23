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
      <header className="mx-auto text-center">
        <h1
          className="mb-4 text-4xl font-medium leading-[1.1] md:mb-6 md:text-7xl"
          dangerouslySetInnerHTML={{ __html: doc.displayTitle ?? doc.title }}
        />
        {doc.subtitle ? (
          <p className="mb-4 text-2xl font-semibold md:mb-6 md:text-3xl">
            {doc.subtitle}
          </p>
        ) : null}
        <AuthorsLinks
          className="mb-1 text-xl font-bold small-caps md:mb-4 md:text-2xl"
          itemClassName="text-dark"
          locale={locale}
          authors={doc.authors}
        />
        <p className="text-xl font-bold opacity-60 small-caps md:text-2xl">
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
            className="mx-auto mt-6 block max-w-screen-sm"
            src={doc.image}
            alt={doc.imageAlt ?? ""}
          />
        ) : null}
      </header>
      <hr className="mx-auto my-4 w-12 md:my-6" />
      {doc.content ? (
        <>
          <DocFormatLinks
            t={t}
            classes={{ root: "justify-center gap-3 font-medium" }}
            doc={doc}
          />
          <hr className="mx-auto my-6 w-12" />
        </>
      ) : (
        <DocFormatLinks
          t={t}
          classes={{ root: "justify-center gap-3 font-medium" }}
          doc={doc}
        />
      )}
    </>
  );
}
