import clsx from "clsx";
import { TFunction } from "i18next";

import { env } from "@/env";
import { generateLocaleToggleLinks, urls } from "@/lib/urls";

import Fathom from "./Fathom";
import { Footer } from "./Footer";
import { Navbar } from "./Navbar";

export type PageLayoutProps = {
  t: TFunction<string, string>;
  className?: string;
  generateHref?: (locale: Locale) => string;
  locale: Locale;
  children: React.ReactNode;
};

export async function PageLayout({
  t,
  className,
  locale,
  generateHref,
  children,
}: PageLayoutProps) {
  const toggleProps = generateHref
    ? generateLocaleToggleLinks(locale, generateHref)
    : {};

  return (
    <body className="flex min-h-screen flex-col">
      <Fathom siteId={env.FATHOM_ID!} />
      <Navbar
        locale={locale}
        title={t("Satoshi Nakamoto Institute")}
        mobileTitle={t("SNI")}
        homeHref={urls(locale).home}
        navLinks={[
          {
            href: urls(locale).satoshi.index,
            text: t("The Complete Satoshi"),
          },
          { href: urls(locale).library.index, text: t("Library") },
          { href: urls(locale).mempool.index, text: t("Mempool") },
          { href: urls(locale).substack, text: t("Newsletter") },
        ]}
        {...toggleProps}
      />
      <main className={clsx("twbs-container mb-4 flex-grow pb-4", className)}>
        {children}
      </main>
      <Footer t={t} locale={locale} />
    </body>
  );
}
