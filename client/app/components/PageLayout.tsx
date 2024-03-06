import clsx from "clsx";

import { env } from "@/env";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateLocaleToggleLinks, urls } from "@/lib/urls";

import Fathom from "./Fathom";
import { Footer } from "./Footer";
import { Navbar } from "./Navbar";

export type PageLayoutProps = {
  className?: string;
  generateHref?: (locale: Locale) => string;
  locale: Locale;
  children: React.ReactNode;
};

export async function PageLayout({
  className,
  locale,
  generateHref,
  children,
}: PageLayoutProps) {
  const { t } = await i18nTranslation(locale);
  const toggleProps = generateHref
    ? generateLocaleToggleLinks(locale, generateHref)
    : {};

  return (
    <body className="flex min-h-screen flex-col">
      <Fathom siteId={env.FATHOM_ID!} />
      <Navbar
        locale={locale}
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
      <Footer locale={locale} />
    </body>
  );
}
