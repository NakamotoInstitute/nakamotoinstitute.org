import { PageLayout } from "@/app/components";
import { getLocaleParams, i18nTranslation } from "@/lib/i18n";

export default async function SatoshiIndex({
  params: { locale },
}: LocaleParams) {
  const { t } = await i18nTranslation(locale);

  return (
    <PageLayout className="text-center" locale={locale}>
      {t("The Complete Satoshi")}
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
