import Link from "next/link";

import "@/app/globals.css";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";

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
      <div>
        <h2>Not Found</h2>
        <p>Could not find requested resource</p>
        <Link href={generateHref(locale)}>Return Home</Link>
      </div>
    </PageLayout>
  );
}
