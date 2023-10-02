import { ReactNode } from "react";
import clsx from "clsx";
import { Navbar } from "./Navbar";
import { Footer } from "./Footer";
import { generateLocaleToggleLinks, urls } from "@/lib/urls";

export function PageLayout({
  className,
  locale,
  generateHref,
  children,
}: {
  className?: string;
  generateHref?: (locale: Locale) => string;
  locale: Locale;
  children: ReactNode | ReactNode[];
}) {
  const toggleProps = generateHref
    ? generateLocaleToggleLinks(locale, generateHref)
    : {};

  return (
    <body className="flex min-h-screen flex-col">
      <Navbar
        locale={locale}
        homeHref={urls(locale).home}
        navLinks={[
          { href: urls(locale).satoshi.index, label: "The Complete Satoshi" },
        ]}
        {...toggleProps}
      />
      <main
        className={clsx(
          "mx-auto w-full max-w-7xl flex-grow px-2 py-12 md:px-6 lg:px-8",
          className,
        )}
      >
        {children}
      </main>
      <Footer locale={locale} />
    </body>
  );
}
