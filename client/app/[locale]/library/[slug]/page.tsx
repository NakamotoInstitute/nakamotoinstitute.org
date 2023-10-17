import { Metadata } from "next";
import { Markdown, PageLayout } from "@/app/components";
import { getLibraryDoc, getLibraryParams } from "@/lib/api";
import { urls } from "@/lib/urls";
import { DocHeader } from "../components/DocHeader";

export async function generateMetadata({
  params: { locale, slug },
}: LocaleParams<{ slug: string }>): Promise<Metadata> {
  const doc = await getLibraryDoc(slug, locale);
  return {
    title: doc.title,
  };
}

export default async function LibraryDetail({
  params: { slug, locale },
}: LocaleParams<{ slug: string }>) {
  const doc = await getLibraryDoc(slug, locale);
  const generateHref = (l: Locale) => {
    const translation = doc.translations?.find((t) => t.locale === l);
    if (translation) {
      return urls(l).library.doc(translation.slug);
    }
    return urls(l).library.index;
  };

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <article>
        <DocHeader locale={locale} doc={doc} />
        {doc.content ? (
          <section className="prose mx-auto">
            <Markdown hasMath={doc.hasMath}>{doc.content}</Markdown>
          </section>
        ) : null}
      </article>
    </PageLayout>
  );
}

export async function generateStaticParams() {
  return getLibraryParams();
}
