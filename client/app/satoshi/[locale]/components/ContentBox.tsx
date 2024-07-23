import clsx from "clsx";
import { TFunction } from "i18next";
import Link from "next/link";
import { UrlObject } from "url";

import { formatDate } from "@/utils/dates";

export type ContentBoxProps = {
  alternate?: boolean;
  children: React.ReactNode;
};

export async function ContentBox({
  alternate = false,
  children,
}: ContentBoxProps) {
  return (
    <div
      className={clsx(
        "drop-shadow-sm",
        alternate ? "bg-taupe-light" : "bg-white",
      )}
    >
      {children}
    </div>
  );
}

export type ContentBoxHeaderProps = {
  locale: Locale;
  satoshi?: boolean;
  source: string;
  sourceId: string;
  from: string;
  subject: string;
  date: Date;
};

export async function ContentBoxHeader({
  locale,
  satoshi = true,
  source,
  sourceId,
  from,
  subject,
  date,
}: ContentBoxHeaderProps) {
  return (
    <header
      className={clsx(
        "border-b border-dashed border-taupe font-mono",
        satoshi && "bg-dandelion",
      )}
    >
      <div className="flex justify-between border-b border-dashed border-taupe px-8 py-2">
        <div className="font-bold">{source}</div>
        <div>#{sourceId}</div>
      </div>
      <div className="grid grid-cols-[auto_1fr] gap-x-4 px-8 py-2">
        <div>From:</div>
        <div>{from}</div>
        <div>Subject:</div>
        <div className="font-bold">{subject}</div>
        <div>Date:</div>
        <div>
          <time dateTime={date.toISOString()}>
            {formatDate(locale, date, {
              dateStyle: "long",
              timeStyle: "long",
              hourCycle: "h24",
            })}
          </time>
        </div>
      </div>
    </header>
  );
}

export type ContentBoxBodyProps = {
  children: React.ReactNode;
};

export async function ContentBoxBody({ children }: ContentBoxBodyProps) {
  return <section className="px-8 py-4">{children}</section>;
}

export type ContentBoxFooterProps = {
  t: TFunction<string, string>;
  hrefs: {
    original: string;
    thread?: UrlObject;
  };
};

export async function ContentBoxFooter({
  t,
  hrefs: { original, thread },
}: ContentBoxFooterProps) {
  return (
    <footer className="flex justify-between border-t border-dashed border-taupe px-8 py-4 font-mono text-cardinal">
      <Link className="text-cardinal hover:underline" href={original}>
        View original
      </Link>
      {thread ? (
        <Link className="text-cardinal hover:underline" href={thread}>
          {t("view_in_thread")}
        </Link>
      ) : null}
    </footer>
  );
}
