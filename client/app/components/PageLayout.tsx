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
        <div className="mb-4 rounded bg-amber-100 px-5 py-3 text-yellow-800 sm:flex">
          <div className="mr-auto">{t("timeless_beauty")}</div>
          <div className="flex items-center">
            <a href="https://news.nakamotoinstitute.org/p/help-give-sni-timeless-beauty">
              {t("more_info")}
            </a>
            <div className="w-px bg-gray-500 mx-2 h-4" />
            <a href="https://pay.zaprite.com/pl_saYgrVYmCi">{t("donate")}</a>
          </div>
        </div>
        {children}
      </main>
      <Footer t={t} locale={locale} />
    </body>
  );
}
