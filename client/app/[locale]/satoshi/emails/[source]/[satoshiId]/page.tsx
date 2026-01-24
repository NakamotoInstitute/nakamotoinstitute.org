import { Metadata } from "next";
import { notFound } from "next/navigation";

import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { EmailSource, api } from "@/lib/api";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatEmailSource } from "@/utils/strings";

import {
  ContentBox,
  ContentBoxBody,
  ContentBoxDisclaimer,
  ContentBoxFooter,
  ContentBoxHeader,
} from "@satoshi/components/ContentBox";
import { EmailNavigation } from "@satoshi/components/ContentNavigation";

// export const dynamicParams = false;

const generateHref = (source: EmailSource, satoshiId: string) => (l: Locale) =>
  urls(l).satoshi.emails.sourceEmail(source, satoshiId);

export async function generateMetadata(
  props: LocaleParams<{
    source: EmailSource;
    satoshiId: string;
  }>,
): Promise<Metadata> {
  const params = await props.params;

  const { source, satoshiId, locale } = params;

  const { data: emailData } = await api.satoshi.getEmailBySource({
    path: { source, satoshi_id: parseInt(satoshiId) },
  });
  const languages = generateHrefLangs(locales, generateHref(source, satoshiId));

  return {
    title: emailData.email.subject,
    alternates: {
      canonical: generateHref(source, satoshiId)(locale),
      languages,
    },
  };
}

export default async function EmailDetail(
  props: LocaleParams<{ source: EmailSource; satoshiId: string }>,
) {
  const params = await props.params;

  const { locale, source, satoshiId } = params;

  const { t } = await i18nTranslation(locale);
  const { data: emailData } = await api.satoshi.getEmailBySource({
    path: { source, satoshi_id: parseInt(satoshiId) },
  });

  if (!emailData) {
    return notFound();
  }

  const { next, previous, email } = emailData;

  return (
    <PageLayout
      t={t}
      locale={locale}
      generateHref={generateHref(source, satoshiId)}
      breadcrumbs={[
        { label: t("complete_satoshi"), href: urls(locale).satoshi.index },
        { label: t("emails"), href: urls(locale).satoshi.emails.index },
        {
          label: formatEmailSource(source, true),
          href: urls(locale).satoshi.emails.sourceIndex(source),
        },
      ]}
    >
      <PageHeader superTitle={formatEmailSource(source)} title={email.subject}>
        <EmailNavigation
          t={t}
          locale={locale}
          id={email.satoshiId}
          source={email.source}
          previous={previous}
          next={next}
        />
      </PageHeader>

      <ContentBox>
        <ContentBoxHeader
          t={t}
          locale={locale}
          from={email.sentFrom}
          subject={email.subject}
          date={email.date}
        />
        <ContentBoxBody mono>
          <div
            dangerouslySetInnerHTML={{
              __html: email.text.replaceAll("\n", "<br />"),
            }}
          />
        </ContentBoxBody>
        {email.disclaimer && (
          <ContentBoxDisclaimer t={t} disclaimer={email.disclaimer} />
        )}
        <ContentBoxFooter
          t={t}
          hrefs={{
            original: email.url,
            thread: {
              pathname: urls(locale).satoshi.emails.sourceThreadsDetail(
                email.source,
                email.threadId.toString(),
              ),
              hash: email.sourceId.toString(),
            },
          }}
        />
      </ContentBox>
    </PageLayout>
  );
}

// export async function generateStaticParams() {
//   const emails = await getSatoshiEmails();
//   return getLocaleParams((locale) =>
//     emails.map((e) => ({
//       locale,
//       source: e.source,
//       satoshiId: e.satoshiId.toString(),
//     })),
//   );
// }
