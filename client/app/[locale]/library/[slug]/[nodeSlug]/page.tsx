import { Metadata } from "next";
import Link from "next/link";

import { PageLayout } from "@/app/components/PageLayout";
import { Rehype } from "@/app/components/Rehype";
import { getLibraryDocNode, getLibraryParams } from "@/lib/api/library";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { getDir } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";

import { NodeHeader } from "../../components/NodeHeader";

export const dynamicParams = false;

export async function generateMetadata({
  params: { locale, slug, nodeSlug },
}: LocaleParams<{ slug: string; nodeSlug: string }>): Promise<Metadata> {
  const node = await getLibraryDocNode(nodeSlug, slug, locale);

  return {
    title: node.title,
    alternates: {
      canonical: urls(locale).library.docNode(slug, nodeSlug),
    },
  };
}

export default async function LibraryDetail({
  params: { slug, nodeSlug, locale },
}: LocaleParams<{ slug: string; nodeSlug: string }>) {
  const { t } = await i18nTranslation(locale);
  const node = await getLibraryDocNode(nodeSlug, slug, locale);

  const backHref = urls(locale).library.index;
  const backLabel = t("back_to_library");

  const generateHref = (l: Locale) => {
    const translation = node.translations.find((t) => t.locale === l);
    if (translation) {
      return urls(l).library.doc(translation.slug);
    }
    return urls(l).library.index;
  };

  return (
    <PageLayout t={t} locale={locale} generateHref={generateHref}>
      <Link className="mb-4 block text-center" href={backHref}>
        {backLabel}
      </Link>
      <div>
        <div>
          {node.previous ? (
            <>
              Previous:{" "}
              <Link
                href={urls(locale).library.docNode(slug, node.previous.slug)}
              >
                {node.previous.navTitle ?? node.previous.title}
              </Link>
            </>
          ) : null}
        </div>
        <div>
          {node.next ? (
            <>
              Next:{" "}
              <Link href={urls(locale).library.docNode(slug, node.next.slug)}>
                {node.next.navTitle ?? node.next.title}
              </Link>
            </>
          ) : null}
        </div>
      </div>
      <article>
        <NodeHeader t={t} locale={locale} node={node} />
        <section className="prose mx-auto" dir={getDir(locale)}>
          <Rehype>{node.content}</Rehype>
        </section>
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
