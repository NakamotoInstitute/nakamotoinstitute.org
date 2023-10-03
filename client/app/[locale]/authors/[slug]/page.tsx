import { Metadata } from "next";
import { PageLayout } from "@/app/components";
import { PageHeader } from "@/app/components/PageHeader";
import { getAuthor, getAuthorParams } from "@/lib/api";
import { urls } from "@/lib/urls";

export const dynamicParams = false;

export async function generateMetadata({
  params: { locale, slug },
}: LocaleParams<{ slug: string }>): Promise<Metadata> {
  const { author } = await getAuthor(slug, locale);
  return {
    title: author.name,
  };
}

export default async function AuthorDetail({
  params: { slug, locale },
}: LocaleParams<{ slug: string }>) {
  const { author } = await getAuthor(slug, locale);

  const generateHref = (l: Locale) => urls(l).authors.detail(slug);

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title={author.name} />
    </PageLayout>
  );
}

export async function generateStaticParams() {
  return getAuthorParams();
}
