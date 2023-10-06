import Link from "next/link";
import { notFound } from "next/navigation";
import { PageLayout } from "@/app/components";
import { EmailSource, getEmail, getSatoshiEmails } from "@/lib/api";
import { getLocaleParams, i18nTranslation } from "@/lib/i18n";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";
import { formatEmailSource } from "@/utils/strings";
import { EmailNavigation } from "@satoshi/components/ContentNavigation";

export const dynamicParams = false;

export default async function EmailDetail({
  params: { locale, source, satoshiId },
}: LocaleParams<{ source: EmailSource; satoshiId: string }>) {
  const { t } = await i18nTranslation(locale);
  const emailData = await getEmail(source, satoshiId);

  if (!emailData) {
    return notFound();
  }

  const { next, previous, email } = emailData;
  const generateHref = (l: Locale) =>
    urls(l).satoshi.emails.sourceEmail(source, satoshiId);

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <EmailNavigation locale={locale} previous={previous} next={next} />
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
          <Link href={email.url}>{t("Original email")}</Link> •{" "}
          <Link
            href={{
              pathname: urls(locale).satoshi.emails.sourceThreadsDetail(
                email.source,
                email.threadId.toString(),
              ),
              hash: email.sourceId.toString(),
            }}
          >
            {t("View in thread")}
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
      <EmailNavigation locale={locale} previous={previous} next={next} />
    </PageLayout>
  );
}

export async function generateStaticParams() {
  const emails = await getSatoshiEmails();
  return getLocaleParams((locale) =>
    emails.map((e) => ({
      locale,
      source: e.source,
      satoshiId: e.satoshiId.toString(),
    })),
  );
}
