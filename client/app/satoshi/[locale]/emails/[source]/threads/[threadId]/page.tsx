import Link from "next/link";
import { notFound } from "next/navigation";
import clsx from "clsx";
import { PageLayout } from "@/app/components/PageLayout";
import { getEmailThread, getEmailThreads } from "@/lib/api/emails";
import { EmailSource, ThreadEmail } from "@/lib/api/schemas/emails";
import { getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";
import { formatEmailSource } from "@/utils/strings";

export const dynamicParams = false;

function ThreadEmail({
  locale,
  email,
  odd,
  satoshiOnly,
}: {
  locale: Locale;
  email: ThreadEmail;
  odd: boolean;
  satoshiOnly: boolean;
}) {
  return (
    <article
      id={email.sourceId}
      className={clsx(
        "mb-3 border-2 border-night font-mono text-[13px] last:mb-0",
        odd ? "bg-gray" : "bg-white",
      )}
    >
      <header className={clsx(email.satoshiId && "bg-flax")}>
        <div className="flex justify-between border-b-1 border-b-night p-2">
          <span className="font-bold">From: {email.sentFrom}</span>
          <Link href={{ hash: email.sourceId }}>#{email.sourceId}</Link>
        </div>
        <div className="border-b-1 border-b-night p-2">
          <h2 className="text-lg font-bold">{email.subject}</h2>
          <time dateTime={email.date.toISOString()}>
            {formatDate(locale, email.date, {
              dateStyle: "long",
              timeStyle: "long",
            })}
          </time>
        </div>
        {!satoshiOnly && email.replies.length > 0 ? (
          <div className="border-b-1 border-night p-2">
            {email.parentId ? (
              <p>Replying to: {email.parent?.sourceId}</p>
            ) : null}
            <p>Replies: {email.replies.join(", ")}</p>
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
      <footer className="flex justify-between border-t-1 border-t-night p-2">
        <Link href={email.url}>External link</Link>
        {email.satoshiId ? (
          <Link
            href={urls(locale).satoshi.emails.sourceEmail(
              email.source,
              email.satoshiId.toString(),
            )}
          >
            Permalink
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

  const generateHref = (l: Locale) =>
    urls(l).satoshi.emails.sourceThreadsDetail(source, threadId);

  const { thread, emails } = threadData;

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <div className="text-center">
        <p>{formatEmailSource(thread.source)}</p>
        <h1 className="text-2xl">{thread.title}</h1>
        {satoshiOnly ? (
          <Link href={generateHref(locale)}>View all emails</Link>
        ) : (
          <Link href={{ query: { view: "satoshi" } }}>View Satoshi only</Link>
        )}
      </div>

      {emails.map((e, index) => (
        <ThreadEmail
          key={e.sourceId}
          locale={locale}
          email={e}
          odd={index % 2 !== 0}
          satoshiOnly={satoshiOnly}
        />
      ))}
    </PageLayout>
  );
}

export async function generateStaticParams() {
  const threads = await getEmailThreads();
  return getLocaleParams((locale) =>
    threads.map((t) => ({
      locale,
      source: t.source,
      threadId: t.id.toString(),
    })),
  );
}
