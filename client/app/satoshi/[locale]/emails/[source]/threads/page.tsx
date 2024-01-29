import { Metadata } from "next";
import Link from "next/link";

import { getEmailThreadsBySource } from "@/lib/api/emails";
import { EmailSource, zEmailSource } from "@/lib/api/schemas/emails";
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
    title: t("{{source}} Threads", { source: formatEmailSource(source) }),
  };
}

export default async function EmailSourceThreadsIndex({
  params: { locale, source },
}: LocaleParams<{ source: EmailSource }>) {
  const threads = await getEmailThreadsBySource(source);
  const generateHref = (l: Locale) =>
    urls(l).satoshi.emails.sourceThreadsIndex(source);

  const otherSource = otherEmailSource(source);

  const navLinks = {
    main: {
      label: "View emails",
      href: urls(locale).satoshi.emails.sourceIndex(source),
    },
    left: {
      label: "All threads",
      href: urls(locale).satoshi.emails.threadsIndex,
      sublink: {
        label: "Emails",
        href: urls(locale).satoshi.emails.index,
      },
    },
    right: {
      label: formatEmailSource(otherSource, true),
      href: urls(locale).satoshi.emails.sourceThreadsIndex(otherSource),
      sublink: {
        label: "Emails",
        href: urls(locale).satoshi.emails.sourceIndex(otherSource),
      },
    },
  };

  return (
    <IndexPageLayout
      title={`${formatEmailSource(source)} Threads`}
      locale={locale}
      generateHref={generateHref}
      navLinks={navLinks}
    >
      <ul>
        {threads.map((t) => (
          <li key={t.id}>
            <Link
              href={urls(locale).satoshi.emails.sourceThreadsDetail(
                t.source,
                t.id.toString(),
              )}
            >
              {t.title}
            </Link>{" "}
            <em>({formatDate(locale, t.date)})</em>
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
