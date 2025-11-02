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
    <div className="mb-4 flex flex-col last:mb-0 md:mb-3 md:flex-row md:gap-4">
      <div className="shrink-0 grow basis-1/6 font-bold md:text-right">
        {label}
      </div>
      <div className="shrink-0 grow basis-5/6">{children}</div>
    </div>
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
    <article className="border-taupe-light border-t border-dashed pt-7 pb-5">
      <h2 className="mb-2.5 text-2xl font-bold">{title}</h2>
      <div>
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
          <Link
            className="text-cardinal wrap-break-word hover:underline"
            href={source}
          >
            {source}
          </Link>
        </CodeTableRow>
      </div>
    </article>
  );
}
