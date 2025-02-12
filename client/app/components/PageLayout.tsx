import clsx from "clsx";
import { TFunction } from "i18next";
import Image from "next/image";

import { env } from "@/env";
import {
  cdnUrl,
  externalUrls,
  generateLocaleToggleLinks,
  urls,
} from "@/lib/urls";

import { AdditionalNavigation } from "./AdditionalNavigation";
import { Breadcrumbs } from "./Breadcrumbs";
import { ButtonLink } from "./Button";
import Fathom from "./Fathom";
import { Footer } from "./Footer";
import { Navbar } from "./Navbar";

export type PageLayoutProps = {
  t: TFunction<string, string>;
  className?: string;
  generateHref?: (locale: Locale) => string;
  size?: "md" | "lg" | "xl";
  locale: Locale;
  breadcrumbs?: Breadcrumbs;
  additionalNav?: React.ReactNode;
  footerNav?: React.ReactNode;
  children: React.ReactNode;
};

export async function PageLayout({
  t,
  className,
  locale,
  generateHref,
  breadcrumbs,
  additionalNav,
  footerNav,
  size = "md",
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
          { href: externalUrls.substack, text: t("newsletter") },
        ]}
        navButtons={[
          <ButtonLink key="donate" href={urls(locale).donate.zaprite}>
            {t("donate")}
          </ButtonLink>,
        ]}
        {...toggleProps}
      />
      {breadcrumbs ? <Breadcrumbs breadcrumbs={breadcrumbs} /> : null}
      {additionalNav ? (
        <AdditionalNavigation>{additionalNav}</AdditionalNavigation>
      ) : null}
      <main
        className={clsx(className, "mx-auto w-full flex-grow px-4", {
          "max-w-3.5xl": size === "md",
          "max-w-4.5xl": size === "lg",
          "max-w-screen-1.5xl": size === "xl",
          "my-10 pb-4 md:mt-18": size !== "xl",
        })}
      >
        {children}
      </main>
      {footerNav ? (
        <AdditionalNavigation bottom>{footerNav}</AdditionalNavigation>
      ) : null}
      <Footer t={t} locale={locale} />
    </body>
  );
}
