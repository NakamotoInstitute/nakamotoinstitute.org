import { Metadata } from "next";

import { locales } from "@/i18n";
import { api, EMAIL_SOURCES, EmailBase, EmailSource } from "@/lib/api";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatEmailSource } from "@/utils/strings";

import { ContentListing } from "@satoshi/components/ContentListing";
import { IndexPageLayout } from "@satoshi/components/IndexPageLayout";

export const dynamicParams = false;

const generateHref = (source: EmailSource) => (l: Locale) =>
  urls(l).satoshi.emails.sourceIndex(source);

export async function generateMetadata(
  props: LocaleParams<{ source: EmailSource }>,
): Promise<Metadata> {
  const params = await props.params;

  const { locale, source } = params;

  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs(locales, generateHref(source));

  return {
    title: t("source_emails", { source: formatEmailSource(source) }),
    alternates: {
      canonical: generateHref(source)(locale),
      languages,
    },
  };
}

export default async function EmailsSourceIndex(
  props: LocaleParams<{ source: EmailSource }>,
) {
  const params = await props.params;

  const { locale, source } = params;

  const { t } = await i18nTranslation(locale);
  const { data: emails } = await api.satoshi.getEmailsBySource({ path: { source } });

  const sourceLinks = [
    { name: t("all"), href: urls(locale).satoshi.emails.index },
    ...EMAIL_SOURCES.map((s) => ({
      name: formatEmailSource(s),
      href: urls(locale).satoshi.emails.sourceIndex(s),
      active: s === source,
    })),
  ];

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
        {emails.map((e: EmailBase) => (
          <ContentListing
            key={e.satoshiId}
            locale={locale}
            label={e.subject}
            href={urls(locale).satoshi.emails.sourceEmail(
              e.source as EmailSource,
              e.satoshiId!.toString(),
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
    EMAIL_SOURCES.map((source) => ({ locale, source })),
  );
}
