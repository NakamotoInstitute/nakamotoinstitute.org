import { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { getEmail } from "@/lib/api/emails";
import { EmailSource } from "@/lib/api/schemas/emails";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";
import { formatEmailSource } from "@/utils/strings";

import { EmailNavigation } from "@satoshi/components/ContentNavigation";

// export const dynamicParams = false;

const generateHref = (source: EmailSource, satoshiId: string) => (l: Locale) =>
  urls(l).satoshi.emails.sourceEmail(source, satoshiId);

export async function generateMetadata({
  params: { source, satoshiId, locale },
}: LocaleParams<{
  source: EmailSource;
  satoshiId: string;
}>): Promise<Metadata> {
  const emailData = await getEmail(source, satoshiId);
  const languages = generateHrefLangs(
    [...locales],
    generateHref(source, satoshiId),
  );

  return {
    title: emailData.email.subject,
    alternates: {
      canonical: generateHref(source, satoshiId)(locale),
      languages,
    },
  };
}

export default async function EmailDetail({
  params: { locale, source, satoshiId },
}: LocaleParams<{ source: EmailSource; satoshiId: string }>) {
  const { t } = await i18nTranslation(locale);
  const emailData = await getEmail(source, satoshiId);

  if (!emailData) {
    return notFound();
  }

  const { next, previous, email } = emailData;

  return (
    <PageLayout
      t={t}
      locale={locale}
      generateHref={generateHref(source, satoshiId)}
    >
      <EmailNavigation
        t={t}
        className="mb-2"
        locale={locale}
        source={email.source}
        previous={previous}
        next={next}
      />
      <div>
        <h2 className="text-2xl">{formatEmailSource(email.source)}</h2>
        <h1 className="text-4xl">{email.subject}</h1>
        <p className="text-xl">
          <time dateTime={email.date.toISOString()}>
            {formatDate(locale, email.date, {
              dateStyle: "long",
              timeStyle: "long",
              hourCycle: "h24",
            })}
          </time>
        </p>
        <div className="flex gap-2">
          <Link href={email.url}>{t("original_email")}</Link> •{" "}
          <Link
            href={{
              pathname: urls(locale).satoshi.emails.sourceThreadsDetail(
                email.source,
                email.threadId.toString(),
              ),
              hash: email.sourceId.toString(),
            }}
          >
            {t("view_in_thread")}
          </Link>
        </div>
      </div>
      <hr className="my-4" />
      <div
        className="font-mono"
        dangerouslySetInnerHTML={{
          __html: email.text.replaceAll("\n", "<br />"),
        }}
      />
      <EmailNavigation
        t={t}
        className="mt-4"
        locale={locale}
        previous={previous}
        next={next}
        source={email.source}
        reverse
      />
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
