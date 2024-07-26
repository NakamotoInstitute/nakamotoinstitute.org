import clsx from "clsx";
import { TFunction } from "i18next";
import Link from "next/link";
import { ElementType } from "react";
import { UrlObject } from "url";

import { formatDate } from "@/utils/dates";

export type ContentBoxProps = {
  as?: ElementType;
  id?: string;
  className?: string;
  alternate?: boolean;
  children: React.ReactNode;
};

export async function ContentBox({
  as: WrapperComponent = "div",
  id,
  className,
  alternate = false,
  children,
}: ContentBoxProps) {
  return (
    <WrapperComponent
      id={id}
      className={clsx(
        "drop-shadow-sm",
        alternate ? "bg-sand" : "bg-white",
        className,
      )}
    >
      {children}
    </WrapperComponent>
  );
}

export type ContentBoxHeaderProps = {
  t: TFunction<string, string>;
  locale: Locale;
  satoshi?: boolean;
  source?: string;
  sourceId?: string;
  from?: string;
  subject: string;
  date: Date;
};

export async function ContentBoxHeader({
  t,
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
      {source || sourceId ? (
        <div className="flex justify-between border-b border-dashed border-taupe px-8 py-2">
          {source ? <div className="font-bold">{source}</div> : null}
          {sourceId ? (
            <Link
              className="text-cardinal hover:underline"
              href={{ hash: sourceId }}
            >
              #{sourceId}
            </Link>
          ) : null}
        </div>
      ) : null}
      <div className="grid grid-cols-[auto_1fr] gap-x-4 px-8 py-2">
        {from ? (
          <>
            <div>{t("from")}</div>
            <div>{from}</div>
          </>
        ) : null}
        <div>{t("subject")}</div>
        <div className="font-bold">{subject}</div>
        <div>{t("date_colon")}</div>
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
  mono?: boolean;
  className?: string;
  children: React.ReactNode;
};

export async function ContentBoxBody({
  className,
  mono,
  children,
}: ContentBoxBodyProps) {
  return (
    <section className={clsx(className, "px-8 py-4", mono && "font-mono")}>
      {children}
    </section>
  );
}

export type ContentBoxFooterProps = {
  t: TFunction<string, string>;
  hrefs: {
    original: string;
    thread?: UrlObject;
    permalink?: string;
  };
};

export async function ContentBoxFooter({
  t,
  hrefs: { original, thread, permalink },
}: ContentBoxFooterProps) {
  return (
    <footer className="flex justify-between border-t border-dashed border-taupe px-8 py-4 font-mono text-sm text-cardinal">
      <Link className="text-cardinal hover:underline" href={original}>
        View original
      </Link>
      {thread ? (
        <Link className="text-cardinal hover:underline" href={thread}>
          {t("view_in_thread")}
        </Link>
      ) : null}
      {permalink ? (
        <Link className="text-cardinal hover:underline" href={permalink}>
          {t("permalink")}
        </Link>
      ) : null}
    </footer>
  );
}
