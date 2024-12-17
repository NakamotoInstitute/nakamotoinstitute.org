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

export async function generateMetadata(
  props: LocaleParams<{ slug: string; nodeSlug: string }>,
): Promise<Metadata> {
  const params = await props.params;

  const { locale, slug, nodeSlug } = params;

  const node = await getLibraryDocNode(nodeSlug, slug, locale);

  return {
    title: node.heading ? `${node.heading}: ${node.title}` : node.title,
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
    <div className="mx-auto flex w-full max-w-4.5xl justify-between gap-5 px-4">
      {node.previous ? (
        <div className="min-w-0">
          <Link
            className="group flex items-center justify-start gap-2"
            href={urls(locale).library.docNode(
              node.docSlug,
              node.previous.slug,
            )}
          >
            <ArrowLeft className="flex-shrink-0 group-hover:text-cardinal" />
            <span className="truncate">
              {node.previous.navTitle ?? node.previous.title}
            </span>
          </Link>
        </div>
      ) : null}
      {node.next ? (
        <div className="min-w-0">
          <Link
            className="ml-auto flex items-center justify-end gap-2"
            href={urls(locale).library.docNode(node.docSlug, node.next.slug)}
          >
            <span className="truncate">
              {node.next.navTitle ?? node.next.title}
            </span>
            <ArrowRight className="flex-shrink-0 group-hover:text-cardinal" />
          </Link>
        </div>
      ) : null}
    </div>
  );
}

export default async function LibraryNodeDetail(
  props: LocaleParams<{ slug: string; nodeSlug: string }>,
) {
  const params = await props.params;

  const { slug, nodeSlug, locale } = params;

  const { t } = await i18nTranslation(locale);
  const node = await getLibraryDocNode(nodeSlug, slug, locale);

  const generateHref = (l: Locale) => {
    const translation = node.translations.find((t) => t.locale === l);
    if (translation) {
      return urls(l).library.doc(translation.slug);
    }
    return urls(l).library.index;
  };

  const nodeNav = <NodeNavigation locale={locale} node={node} />;

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
      additionalNav={nodeNav}
      footerNav={nodeNav}
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
