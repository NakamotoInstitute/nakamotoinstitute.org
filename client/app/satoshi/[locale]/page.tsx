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
      t={t}
      className="text-center"
      locale={locale}
      generateHref={generateHref}
    >
      <PageHeader title={t("complete_satoshi")}>
        <Markdown>{content}</Markdown>
      </PageHeader>
      <section>
        <p>
          <Link href="/satoshinakamoto.asc">{t("satoshi_pgp_key")}</Link>
        </p>
      </section>
      <hr className="my-4" />
      <section className="mx-auto flex flex-col gap-4">
        <SatoshiSection
          text={t("the_whitepaper")}
          href={urls(locale).library.doc("bitcoin")}
        >
          {t("original_vision")}
        </SatoshiSection>
        <SatoshiSection
          text={t("emails")}
          href={urls(locale).satoshi.emails.index}
        >
          {t("it_all_began_here")}
        </SatoshiSection>
        <SatoshiSection
          text={t("forum_posts")}
          href={urls(locale).satoshi.posts.index}
        >
          {t("idea_flourished")}
        </SatoshiSection>
        <SatoshiSection text={t("code")} href={urls(locale).satoshi.code}>
          {t("vision_instantiated")}
        </SatoshiSection>
        <SatoshiSection
          text={t("quotes")}
          href={urls(locale).satoshi.quotesIndex}
        >
          {t("indexed_wisdom")}
        </SatoshiSection>
      </section>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
