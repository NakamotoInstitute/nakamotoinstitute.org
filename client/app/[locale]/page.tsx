import { PageLayout } from "../components";

export default function HomePage({ params: { locale } }: LocaleParams) {
  return (
    <PageLayout locale={locale}>
      <h1>Satoshi Nakamoto Institute</h1>
    </PageLayout>
  );
}
