import { PageLayout } from "@/app/components/PageLayout";
import { PageHeader } from "@/app/components/PageHeader";
import { getEmailThreads } from "@/lib/api/emails";
import { EmailSource, EmailThread } from "@/lib/api/schemas/emails";
import { getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";
import { formatEmailSource } from "@/utils/strings";
import Link from "next/link";

export default async function EmailThreadsIndex({
  params: { locale },
}: LocaleParams) {
  const threads = await getEmailThreads();
  const generateHref = (l: Locale) => urls(l).satoshi.emails.threadsIndex;
  const sortedThreads = threads.reduce(
    (acc, thread) => {
      acc[thread.source].push(thread);
      return acc;
    },
    {
      cryptography: [],
      "bitcoin-list": [],
    } as { [K in EmailSource]: EmailThread[] },
  );

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title="Email Threads" />
      <section>
        {Object.entries(sortedThreads).map(([source, sourceThreads]) => {
          const typedSource = source as EmailSource;
          return (
            <div key={typedSource} className="pb-4 last:pb-0">
              <h2 className="pb-2 text-3xl">
                {formatEmailSource(typedSource)}
              </h2>
              <ul>
                {sourceThreads.map((thread) => (
                  <li key={thread.title}>
                    <Link
                      href={urls(locale).satoshi.emails.sourceThreadsDetail(
                        thread.source,
                        thread.id.toString(),
                      )}
                    >
                      {thread.title}
                    </Link>{" "}
                    - <em>{formatDate(locale, thread.date)}</em>
                  </li>
                ))}
              </ul>
            </div>
          );
        })}
      </section>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
