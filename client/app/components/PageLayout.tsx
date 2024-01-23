import clsx from "clsx";
import { Navbar } from "./Navbar";
import { Footer } from "./Footer";
import { generateLocaleToggleLinks, urls } from "@/lib/urls";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";

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
      <Navbar
        locale={locale}
        homeHref={urls(locale).home}
        navLinks={[
          {
            href: urls(locale).satoshi.index,
            label: t("The Complete Satoshi"),
          },
          { href: urls(locale).library.index, label: t("Library") },
          { href: urls(locale).mempool.index, label: t("Mempool") },
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
