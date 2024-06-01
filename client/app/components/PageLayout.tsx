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
      {env.FATHOM_ID ? <Fathom siteId={env.FATHOM_ID} /> : null}
      <Navbar
        locale={locale}
        title={t("sni_full")}
        mobileTitle={t("sni")}
        homeHref={urls(locale).home}
        navLinks={[
          {
            href: urls(locale).satoshi.index,
            text: t("complete_satoshi"),
          },
          { href: urls(locale).library.index, text: t("library") },
          { href: urls(locale).mempool.index, text: t("mempool") },
          { href: urls(locale).substack, text: t("newsletter") },
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
