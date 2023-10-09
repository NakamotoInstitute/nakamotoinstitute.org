import { Trans } from "react-i18next/TransWithoutContext";
import { AuthorsLinks } from "@/app/components";
import { formatDocDate, formatTimeAttr } from "@/utils/dates";
import { i18nTranslation } from "@/lib/i18n";
import { Document } from "@/lib/api/schemas";

type DocHeaderProps = {
  locale: Locale;
  doc: Document;
};

export async function DocHeader({ locale, doc }: DocHeaderProps) {
  const { t } = await i18nTranslation(locale);

  return (
    <>
      <header className="mt-17 mx-auto max-w-4xl text-center">
        <h1
          className="mb-6 text-7xl font-medium"
          dangerouslySetInnerHTML={{ __html: doc.displayTitle ?? doc.title }}
        />
        {doc.subtitle ? (
          <p className="mb-6 text-xl italic">{doc.subtitle}</p>
        ) : null}
        <p className="text-2xl font-medium">
          <Trans
            t={t}
            i18nKey="By <authors />"
            components={{
              authors: (
                <AuthorsLinks
                  as={"span"}
                  locale={locale}
                  authors={doc.authors}
                />
              ),
            }}
          />
        </p>
        <p className="text-xl font-medium italic opacity-60">
          <time dateTime={formatTimeAttr(doc.date, doc.granularity)}>
            {formatDocDate(locale, doc.date, doc.granularity)}
          </time>
        </p>
        {doc.image ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            className="mx-auto block rounded-sm pt-6"
            src={`/img/library/${doc.slug}/${doc.image}`}
            alt={doc.imageAlt ?? ""}
          />
        ) : null}
      </header>
      <hr className="mx-auto my-12 w-12 border-night border-opacity-40" />
    </>
  );
}
