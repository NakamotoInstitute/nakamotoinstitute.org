import { AuthorsLinks } from "@/app/components/AuthorsLinks";
import { Document } from "@/lib/api/schemas/library";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { formatDocDate, formatTimeAttr } from "@/utils/dates";

import { DocFormatLinks } from "./DocFormats";

type DocHeaderProps = {
  locale: Locale;
  doc: Document;
};

export async function DocHeader({ locale, doc }: DocHeaderProps) {
  const { t } = await i18nTranslation(locale);

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
          <time dateTime={formatTimeAttr(doc.date, doc.granularity)}>
            {formatDocDate(locale, doc.date, doc.granularity)}
          </time>
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
            classes={{ root: "justify-center gap-3 font-medium" }}
            locale={locale}
            doc={doc}
          />
          <hr className="mx-auto my-6 w-12 border-opacity-40" />
        </>
      ) : (
        <DocFormatLinks
          classes={{
            root: "text-center flex-col gap-3",
            link: "text-lg font-medium",
          }}
          locale={locale}
          doc={doc}
        />
      )}
    </>
  );
}
