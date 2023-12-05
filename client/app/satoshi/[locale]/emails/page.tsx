import Link from "next/link";
import { PageLayout } from "@/app/components/PageLayout";
import { getSatoshiEmails } from "@/lib/api/emails";
import { getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";
import { PageHeader } from "@/app/components/PageHeader";

export default async function EmailsIndex({
  params: { locale },
}: LocaleParams) {
  const emails = await getSatoshiEmails();
  const generateHref = (l: Locale) => urls(l).satoshi.emails.index;

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title="Emails" />
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
              {formatDate(locale, e.date, {
                dateStyle: "medium",
                timeStyle: "long",
              })}
            </em>
          </li>
        ))}
      </ul>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
