import { Metadata } from "next";
import Image from "next/image";

import { Markdown } from "@/app/components/Markdown";
import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { getPage } from "@/lib/content";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { cdnUrl, urls } from "@/lib/urls";

const generateHref = (l: Locale) => urls(l).crashCourse;

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs([...locales], generateHref);

  return {
    title: t("sni_mempool_crash_course"),
    alternates: {
      canonical: generateHref(locale),
      languages,
    },
  };
}

export default async function CrashCoursePage({
  params: { locale },
}: LocaleParams) {
  const { t } = await i18nTranslation(locale);

  const content = await getPage("crash-course", locale);

  return (
    <PageLayout t={t} locale={locale} generateHref={generateHref}>
      <PageHeader title={t("sni_mempool_crash_course")}>
        <Image
          className="mx-auto my-4"
          src={cdnUrl("/img/mempool/hyperbitcoinization/BitcoinFace.png")}
          alt={t("hyperbitcoinization")}
          width={600}
          height={341}
        />
      </PageHeader>
      <Markdown className="prose mx-auto">{content}</Markdown>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
