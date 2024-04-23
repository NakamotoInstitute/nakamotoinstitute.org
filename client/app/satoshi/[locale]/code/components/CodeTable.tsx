import { TFunction } from "i18next";
import Link from "next/link";

import { formatDate } from "@/utils/dates";

import { CodeDownload, CodeDownloadProps } from "./CodeDownload";

type CodeTableRowProps = {
  label: string;
  children: React.ReactNode;
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
  t: TFunction<string, string>;
  locale: Locale;
  title: string;
  date: Date;
  dateRef?: string;
  downloads: CodeDownloadProps | CodeDownloadProps[];
  notes?: string;
  source: string;
};

export async function CodeTable({
  t,
  locale,
  title,
  date,
  dateRef,
  downloads,
  notes,
  source,
}: CodeTableProps) {
  return (
    <article className="my-4 first:mt-0 last:mb-0">
      <h2 className="text-2xl font-medium">{title}</h2>
      <div className="grid grid-cols-1 md:grid-cols-[1fr,5fr] md:gap-4">
        <CodeTableRow label={t("date")}>
          {formatDate(locale, date)}
          {dateRef ? (
            <span className="ml-1">
              (<Link href={dateRef}>?</Link>)
            </span>
          ) : null}
        </CodeTableRow>
        <CodeTableRow label={t("download")}>
          {Array.isArray(downloads) ? (
            downloads.map((download, index) => (
              <CodeDownload key={index} {...download} />
            ))
          ) : (
            <CodeDownload {...downloads} />
          )}
        </CodeTableRow>
        {notes ? (
          <CodeTableRow label={t("release_notes")}>{notes}</CodeTableRow>
        ) : null}
        <CodeTableRow label={t("source")}>
          <Link className="break-words" href={source}>
            {source}
          </Link>
        </CodeTableRow>
      </div>
    </article>
  );
}
