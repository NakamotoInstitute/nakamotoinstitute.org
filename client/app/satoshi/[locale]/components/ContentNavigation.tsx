import { SatoshiEmail } from "@/lib/api/schemas/emails";
import { SatoshiForumPost } from "@/lib/api/schemas/posts";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { urls } from "@/lib/urls";
import Link from "next/link";

type NavProps<Data> = {
  locale: Locale;
  previous: Data | null;
  next: Data | null;
};

type EmailNavProps = NavProps<SatoshiEmail>;

type PostNavProps = NavProps<SatoshiForumPost>;

type ContentNavigationProps = {
  locale: Locale;
  prevHref?: string;
  nextHref?: string;
  indexHref: string;
};

const ContentNavigation = async ({
  locale,
  prevHref,
  nextHref,
  indexHref,
}: ContentNavigationProps) => {
  const { t } = await i18nTranslation(locale);
  return (
    <div className="flex justify-center gap-4">
      {prevHref ? (
        <Link className="border-r-1 border-night pr-4" href={prevHref}>
          {t("Previous")}
        </Link>
      ) : null}
      <Link href={indexHref}>{t("Index")}</Link>
      {nextHref ? (
        <Link className="border-l-1 border-night pl-4" href={nextHref}>
          {t("Next")}
        </Link>
      ) : null}
    </div>
  );
};

export const EmailNavigation = ({ locale, previous, next }: EmailNavProps) => {
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

  const indexHref = urls(locale).satoshi.emails.index;

  return (
    <ContentNavigation
      locale={locale}
      prevHref={prevHref}
      nextHref={nextHref}
      indexHref={indexHref}
    />
  );
};

export const PostNavigation = ({ locale, previous, next }: PostNavProps) => {
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

  const indexHref = urls(locale).satoshi.emails.index;

  return (
    <ContentNavigation
      locale={locale}
      prevHref={prevHref}
      nextHref={nextHref}
      indexHref={indexHref}
    />
  );
};
