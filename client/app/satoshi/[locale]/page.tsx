import { Metadata } from "next";
import Link from "next/link";

import { Markdown } from "@/app/components/Markdown";
import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { getPage } from "@/lib/content";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";

const generateHref = (l: Locale) => urls(l).satoshi.index;

export async function generateMetadata(): Promise<Metadata> {
  const languages = generateHrefLangs([...locales], generateHref);

  return {
    alternates: { languages },
  };
}

type SatoshiSectionProps = AnchorProps & {
  children: string;
};

const SatoshiSection = ({ text, href, children }: SatoshiSectionProps) => {
  return (
    <div>
      <Link href={href} className="text-xl font-medium">
        {text}
      </Link>
      <p>{children}</p>
    </div>
  );
};

export default async function SatoshiIndex({
  params: { locale },
}: LocaleParams) {
  const { t } = await i18nTranslation(locale);
  const content = await getPage("complete-satoshi", locale);

  return (
    <PageLayout
      className="text-center"
      locale={locale}
      generateHref={generateHref}
    >
      <PageHeader title={t("The Complete Satoshi")}>
        <Markdown>{content}</Markdown>
      </PageHeader>
      <section>
        <p>
          <Link href="/satoshinakamoto.asc">
            {t("Satoshi Nakamoto&rsquo;s PGP Key")}
          </Link>
        </p>
      </section>
      <hr className="my-4" />
      <section className="mx-auto flex flex-col gap-4">
        <SatoshiSection
          text={t("The Whitepaper")}
          href={urls(locale).library.doc("bitcoin")}
        >
          {t("The original vision.")}
        </SatoshiSection>
        <SatoshiSection
          text={t("Emails")}
          href={urls(locale).satoshi.emails.index}
        >
          {t("It all began here.")}
        </SatoshiSection>
        <SatoshiSection
          text={t("Forum Posts")}
          href={urls(locale).satoshi.posts.index}
        >
          {t("Where an idea flourished.")}
        </SatoshiSection>
        <SatoshiSection text={t("Code")} href={urls(locale).satoshi.code}>
          {t("The vision instantiated.")}
        </SatoshiSection>
        <SatoshiSection
          text={t("Quotes")}
          href={urls(locale).satoshi.quotesIndex}
        >
          {t("Indexed wisdom from the quotable Satoshi.")}
        </SatoshiSection>
      </section>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
