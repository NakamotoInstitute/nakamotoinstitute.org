import { TFunction } from "i18next";
import { Metadata } from "next";
import { notFound } from "next/navigation";

import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { getEmailThread } from "@/lib/api/emails";
import { EmailSource, EmailWithParent } from "@/lib/api/schemas/emails";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatEmailSource } from "@/utils/strings";

import {
  ContentBox,
  ContentBoxBody,
  ContentBoxFooter,
  ContentBoxHeader,
} from "@satoshi/components/ContentBox";
import { EmailThreadNavigation } from "@satoshi/components/ContentNavigation";
import { ThreadPageHeader } from "@satoshi/components/ThreadPageHeader";

// export const dynamicParams = false;

const generateHref = (source: EmailSource, threadId: string) => (l: Locale) =>
  urls(l).satoshi.emails.sourceThreadsDetail(source, threadId);

export async function generateMetadata({
  params: { locale, source, threadId },
}: LocaleParams<{ source: EmailSource; threadId: string }>): Promise<Metadata> {
  const threadData = await getEmailThread(source, threadId);
  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs(
    [...locales],
    generateHref(source, threadId),
  );

  return {
    title: t("title_thread", { title: threadData.thread.title }),
    alternates: {
      canonical: generateHref(source, threadId)(locale),
      languages,
    },
  };
}

type ThreadEmailProps = {
  t: TFunction<string, string>;
  locale: Locale;
  email: EmailWithParent;
  odd: boolean;
};

async function ThreadEmail({ t, locale, email, odd }: ThreadEmailProps) {
  return (
    <ContentBox
      id={email.sourceId}
      as="article"
      className="mb-3 last:mb-0"
      alternate={odd}
    >
      <ContentBoxHeader
        t={t}
        locale={locale}
        source={formatEmailSource(email.source)}
        sourceId={email.sourceId}
        from={email.sentFrom}
        subject={email.subject}
        date={email.date}
        satoshi={!!email.satoshiId}
      />
      <ContentBoxBody mono>
        <div
          dangerouslySetInnerHTML={{
            __html: email.text.replaceAll("\n", "<br />"),
          }}
        />
      </ContentBoxBody>
      <ContentBoxFooter
        t={t}
        hrefs={{
          original: email.url,
          permalink: email.satoshiId
            ? urls(locale).satoshi.emails.sourceEmail(
                email.source,
                email.satoshiId.toString(),
              )
            : undefined,
        }}
      />
    </ContentBox>
  );
}

export default async function EmailSourceThreadDetail({
  params: { locale, source, threadId },
  searchParams: { view },
}: LocaleParams<
  { source: EmailSource; threadId: string },
  { searchParams: { [key: string]: string | string[] | undefined } }
>) {
  const satoshiOnly = view === "satoshi";

  const threadData = await getEmailThread(source, threadId, satoshiOnly);
  if (!threadData) {
    return notFound();
  }

  const { thread, emails, next, previous } = threadData;

  const { t } = await i18nTranslation(locale);

  return (
    <PageLayout
      t={t}
      locale={locale}
      generateHref={generateHref(source, threadId)}
      breadcrumbs={[
        { label: t("complete_satoshi"), href: urls(locale).satoshi.index },
        { label: t("emails"), href: urls(locale).satoshi.emails.threadsIndex },
        {
          label: formatEmailSource(source, true),
          href: urls(locale).satoshi.emails.sourceThreadsIndex(source),
        },
      ]}
    >
      <ThreadPageHeader
        t={t}
        sourceTitle={formatEmailSource(thread.source)}
        title={thread.title}
        allLink={{
          href: generateHref(source, threadId)(locale),
          text: t("view_all_emails"),
        }}
        externalLink={thread.url}
        satoshiOnly={satoshiOnly}
      >
        <EmailThreadNavigation
          t={t}
          locale={locale}
          id={thread.id}
          previous={previous}
          next={next}
          source={thread.source}
        />
      </ThreadPageHeader>
      {emails.map((e, index) => (
        <ThreadEmail
          key={e.sourceId}
          t={t}
          locale={locale}
          email={e}
          odd={index % 2 !== 0}
        />
      ))}
    </PageLayout>
  );
}

// export async function generateStaticParams() {
//   const threads = await getEmailThreads();
//   return getLocaleParams((locale) =>
//     threads.map((t) => ({
//       locale,
//       source: t.source,
//       threadId: t.id.toString(),
//     })),
//   );
// }
