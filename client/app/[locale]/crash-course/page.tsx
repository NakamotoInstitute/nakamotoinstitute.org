import { Metadata } from "next";
import Image from "next/image";

import { MarkdownContent } from "@/app/components/Markdown";
import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { getPage } from "@/lib/content";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { cdnUrl, urls } from "@/lib/urls";

const generateHref = (l: Locale) => urls(l).crashCourse;

export async function generateMetadata(props: LocaleParams): Promise<Metadata> {
  const params = await props.params;

  const { locale } = params;

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

export default async function CrashCoursePage(props: LocaleParams) {
  const params = await props.params;

  const { locale } = params;

  const { t } = await i18nTranslation(locale);

  const content = await getPage("crash-course", locale);

  return (
    <PageLayout t={t} locale={locale} generateHref={generateHref}>
      <div className="mx-auto text-center">
        <h1 className="mb-4 text-4xl leading-[1.1] font-medium md:mb-6 md:text-7xl">
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
      <MarkdownContent className="prose mx-auto">{content}</MarkdownContent>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
