import { TFunction } from "i18next";
import Image from "next/image";

import { AuthorsLinks } from "@/app/components/AuthorsLinks";
import { Document } from "@/lib/api";
import { formatDocDate, formatTimeAttr } from "@/utils/dates";

import { DocFormatLinksContainer, getDocFormatLinks } from "./DocFormats";

type DocHeaderProps = {
  t: TFunction<string, string>;
  locale: Locale;
  doc: Document;
};

export async function DocHeader({ t, locale, doc }: DocHeaderProps) {
  const formatLinks = getDocFormatLinks({ t, locale, doc });

  return (
    <>
      <header className="mx-auto text-center">
        <h1
          className="mb-4 text-4xl leading-[1.1] font-medium md:mb-6 md:text-7xl"
          dangerouslySetInnerHTML={{ __html: doc.displayTitle ?? doc.title }}
        />
        {doc.subtitle ? (
          <p className="mb-4 text-2xl font-semibold md:mb-6 md:text-3xl">
            {doc.subtitle}
          </p>
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
          <div className="relative mx-auto mt-6 h-48 max-w-(--breakpoint-sm) sm:h-60 md:h-80">
            <Image
              className="object-contain"
              src={doc.image}
              alt={doc.imageAlt ?? ""}
              fill
            />
          </div>
        ) : null}
      </header>
      <hr className="mx-auto my-4 w-12 md:my-6" />
      <DocFormatLinksContainer
        links={formatLinks}
        className="justify-center gap-3"
        border={!!doc.content}
      />
    </>
  );
}
