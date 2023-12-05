import { ReactNode } from "react";
import { CodeDownload, CodeDownloadProps } from "./CodeDownload";
import Link from "next/link";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { formatDate } from "@/utils/dates";

type CodeTableRowProps = {
  label: string;
  children: ReactNode;
};

function CodeTableRow({ label, children }: CodeTableRowProps) {
  return (
    <>
      <div className="font-bold md:text-right">{label}</div>
      <div>{children}</div>
    </>
  );
}

type CodeTableProps = {
  locale: Locale;
  title: string;
  date: Date;
  dateRef?: string;
  downloads: CodeDownloadProps | CodeDownloadProps[];
  notes?: string;
  source: string;
};

export async function CodeTable({
  locale,
  title,
  date,
  dateRef,
  downloads,
  notes,
  source,
}: CodeTableProps) {
  const { t } = await i18nTranslation(locale);
  return (
    <article className="my-4 first:mt-0 last:mb-0">
      <h2 className="text-2xl font-medium">{title}</h2>
      <div className="grid grid-cols-1 md:grid-cols-[1fr,5fr] md:gap-4">
        <CodeTableRow label={t("Date")}>
          {formatDate(locale, date)}
          {dateRef ? (
            <span className="ml-1">
              (<Link href={dateRef}>?</Link>)
            </span>
          ) : null}
        </CodeTableRow>
        <CodeTableRow label={t("Download")}>
          {Array.isArray(downloads) ? (
            downloads.map((download, index) => (
              <CodeDownload key={index} {...download} />
            ))
          ) : (
            <CodeDownload {...downloads} />
          )}
        </CodeTableRow>
        {notes ? (
          <CodeTableRow label={t("Release notes")}>{notes}</CodeTableRow>
        ) : null}
        <CodeTableRow label={t("Source")}>
          <Link className="break-words" href={source}>
            {source}
          </Link>
        </CodeTableRow>
      </div>
    </article>
  );
}
