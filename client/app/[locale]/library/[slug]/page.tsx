import { Metadata } from "next";
import Link from "next/link";
import { Trans } from "react-i18next/TransWithoutContext";

import { PageLayout } from "@/app/components/PageLayout";
import { Rehype } from "@/app/components/Rehype";
import { RenderedItemsList } from "@/app/components/RenderedItemsList";
import { getLibraryDoc, getLibraryParams } from "@/lib/api/library";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { getDir } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";

import { TranslationLinks } from "../../mempool/components/TranslationLinks";
import { DocHeader } from "../components/DocHeader";

export const dynamicParams = false;

export async function generateMetadata({
  params: { locale, slug },
}: LocaleParams<{ slug: string }>): Promise<Metadata> {
  const doc = await getLibraryDoc(slug, locale);
  const languages = doc.translations.reduce(
    (acc, t) => {
      acc[t.locale] = urls(t.locale).library.doc(t.slug);
      return acc;
    },
    {} as Record<Locale, string>,
  );

  return {
    title: doc.title,
    alternates: {
      canonical: urls(locale).library.doc(slug),
      languages,
    },
  };
}

export default async function LibraryDetail({
  params: { slug, locale },
}: LocaleParams<{ slug: string }>) {
  const { t } = await i18nTranslation(locale);
  const doc = await getLibraryDoc(slug, locale);

  const backHref = urls(locale).library.index;
  const backLabel = t("back_to_library");

  const generateHref = (l: Locale) => {
    const translation = doc.translations.find((t) => t.locale === l);
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
      <article>
        <DocHeader t={t} locale={locale} doc={doc} />
        {doc.content ? (
          <>
            <section className="prose mx-auto md:prose-lg" dir={getDir(locale)}>
              <Rehype hasMath={doc.hasMath}>{doc.content}</Rehype>
              {doc.translators.length > 0 ? (
                <>
                  <hr />
                  <p>
                    <Trans
                      t={t}
                      i18nKey="translated_by"
                      components={{
                        links: (
                          <RenderedItemsList
                            as="span"
                            locale={locale}
                            items={doc.translators}
                            renderItem={(item) =>
                              item.url ? (
                                <Link key={item.slug} href={item.url}>
                                  {item.name}
                                </Link>
                              ) : (
                                item.name
                              )
                            }
                          />
                        ),
                      }}
                    />
                  </p>
                </>
              ) : null}
              {doc.translations.length > 0 ? (
                <>
                  <hr />
                  <p>
                    <Trans
                      t={t}
                      i18nKey="translation_links"
                      components={{
                        links: (
                          <TranslationLinks
                            locale={locale}
                            translations={doc.translations}
                            urlFunc={(item) =>
                              urls(item.locale).library.doc(item.slug)
                            }
                          />
                        ),
                      }}
                    />
                  </p>
                </>
              ) : null}
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
