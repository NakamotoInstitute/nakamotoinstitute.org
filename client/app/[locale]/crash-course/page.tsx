import { Metadata } from "next";
import Image from "next/image";

import { Markdown } from "@/app/components/Markdown";
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
      <div className="mx-auto text-center">
        <h1 className="mb-4 text-4xl font-medium leading-[1.1] md:mb-6 md:text-7xl">
          {t("sni_mempool_crash_course")}
        </h1>
        <Image
          className="mx-auto my-4"
          src={cdnUrl("/img/mempool/hyperbitcoinization/BitcoinFace.png")}
          alt={t("hyperbitcoinization")}
          width={600}
          height={341}
        />
      </div>
      <hr className="mx-auto my-7 w-12 md:my-18" />
      <Markdown className="prose mx-auto">{content}</Markdown>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
