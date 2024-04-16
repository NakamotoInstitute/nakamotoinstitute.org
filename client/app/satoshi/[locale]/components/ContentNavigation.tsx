import clsx from "clsx";
import { TFunction } from "i18next";
import Link from "next/link";

import {
  EmailSource,
  EmailThread,
  SatoshiEmail,
} from "@/lib/api/schemas/emails";
import {
  ForumPostSource,
  ForumThread,
  SatoshiForumPost,
} from "@/lib/api/schemas/posts";
import { urls } from "@/lib/urls";
import { formatEmailSource, formatPostSource } from "@/utils/strings";

type ContentNavigationProps = {
  t: TFunction<string, string>;
  mainLink: AnchorProps;
  prevHref?: string;
  nextHref?: string;
  indexLink: AnchorProps;
  className?: string;
  reverse?: boolean;
};

const ContentNavigation = async ({
  t,
  mainLink,
  prevHref,
  nextHref,
  indexLink,
  className,
  reverse,
}: ContentNavigationProps) => {
  return (
    <div
      className={clsx(
        className,
        "grid grid-cols-[1fr_max-content_1fr] grid-rows-2 gap-y-2 text-center",
      )}
    >
      <div className={clsx("col-span-3", reverse && "order-2")}>
        <Link href={mainLink.href}>{mainLink.text}</Link>
      </div>
      <div
        className={clsx(
          "pr-2 text-right",
          !!prevHref && "border-r border-gray-400",
        )}
      >
        {prevHref ? <Link href={prevHref}>{t("Previous")}</Link> : null}
      </div>
      <div className="px-2">
        <Link href={indexLink.href}>{indexLink.text}</Link>
      </div>
      <div
        className={clsx(
          "pl-2 text-left",
          !!nextHref && "border-l border-gray-400",
        )}
      >
        {nextHref ? <Link href={nextHref}>{t("Next")}</Link> : null}
      </div>
    </div>
  );
};

type NavProps<Data, Source> = {
  t: TFunction<string, string>;
  locale: Locale;
  previous: Data | null;
  next: Data | null;
  className?: string;
  source: Source;
  reverse?: boolean;
};

type EmailNavProps = NavProps<SatoshiEmail, EmailSource>;

export const EmailNavigation = async ({
  t,
  locale,
  source,
  previous,
  next,
  className,
  reverse,
}: EmailNavProps) => {
  const prevHref = previous
    ? urls(locale).satoshi.emails.sourceEmail(
        previous.source,
        previous.satoshiId.toString(),
      )
    : undefined;

  const nextHref = next
    ? urls(locale).satoshi.emails.sourceEmail(
        next.source,
        next.satoshiId.toString(),
      )
    : undefined;

  const indexHref = urls(locale).satoshi.emails.sourceIndex(source);

  return (
    <ContentNavigation
      t={t}
      className={className}
      mainLink={{
        href: urls(locale).satoshi.emails.index,
        text: t("All emails"),
      }}
      prevHref={prevHref}
      nextHref={nextHref}
      indexLink={{
        href: indexHref,
        text: t("{{source}} index", {
          source: formatEmailSource(source, true),
        }),
      }}
      reverse={reverse}
    />
  );
};

export type EmailThreadNavProps = NavProps<EmailThread, EmailSource>;

export const EmailThreadNavigation = async ({
  t,
  locale,
  source,
  previous,
  next,
  className,
  reverse,
}: EmailThreadNavProps) => {
  const prevHref = previous
    ? urls(locale).satoshi.emails.sourceThreadsDetail(
        previous.source,
        previous.id.toString(),
      )
    : undefined;

  const nextHref = next
    ? urls(locale).satoshi.emails.sourceThreadsDetail(
        next.source,
        next.id.toString(),
      )
    : undefined;

  const indexHref = urls(locale).satoshi.emails.sourceThreadsIndex(source);

  return (
    <ContentNavigation
      t={t}
      className={className}
      mainLink={{
        href: urls(locale).satoshi.emails.threadsIndex,
        text: t("All email threads"),
      }}
      prevHref={prevHref}
      nextHref={nextHref}
      indexLink={{
        href: indexHref,
        text: t("{{source}} index", {
          source: formatEmailSource(source, true),
        }),
      }}
      reverse={reverse}
    />
  );
};

type PostNavProps = NavProps<SatoshiForumPost, ForumPostSource>;

export const PostNavigation = async ({
  t,
  locale,
  source,
  previous,
  next,
  className,
  reverse,
}: PostNavProps) => {
  const prevHref = previous
    ? urls(locale).satoshi.posts.sourcePost(
        previous.source,
        previous.satoshiId.toString(),
      )
    : undefined;

  const nextHref = next
    ? urls(locale).satoshi.posts.sourcePost(
        next.source,
        next.satoshiId.toString(),
      )
    : undefined;

  const indexHref = urls(locale).satoshi.posts.sourceIndex(source);

  return (
    <ContentNavigation
      t={t}
      className={className}
      mainLink={{
        href: urls(locale).satoshi.posts.index,
        text: t("All posts"),
      }}
      prevHref={prevHref}
      nextHref={nextHref}
      indexLink={{
        href: indexHref,
        text: t("{{source}} posts", { source: formatPostSource(source) }),
      }}
      reverse={reverse}
    />
  );
};

export type PostThreadNavProps = NavProps<ForumThread, ForumPostSource>;

export const PostThreadNavigation = async ({
  t,
  locale,
  source,
  previous,
  next,
  className,
  reverse,
}: PostThreadNavProps) => {
  const prevHref = previous
    ? urls(locale).satoshi.posts.sourceThreadsDetail(
        previous.source,
        previous.id.toString(),
      )
    : undefined;

  const nextHref = next
    ? urls(locale).satoshi.posts.sourceThreadsDetail(
        next.source,
        next.id.toString(),
      )
    : undefined;

  const indexHref = urls(locale).satoshi.posts.sourceThreadsIndex(source);

  return (
    <ContentNavigation
      t={t}
      className={className}
      mainLink={{
        href: urls(locale).satoshi.emails.threadsIndex,
        text: t("All post threads"),
      }}
      prevHref={prevHref}
      nextHref={nextHref}
      indexLink={{
        href: indexHref,
        text: t("{{source}} index", { source: formatPostSource(source) }),
      }}
      reverse={reverse}
    />
  );
};
