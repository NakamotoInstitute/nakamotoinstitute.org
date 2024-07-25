import Link from "next/link";

import "@/app/globals.css";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";

import { ButtonLink } from "./Button";
import { PageHeader } from "./PageHeader";
import { PageLayout } from "./PageLayout";

type NotFoundLayoutProps = {
  locale: Locale;
  generateHref: (locale: Locale) => string;
};

export default async function NotFoundLayout({
  locale,
  generateHref,
}: NotFoundLayoutProps) {
  const { t } = await i18nTranslation(locale);
  return (
    <PageLayout t={t} locale={locale} generateHref={generateHref}>
      <PageHeader title="Not Found"></PageHeader>
      <section>
        <p>Could not find requested resource</p>
        <ButtonLink className="mt-4" href={generateHref(locale)}>
          Return home
        </ButtonLink>
      </section>
    </PageLayout>
  );
}
