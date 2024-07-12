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
    alternates: {
      canonical: generateHref(locale),
      languages,
    },
  };
}

export default async function EmailsIndex({
  params: { locale },
}: LocaleParams) {
  const { t } = await i18nTranslation(locale);
  const emails = await getSatoshiEmails();

  return (
    <IndexPageLayout
      t={t}
      locale={locale}
      generateHref={generateHref}
      title={t("emails")}
      sourceLinks={[
        {
          name: t("all"),
          active: true,
        },
        {
          name: formatEmailSource("cryptography"),
          href: urls(locale).satoshi.emails.sourceIndex("cryptography"),
        },
        {
          name: formatEmailSource("bitcoin-list"),
          href: urls(locale).satoshi.emails.sourceIndex("bitcoin-list"),
        },
      ]}
      toggleLinks={{
        active: "individual",
        href: urls(locale).satoshi.emails.threadsIndex,
      }}
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
