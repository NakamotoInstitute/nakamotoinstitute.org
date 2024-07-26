import { Metadata } from "next";
import Link from "next/link";

import { ArrowLeft } from "@/app/components/ArrowLeft";
import { ArrowRight } from "@/app/components/ArrowRight";
import { PageLayout } from "@/app/components/PageLayout";
import { Rehype } from "@/app/components/Rehype";
import { getLibraryDocNode, getLibraryNodeParams } from "@/lib/api/library";
import { DocumentNode } from "@/lib/api/schemas/library";
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
    title: `${node.title} | ${node.docTitle}`,
    alternates: {
      canonical: urls(locale).library.docNode(slug, nodeSlug),
    },
  };
}

type NodeNavigationProps = {
  locale: Locale;
  node: DocumentNode;
};

async function NodeNavigation({ node, locale }: NodeNavigationProps) {
  return (
    <div className="mx-auto flex w-full max-w-[960px] flex-col gap-2 px-4 md:flex-row md:justify-between">
      {node.previous ? (
        <Link
          className="group flex gap-2 max-md:mx-auto"
          href={urls(locale).library.docNode(node.docSlug, node.previous.slug)}
        >
          <ArrowLeft className="group-hover:text-cardinal" />
          <span>{node.previous.navTitle ?? node.previous.title}</span>
        </Link>
      ) : null}
      {node.next ? (
        <Link
          className="ml-auto flex gap-2 max-md:mr-auto"
          href={urls(locale).library.docNode(node.docSlug, node.next.slug)}
        >
          <span>{node.next.navTitle ?? node.next.title}</span>
          <ArrowRight className="group-hover:text-cardinal" />
        </Link>
      ) : null}
    </div>
  );
}

export default async function LibraryNodeDetail({
  params: { slug, nodeSlug, locale },
}: LocaleParams<{ slug: string; nodeSlug: string }>) {
  const { t } = await i18nTranslation(locale);
  const node = await getLibraryDocNode(nodeSlug, slug, locale);

  const generateHref = (l: Locale) => {
    const translation = node.translations.find((t) => t.locale === l);
    if (translation) {
      return urls(l).library.doc(translation.slug);
    }
    return urls(l).library.index;
  };

  return (
    <PageLayout
      t={t}
      locale={locale}
      generateHref={generateHref}
      breadcrumbs={[
        { label: t("library"), href: urls(locale).library.index },
        {
          label: node.docTitle,
          href: urls(locale).library.doc(node.docSlug),
        },
        {
          label: node.title,
          href: urls(locale).library.docNode(slug, nodeSlug),
        },
      ]}
      additionalNav={<NodeNavigation locale={locale} node={node} />}
      size="lg"
    >
      <article>
        <NodeHeader node={node} hr={!!node.content ? "bottom" : "middle"} />
        <section className="prose mx-auto" dir={getDir(locale)}>
          <Rehype>{node.content}</Rehype>
        </section>
      </article>
    </PageLayout>
  );
}

export async function generateStaticParams() {
  return getLibraryNodeParams();
}
