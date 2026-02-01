import { Metadata } from "next";

import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { ForumPostSource, api, getOrNotFound } from "@/lib/api";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatPostSource } from "@/utils/strings";

import {
  ContentBox,
  ContentBoxBody,
  ContentBoxDisclaimer,
  ContentBoxFooter,
  ContentBoxHeader,
} from "@satoshi/components/ContentBox";
import { PostNavigation } from "@satoshi/components/ContentNavigation";

export const dynamicParams = false;

const generateHref =
  (source: ForumPostSource, satoshiId: string) => (l: Locale) =>
    urls(l).satoshi.posts.sourcePost(source, satoshiId);

export async function generateMetadata(
  props: LocaleParams<{
    source: ForumPostSource;
    satoshiId: string;
  }>,
): Promise<Metadata> {
  const params = await props.params;

  const { locale, source, satoshiId } = params;

  const postData = await getOrNotFound(
    api.satoshi.getForumPostBySource({
      path: { source, satoshi_id: parseInt(satoshiId) },
    }),
  );
  const languages = generateHrefLangs(locales, generateHref(source, satoshiId));

  return {
    title: postData.post.subject,
    alternates: {
      canonical: generateHref(source, satoshiId)(locale),
      languages,
    },
  };
}

export default async function PostDetail(
  props: LocaleParams<{ source: ForumPostSource; satoshiId: string }>,
) {
  const params = await props.params;

  const { source, satoshiId, locale } = params;

  const { next, previous, post } = await getOrNotFound(
    api.satoshi.getForumPostBySource({
      path: { source, satoshi_id: parseInt(satoshiId) },
    }),
  );

  const { t } = await i18nTranslation(locale);

  return (
    <PageLayout
      t={t}
      locale={locale}
      generateHref={generateHref(source, satoshiId)}
      breadcrumbs={[
        { label: t("complete_satoshi"), href: urls(locale).satoshi.index },
        { label: t("forum_posts"), href: urls(locale).satoshi.posts.index },
        {
          label: formatPostSource(source),
          href: urls(locale).satoshi.posts.sourceIndex(source),
        },
      ]}
    >
      <PageHeader
        superTitle={formatPostSource(post.source)}
        title={post.subject}
      >
        <PostNavigation
          t={t}
          locale={locale}
          id={post.satoshiId}
          source={post.source}
          previous={previous}
          next={next}
        />
      </PageHeader>

      <ContentBox>
        <ContentBoxHeader
          t={t}
          locale={locale}
          from={post.posterName}
          subject={post.subject}
          date={post.date}
        />
        <ContentBoxBody>
          <div
            dangerouslySetInnerHTML={{
              __html: post.text,
            }}
          />
        </ContentBoxBody>
        {post.disclaimer && (
          <ContentBoxDisclaimer t={t} disclaimer={post.disclaimer} />
        )}
        <ContentBoxFooter
          t={t}
          hrefs={{
            original: post.url,
            thread: {
              pathname: urls(locale).satoshi.posts.sourceThreadsDetail(
                source,
                post.threadId.toString(),
              ),
              hash: post.sourceId.toString(),
            },
          }}
        />
      </ContentBox>
    </PageLayout>
  );
}

// export async function generateStaticParams() {
//   const posts = await getSatoshiPosts();
//   return getLocaleParams((locale) =>
//     posts
//       .filter((p) => p.satoshiId)
//       .map((p) => ({
//         locale,
//         source: p.source,
//         satoshiId: p.satoshiId!.toString(),
//       })),
//   );
// }
