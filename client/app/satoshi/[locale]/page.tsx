import { PageLayout } from "@/app/components";
import { getLocaleParams, i18nTranslation } from "@/lib/i18n";
import { urls } from "@/lib/urls";

export default async function SatoshiIndex({
  params: { locale },
}: LocaleParams) {
  const { t } = await i18nTranslation(locale);
  const generateHref = (l: Locale) => urls(l).satoshi.index;

  return (
    <PageLayout
      className="text-center"
      locale={locale}
      generateHref={generateHref}
    >
      {t("The Complete Satoshi")}
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
