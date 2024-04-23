import { Metadata } from "next";
import Link from "next/link";

import { locales } from "@/i18n";
import { getSatoshiEmails } from "@/lib/api/emails";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";
import { formatEmailSource } from "@/utils/strings";

import { IndexPageLayout } from "@satoshi/components/IndexPageLayout";

export const dynamicParams = false;

const generateHref = (l: Locale) => urls(l).satoshi.emails.index;

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs([...locales], generateHref);

  return {
    title: t("emails"),
    alternates: { languages },
  };
}

export default async function EmailsIndex({
  params: { locale },
}: LocaleParams) {
  const { t } = await i18nTranslation(locale);
  const emails = await getSatoshiEmails();

  const navLinks = {
    main: {
      text: t("view_threads"),
      href: urls(locale).satoshi.emails.threadsIndex,
    },
    left: {
      text: formatEmailSource("cryptography", true),
      href: urls(locale).satoshi.emails.sourceIndex("cryptography"),
      sublink: {
        text: t("threads"),
        href: urls(locale).satoshi.emails.sourceThreadsIndex("cryptography"),
      },
    },
    right: {
      text: formatEmailSource("bitcoin-list", true),
      href: urls(locale).satoshi.emails.sourceIndex("bitcoin-list"),
      sublink: {
        text: t("threads"),
        href: urls(locale).satoshi.emails.sourceThreadsIndex("bitcoin-list"),
      },
    },
  };

  return (
    <IndexPageLayout
      t={t}
      title={t("emails")}
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
  return getLocaleParams();
}
