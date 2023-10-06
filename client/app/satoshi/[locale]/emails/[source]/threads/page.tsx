import { PageLayout } from "@/app/components";
import { PageHeader } from "@/app/components/PageHeader";
import { EmailSource, getEmailThreadsBySource, zEmailSource } from "@/lib/api";
import { getLocaleParams } from "@/lib/i18n";
import { urls } from "@/lib/urls";
import { formatEmailSource } from "@/utils/strings";
import Link from "next/link";

export const dynamicParams = false;

export default async function EmailSourceThreadsIndex({
  params: { locale, source },
}: LocaleParams<{ source: EmailSource }>) {
  const threads = await getEmailThreadsBySource(source);
  const generateHref = (l: Locale) =>
    urls(l).satoshi.emails.sourceThreadsIndex(source);

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title={`${formatEmailSource(source)} Threads`} />
      <ul>
        {threads.map((t) => (
          <li key={t.id}>
            <Link
              href={urls(locale).satoshi.emails.sourceThreadsDetail(
                t.source,
                t.id.toString(),
              )}
            >
              {t.title}
            </Link>
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
