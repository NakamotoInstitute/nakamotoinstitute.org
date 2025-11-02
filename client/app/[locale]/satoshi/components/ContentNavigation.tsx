import clsx from "clsx";
import { TFunction } from "i18next";

import { ArrowLink } from "@/app/components/ArrowButton";
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

type ContentNavigationProps = {
  id: number;
  prevHref?: string;
  nextHref?: string;
  className?: string;
};

const ContentNavigation = async ({
  id,
  prevHref,
  nextHref,
  className,
}: ContentNavigationProps) => {
  return (
    <div className={clsx(className, "flex items-center gap-x-4")}>
      <ArrowLink href={prevHref} direction="left" />
      <div>{id}</div>
      <ArrowLink href={nextHref} direction="right" />
    </div>
  );
};

type NavProps<Data, Source> = {
  t: TFunction<string, string>;
  locale: Locale;
  id: number;
  previous: Data | null;
  next: Data | null;
  className?: string;
  source: Source;
  reverse?: boolean;
};

type EmailNavProps = NavProps<SatoshiEmail, EmailSource>;

export const EmailNavigation = async ({
  locale,
  id,
  previous,
  next,
  className,
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

  return (
    <ContentNavigation
      className={className}
      id={id}
      prevHref={prevHref}
      nextHref={nextHref}
    />
  );
};

export type EmailThreadNavProps = NavProps<EmailThread, EmailSource>;

export const EmailThreadNavigation = async ({
  locale,
  id,
  previous,
  next,
  className,
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

  return (
    <ContentNavigation
      className={className}
      id={id}
      prevHref={prevHref}
      nextHref={nextHref}
    />
  );
};

type PostNavProps = NavProps<SatoshiForumPost, ForumPostSource>;

export const PostNavigation = async ({
  locale,
  id,
  previous,
  next,
  className,
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

  return (
    <ContentNavigation
      className={className}
      id={id}
      prevHref={prevHref}
      nextHref={nextHref}
    />
  );
};

export type PostThreadNavProps = NavProps<ForumThread, ForumPostSource>;

export const PostThreadNavigation = async ({
  locale,
  id,
  previous,
  next,
  className,
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

  return (
    <ContentNavigation
      className={className}
      id={id}
      prevHref={prevHref}
      nextHref={nextHref}
    />
  );
};
