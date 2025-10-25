import { Metadata } from "next";

import { locales } from "@/i18n";
import { getSatoshiEmails } from "@/lib/api/emails";
import { EMAIL_SOURCES } from "@/lib/api/schemas/emails";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatEmailSource } from "@/utils/strings";

import { ContentListing } from "@satoshi/components/ContentListing";
import { SourceLink } from "@satoshi/components/IndexHeader";
import { IndexPageLayout } from "@satoshi/components/IndexPageLayout";

export const dynamicParams = false;

const generateHref = (l: Locale) => urls(l).satoshi.emails.index;

export async function generateMetadata(props: LocaleParams): Promise<Metadata> {
  const params = await props.params;

  const { locale } = params;

  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs(locales, generateHref);

  return {
    title: t("emails"),
    alternates: {
      canonical: generateHref(locale),
      languages,
    },
  };
}

export default async function EmailsIndex(props: LocaleParams) {
  const params = await props.params;

  const { locale } = params;

  const { t } = await i18nTranslation(locale);
  const emails = await getSatoshiEmails();

  const sourceLinks: SourceLink[] = [
    { name: t("all"), active: true },
    ...EMAIL_SOURCES.map((s) => ({
      name: formatEmailSource(s),
      href: urls(locale).satoshi.emails.sourceIndex(s),
    })),
  ];

  return (
    <IndexPageLayout
      t={t}
      locale={locale}
      generateHref={generateHref}
      type="emails"
      breadcrumbs={[
        { label: t("complete_satoshi"), href: urls(locale).satoshi.index },
        { label: t("emails"), href: urls(locale).satoshi.emails.index },
      ]}
      sourceLinks={sourceLinks}
      toggleLinks={{
        active: "individual",
        href: urls(locale).satoshi.emails.threadsIndex,
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
  return getLocaleParams();
}
