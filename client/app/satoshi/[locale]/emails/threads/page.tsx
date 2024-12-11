import { Metadata } from "next";

import { locales } from "@/i18n";
import { getEmailThreads } from "@/lib/api/emails";
import {
  EMAIL_SOURCES,
  EmailSource,
  EmailThread,
} from "@/lib/api/schemas/emails";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatEmailSource } from "@/utils/strings";

import { ContentListing } from "@satoshi/components/ContentListing";
import { IndexPageLayout } from "@satoshi/components/IndexPageLayout";

export const dynamicParams = false;

const generateHref = (l: Locale) => urls(l).satoshi.emails.threadsIndex;

export async function generateMetadata(props: LocaleParams): Promise<Metadata> {
  const params = await props.params;

  const { locale } = params;

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

export default async function EmailThreadsIndex(props: LocaleParams) {
  const params = await props.params;

  const { locale } = params;

  const { t } = await i18nTranslation(locale);
  const threads = await getEmailThreads();
  const sortedThreads = threads.reduce(
    (acc, thread) => {
      acc[thread.source].push(thread);
      return acc;
    },
    Object.fromEntries(
      EMAIL_SOURCES.map((source) => [source, [] as EmailThread[]]),
    ) as {
      [K in EmailSource]: EmailThread[];
    },
  );

  const sourceLinks = [
    {
      name: t("all"),
      href: urls(locale).satoshi.emails.threadsIndex,
      active: true,
    },
    ...EMAIL_SOURCES.map((s) => ({
      name: formatEmailSource(s),
      href: urls(locale).satoshi.emails.sourceThreadsIndex(s),
    })),
  ];

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
      sourceLinks={sourceLinks}
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
