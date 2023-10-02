import { PageLayout } from "@/app/components";
import { getLocaleParams, i18nTranslation } from "@/lib/i18n";

export default async function HomePage({ params: { locale } }: LocaleParams) {
  const { t } = await i18nTranslation(locale);

  return (
    <PageLayout locale={locale}>
      <section>
        <h1>
          {t(
            "I've been working on a new electronic cash system that's fully peer-to-peer, with no trusted third party...",
          )}
        </h1>
      </section>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
