import clsx from "clsx";
import { TFunction } from "i18next";
import { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { getEmailThread } from "@/lib/api/emails";
import { EmailSource, EmailWithParent } from "@/lib/api/schemas/emails";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";
import { formatEmailSource } from "@/utils/strings";

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
  satoshiOnly: boolean;
};

async function ThreadEmail({
  t,
  locale,
  email,
  odd,
  satoshiOnly,
}: ThreadEmailProps) {
  return (
    <article
      id={email.sourceId}
      className={clsx(
        "mb-3 border-2 font-mono text-[13px] last:mb-0",
        odd ? "bg-neutral-100" : "bg-white",
      )}
    >
      <header className={clsx(email.satoshiId && "bg-amber-200")}>
        <div className="flex justify-between border-b p-2">
          <span className="font-bold">From: {email.sentFrom}</span>
          <Link href={{ hash: email.sourceId }}>#{email.sourceId}</Link>
        </div>
        <div className="border-b p-2">
          <h2 className="text-lg font-bold">{email.subject}</h2>
          <time dateTime={email.date.toISOString()}>
            {formatDate(locale, email.date, {
              dateStyle: "long",
              timeStyle: "long",
            })}
          </time>
        </div>
        {!satoshiOnly && (email.parent || email.replies.length > 0) ? (
          <div className="border-b p-2">
            {email.parent ? (
              <div className="flex gap-2">
                <span>{t("replying_to")}</span>
                <Link
                  href={{ hash: email.parent.sourceId }}
                >{`>>${email.parent.sourceId}`}</Link>
              </div>
            ) : null}
            {email.replies.length > 0 ? (
              <div className="flex gap-2">
                <span>{t("replies")}</span>
                {email.replies.map((reply) => (
                  <Link key={reply} href={{ hash: reply }}>{`>>${reply}`}</Link>
                ))}
              </div>
            ) : null}
          </div>
        ) : null}
      </header>
      <section>
        <div
          className="p-2"
          dangerouslySetInnerHTML={{
            __html: email.text.replaceAll("\n", "<br />"),
          }}
        />
      </section>
      <footer className="flex justify-between border-t p-2">
        <Link href={email.url}>{t("external_link")}</Link>
        {email.satoshiId ? (
          <Link
            href={urls(locale).satoshi.emails.sourceEmail(
              email.source,
              email.satoshiId.toString(),
            )}
          >
            {t("permalink")}
          </Link>
        ) : null}
      </footer>
    </article>
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
          className="mb-4"
          locale={locale}
          next={next}
          previous={previous}
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
          satoshiOnly={satoshiOnly}
        />
      ))}
      <EmailThreadNavigation
        t={t}
        className="mt-4"
        locale={locale}
        next={next}
        previous={previous}
        source={thread.source}
        reverse
      />
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
