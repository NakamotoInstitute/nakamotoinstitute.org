import Link from "next/link";

import "@/app/globals.css";

import { PageLayout } from "./PageLayout";

type NotFoundLayoutProps = {
  locale: Locale;
  generateHref: (locale: Locale) => string;
};

export default function NotFoundLayout({
  locale,
  generateHref,
}: NotFoundLayoutProps) {
  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <div>
        <h2>Not Found</h2>
        <p>Could not find requested resource</p>
        <Link href={generateHref(locale)}>Return Home</Link>
      </div>
    </PageLayout>
  );
}
