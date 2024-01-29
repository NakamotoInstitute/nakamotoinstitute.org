import { Metadata } from "next";
import Link from "next/link";

import { PageLayout } from "@/app/components/PageLayout";
import { Rehype } from "@/app/components/Rehype";
import { getLibraryDoc, getLibraryParams } from "@/lib/api/library";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { getDir } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";

import { DocHeader } from "../components/DocHeader";

export const dynamicParams = false;

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
  const { t } = await i18nTranslation(locale);
  const doc = await getLibraryDoc(slug, locale);

  const backHref = urls(locale).library.index;
  const backLabel = t("Back to library");

  const generateHref = (l: Locale) => {
    const translation = doc.translations?.find((t) => t.locale === l);
    if (translation) {
      return urls(l).library.doc(translation.slug);
    }
    return urls(l).library.index;
  };

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <Link className="mb-4 block text-center" href={backHref}>
        {backLabel}
      </Link>
      <article>
        <DocHeader locale={locale} doc={doc} />
        {doc.content ? (
          <>
            <section className="prose mx-auto" dir={getDir(locale)}>
              <Rehype hasMath={doc.hasMath}>{doc.content}</Rehype>
            </section>
          </>
        ) : null}
      </article>
      <Link className="mt-4 block text-center" href={backHref}>
        {backLabel}
      </Link>
    </PageLayout>
  );
}

export async function generateStaticParams() {
  return getLibraryParams();
}
