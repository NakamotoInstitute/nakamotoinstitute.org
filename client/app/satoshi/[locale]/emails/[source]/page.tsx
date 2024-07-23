import { Metadata } from "next";

import { locales } from "@/i18n";
import { getSatoshiEmailsBySource } from "@/lib/api/emails";
import { EmailSource } from "@/lib/api/schemas/emails";
import { zEmailSource } from "@/lib/api/schemas/emails";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatEmailSource, otherEmailSource } from "@/utils/strings";

import { ContentListing } from "@satoshi/components/ContentListing";
import { SourceLink } from "@satoshi/components/IndexHeader";
import { IndexPageLayout } from "@satoshi/components/IndexPageLayout";

export const dynamicParams = false;

const generateHref = (source: EmailSource) => (l: Locale) =>
  urls(l).satoshi.emails.sourceIndex(source);

export async function generateMetadata({
  params: { locale, source },
}: LocaleParams<{ source: EmailSource }>): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs([...locales], generateHref(source));

  return {
    title: t("source_emails", { source: formatEmailSource(source) }),
    alternates: {
      canonical: generateHref(source)(locale),
      languages,
    },
  };
}

export default async function EmailsSourceIndex({
  params: { locale, source },
}: LocaleParams<{ source: EmailSource }>) {
  const { t } = await i18nTranslation(locale);
  const emails = await getSatoshiEmailsBySource(source);

  const otherSource = otherEmailSource(source);

  const allLink: SourceLink = {
    name: t("all"),
    href: urls(locale).satoshi.emails.index,
  };
  const additionalLinks: SourceLink[] =
    source === "cryptography"
      ? [
          { name: formatEmailSource("cryptography"), active: true },
          {
            name: formatEmailSource("bitcoin-list"),
            href: urls(locale).satoshi.emails.sourceIndex(otherSource),
          },
        ]
      : [
          {
            name: formatEmailSource("cryptography"),
            href: urls(locale).satoshi.emails.sourceIndex(otherSource),
          },
          { name: formatEmailSource("bitcoin-list"), active: true },
        ];
  const sourceLinks = [allLink, ...additionalLinks];

  return (
    <IndexPageLayout
      t={t}
      type="emails"
      locale={locale}
      generateHref={generateHref(source)}
      breadcrumbs={[
        { label: t("complete_satoshi"), href: urls(locale).satoshi.index },
        { label: t("emails"), href: urls(locale).satoshi.emails.index },
        {
          label: formatEmailSource(source, true),
          href: urls(locale).satoshi.emails.sourceIndex(source),
        },
      ]}
      sourceLinks={sourceLinks}
      toggleLinks={{
        active: "individual",
        href: urls(locale).satoshi.emails.sourceThreadsIndex(source),
      }}
    >
      <section>
        {emails.map((e) => (
          <ContentListing
            key={e.satoshiId}
            locale={locale}
            label={e.subject}
            href={urls(locale).satoshi.emails.sourceEmail(
              e.source,
              e.satoshiId.toString(),
            )}
            date={e.date}
          />
        ))}
      </section>
    </IndexPageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams((locale) =>
    zEmailSource.options.map((source) => ({ locale, source })),
  );
}
