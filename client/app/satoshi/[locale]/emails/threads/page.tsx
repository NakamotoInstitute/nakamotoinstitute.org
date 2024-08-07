import { Metadata } from "next";

import { locales } from "@/i18n";
import { getEmailThreads } from "@/lib/api/emails";
import { EmailSource, EmailThread } from "@/lib/api/schemas/emails";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatEmailSource } from "@/utils/strings";

import { IndexPageLayout } from "@satoshi/components/IndexPageLayout";

import { ContentListing } from "../../components/ContentListing";

export const dynamicParams = false;

const generateHref = (l: Locale) => urls(l).satoshi.emails.threadsIndex;

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs([...locales], generateHref);

  return {
    title: t("email_threads"),
    alternates: {
      canonical: generateHref(locale),
      languages,
    },
  };
}

export default async function EmailThreadsIndex({
  params: { locale },
}: LocaleParams) {
  const { t } = await i18nTranslation(locale);
  const threads = await getEmailThreads();
  const sortedThreads = threads.reduce(
    (acc, thread) => {
      acc[thread.source].push(thread);
      return acc;
    },
    {
      cryptography: [],
      "bitcoin-list": [],
      p2presearch: [],
    } as { [K in EmailSource]: EmailThread[] },
  );

  return (
    <IndexPageLayout
      t={t}
      type="emails"
      locale={locale}
      generateHref={generateHref}
      breadcrumbs={[
        { label: t("complete_satoshi"), href: urls(locale).satoshi.index },
        { label: t("emails"), href: urls(locale).satoshi.emails.threadsIndex },
      ]}
      sourceLinks={[
        {
          name: t("all"),
          active: true,
        },
        {
          name: formatEmailSource("cryptography"),
          href: urls(locale).satoshi.emails.sourceThreadsIndex("cryptography"),
        },
        {
          name: formatEmailSource("bitcoin-list"),
          href: urls(locale).satoshi.emails.sourceThreadsIndex("bitcoin-list"),
        },
        {
          name: formatEmailSource("p2presearch"),
          href: urls(locale).satoshi.emails.sourceThreadsIndex("p2presearch"),
        },
      ]}
      toggleLinks={{
        active: "threads",
        href: urls(locale).satoshi.emails.index,
      }}
    >
      <section>
        {Object.entries(sortedThreads).map(([source, sourceThreads]) => {
          const typedSource = source as EmailSource;
          return (
            <div key={typedSource} className="pt-5">
              <h2 className="text-2xl font-bold">
                {formatEmailSource(typedSource)}
              </h2>
              {sourceThreads.map((thread) => (
                <ContentListing
                  key={thread.id}
                  locale={locale}
                  label={thread.title}
                  href={urls(locale).satoshi.emails.sourceThreadsDetail(
                    thread.source,
                    thread.id.toString(),
                  )}
                  date={thread.date}
                />
              ))}
            </div>
          );
        })}
      </section>
    </IndexPageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
