import { Metadata } from "next";
import Link from "next/link";

import { locales } from "@/i18n";
import { getEmailThreadsBySource } from "@/lib/api/emails";
import { EmailSource, zEmailSource } from "@/lib/api/schemas/emails";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";
import { formatEmailSource, otherEmailSource } from "@/utils/strings";

import { IndexPageLayout } from "@satoshi/components/IndexPageLayout";

export const dynamicParams = false;

const generateHref = (source: EmailSource) => (l: Locale) =>
  urls(l).satoshi.emails.sourceThreadsIndex(source);

export async function generateMetadata({
  params: { locale, source },
}: LocaleParams<{ source: EmailSource }>): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs([...locales], generateHref(source));

  return {
    title: t("{{source}} Threads", { source: formatEmailSource(source) }),
    alternates: { languages },
  };
}

export default async function EmailSourceThreadsIndex({
  params: { locale, source },
}: LocaleParams<{ source: EmailSource }>) {
  const { t } = await i18nTranslation(locale);
  const threads = await getEmailThreadsBySource(source);

  const otherSource = otherEmailSource(source);

  const navLinks = {
    main: {
      text: t("View emails"),
      href: urls(locale).satoshi.emails.sourceIndex(source),
    },
    left: {
      text: t("All threads"),
      href: urls(locale).satoshi.emails.threadsIndex,
      sublink: {
        text: t("Emails"),
        href: urls(locale).satoshi.emails.index,
      },
    },
    right: {
      text: formatEmailSource(otherSource, true),
      href: urls(locale).satoshi.emails.sourceThreadsIndex(otherSource),
      sublink: {
        text: t("Emails"),
        href: urls(locale).satoshi.emails.sourceIndex(otherSource),
      },
    },
  };

  return (
    <IndexPageLayout
      t={t}
      title={t("{{source}} Threads", { source: formatEmailSource(source) })}
      locale={locale}
      generateHref={generateHref(source)}
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
