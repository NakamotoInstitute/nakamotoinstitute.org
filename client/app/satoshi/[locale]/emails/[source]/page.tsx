import Link from "next/link";
import { PageLayout } from "@/app/components";
import { EmailSource, getSatoshiEmailsBySource } from "@/lib/api";
import { formatEmailSource } from "@/utils/strings";
import { getLocaleParams } from "@/lib/i18n";
import { urls } from "@/lib/urls";
import { PageHeader } from "@/app/components/PageHeader";
import { zEmailSource } from "@/lib/api";

export const dynamicParams = false;

export default async function EmailsSourceIndex({
  params: { locale, source },
}: LocaleParams<{ source: EmailSource }>) {
  const emails = await getSatoshiEmailsBySource(source);
  const generateHref = (l: Locale) =>
    urls(l).satoshi.emails.sourceIndex(source);

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title={`${formatEmailSource(source)} Emails`} />
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
            <em>{e.date.toString()}</em>
          </li>
        ))}
      </ul>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams((locale) =>
    zEmailSource.options.map((source) => ({ locale, source })),
  );
}
