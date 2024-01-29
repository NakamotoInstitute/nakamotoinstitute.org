import { Metadata } from "next";
import Link from "next/link";

import { getSatoshiEmailsBySource } from "@/lib/api/emails";
import { EmailSource } from "@/lib/api/schemas/emails";
import { zEmailSource } from "@/lib/api/schemas/emails";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";
import { formatEmailSource, otherEmailSource } from "@/utils/strings";

import { IndexPageLayout } from "@satoshi/components/IndexPageLayout";

export const dynamicParams = false;

export async function generateMetadata({
  params: { locale, source },
}: LocaleParams<{ source: EmailSource }>): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  return {
    title: t("{{source}} Emails", { source: formatEmailSource(source) }),
  };
}

export default async function EmailsSourceIndex({
  params: { locale, source },
}: LocaleParams<{ source: EmailSource }>) {
  const emails = await getSatoshiEmailsBySource(source);
  const generateHref = (l: Locale) =>
    urls(l).satoshi.emails.sourceIndex(source);

  const otherSource = otherEmailSource(source);

  const navLinks = {
    main: {
      label: "View threads",
      href: urls(locale).satoshi.emails.sourceThreadsIndex(source),
    },
    left: {
      label: "All emails",
      href: urls(locale).satoshi.emails.index,
      sublink: {
        label: "Threads",
        href: urls(locale).satoshi.emails.threadsIndex,
      },
    },
    right: {
      label: formatEmailSource(otherSource, true),
      href: urls(locale).satoshi.emails.sourceIndex(otherSource),
      sublink: {
        label: "Threads",
        href: urls(locale).satoshi.emails.sourceThreadsIndex(otherSource),
      },
    },
  };

  return (
    <IndexPageLayout
      title={`${formatEmailSource(source)} Emails`}
      locale={locale}
      generateHref={generateHref}
      navLinks={navLinks}
    >
      <ul>
        {emails.map((e) => (
          <li key={e.satoshiId}>
            <Link
              href={urls(locale).satoshi.emails.sourceEmail(
                e.source,
                e.satoshiId.toString(),
              )}
            >
              {e.subject}
            </Link>{" "}
            <em>
              (
              {formatDate(locale, e.date, {
                dateStyle: "medium",
                timeStyle: "long",
                hourCycle: "h24",
              })}
              )
            </em>
          </li>
        ))}
      </ul>
    </IndexPageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams((locale) =>
    zEmailSource.options.map((source) => ({ locale, source })),
  );
}
