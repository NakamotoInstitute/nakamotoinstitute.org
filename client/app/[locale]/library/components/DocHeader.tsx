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
          className="mb-4 text-4xl font-medium md:mb-6 md:text-7xl"
          dangerouslySetInnerHTML={{ __html: doc.displayTitle ?? doc.title }}
        />
        {doc.subtitle ? (
          <p className="mb-4 text-xl italic md:mb-6">{doc.subtitle}</p>
        ) : null}
        <AuthorsLinks
          className="small-caps mb-1 text-xl font-bold md:mb-4 md:text-2xl"
          itemClassName="text-dark"
          locale={locale}
          authors={doc.authors}
        />
        <p className="small-caps text-xl font-bold opacity-60 md:text-2xl">
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
