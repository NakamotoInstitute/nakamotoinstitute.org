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

import { SourceLink } from "@satoshi/components/IndexHeader";
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
    title: t("source_threads", { source: formatEmailSource(source) }),
    alternates: {
      canonical: generateHref(source)(locale),
      languages,
    },
  };
}

export default async function EmailSourceThreadsIndex({
  params: { locale, source },
}: LocaleParams<{ source: EmailSource }>) {
  const { t } = await i18nTranslation(locale);
  const threads = await getEmailThreadsBySource(source);

  const otherSource = otherEmailSource(source);

  const allLink: SourceLink = {
    name: t("all"),
    href: urls(locale).satoshi.emails.threadsIndex,
  };
  const additionalLinks: SourceLink[] =
    source === "cryptography"
      ? [
          { name: formatEmailSource("cryptography"), active: true },
          {
            name: formatEmailSource("bitcoin-list"),
            href: urls(locale).satoshi.emails.sourceThreadsIndex(otherSource),
          },
        ]
      : [
          {
            name: formatEmailSource("cryptography"),
            href: urls(locale).satoshi.emails.sourceThreadsIndex(otherSource),
          },
          { name: formatEmailSource("bitcoin-list"), active: true },
        ];
  const sourceLinks = [allLink, ...additionalLinks];

  return (
    <IndexPageLayout
      t={t}
      title={t("emails")}
      locale={locale}
      generateHref={generateHref(source)}
      breadcrumbs={[
        { label: t("complete_satoshi"), href: urls(locale).satoshi.index },
        { label: t("emails"), href: urls(locale).satoshi.emails.index },
      ]}
      sourceLinks={sourceLinks}
      toggleLinks={{
        active: "threads",
        href: urls(locale).satoshi.emails.sourceIndex(source),
      }}
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
