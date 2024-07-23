import clsx from "clsx";
import { TFunction } from "i18next";
import Image from "next/image";

import { env } from "@/env";
import { cdnUrl, generateLocaleToggleLinks, urls } from "@/lib/urls";

import { Breadcrumbs } from "./Breadcrumbs";
import { ButtonLink } from "./Button";
import Fathom from "./Fathom";
import { Footer } from "./Footer";
import { Navbar } from "./Navbar";

export type PageLayoutProps = {
  t: TFunction<string, string>;
  className?: string;
  generateHref?: (locale: Locale) => string;
  wide?: boolean;
  locale: Locale;
  breadcrumbs?: Breadcrumbs;
  children: React.ReactNode;
};

export async function PageLayout({
  t,
  className,
  locale,
  generateHref,
  breadcrumbs,
  wide = false,
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
        logo={
          <Image
            src={cdnUrl("/img/navbar-logo.svg")}
            width={121}
            height={48}
            alt="SNI logo with text"
          />
        }
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
        navButtons={[
          <ButtonLink key="donate" href={urls(locale).donate.index}>
            {t("donate")}
          </ButtonLink>,
        ]}
        {...toggleProps}
      />
      {breadcrumbs ? <Breadcrumbs breadcrumbs={breadcrumbs} /> : null}
      <main
        className={clsx(
          "mx-auto my-10 w-full flex-grow px-4 pb-4 md:mt-18",
          wide ? "max-w-[960px]" : "max-w-[872px]",
          className,
        )}
      >
        {children}
      </main>
      <Footer t={t} locale={locale} />
    </body>
  );
}
