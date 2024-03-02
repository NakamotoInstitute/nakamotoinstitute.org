import clsx from "clsx";
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
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { urls } from "@/lib/urls";
import { formatEmailSource, formatPostSource } from "@/utils/strings";

type ContentNavigationProps = {
  locale: Locale;
  mainLink: AnchorProps;
  prevHref?: string;
  nextHref?: string;
  indexLink: AnchorProps;
  className?: string;
  reverse?: boolean;
};

const ContentNavigation = async ({
  locale,
  mainLink,
  prevHref,
  nextHref,
  indexLink,
  className,
  reverse,
}: ContentNavigationProps) => {
  const { t } = await i18nTranslation(locale);
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
  locale: Locale;
  previous: Data | null;
  next: Data | null;
  className?: string;
  source: Source;
  reverse?: boolean;
};

type EmailNavProps = NavProps<SatoshiEmail, EmailSource>;

export const EmailNavigation = ({
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
      className={className}
      locale={locale}
      mainLink={{
        href: urls(locale).satoshi.emails.index,
        text: "All emails",
      }}
      prevHref={prevHref}
      nextHref={nextHref}
      indexLink={{
        href: indexHref,
        text: `${formatEmailSource(source, true)} index`,
      }}
      reverse={reverse}
    />
  );
};

export type EmailThreadNavProps = NavProps<EmailThread, EmailSource>;

export const EmailThreadNavigation = ({
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
      className={className}
      locale={locale}
      mainLink={{
        href: urls(locale).satoshi.emails.threadsIndex,
        text: "All email threads",
      }}
      prevHref={prevHref}
      nextHref={nextHref}
      indexLink={{
        href: indexHref,
        text: `${formatEmailSource(source, true)} index`,
      }}
      reverse={reverse}
    />
  );
};

type PostNavProps = NavProps<SatoshiForumPost, ForumPostSource>;

export const PostNavigation = ({
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
      className={className}
      locale={locale}
      mainLink={{
        href: urls(locale).satoshi.posts.index,
        text: "All posts",
      }}
      prevHref={prevHref}
      nextHref={nextHref}
      indexLink={{
        href: indexHref,
        text: `${formatPostSource(source)} posts`,
      }}
      reverse={reverse}
    />
  );
};

export type PostThreadNavProps = NavProps<ForumThread, ForumPostSource>;

export const PostThreadNavigation = ({
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
      className={className}
      locale={locale}
      mainLink={{
        href: urls(locale).satoshi.emails.threadsIndex,
        text: "All post threads",
      }}
      prevHref={prevHref}
      nextHref={nextHref}
      indexLink={{
        href: indexHref,
        text: `${formatPostSource(source)} index`,
      }}
      reverse={reverse}
    />
  );
};
