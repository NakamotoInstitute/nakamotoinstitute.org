import { PageLayout } from "@/app/components";

export default async function SatoshiIndex({
  params: { locale },
}: LocaleParams) {
  return (
    <PageLayout className="text-center" locale={locale}>
      The Complete Satoshi
    </PageLayout>
  );
}
