import { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { getForumPost, getSatoshiPosts } from "@/lib/api/posts";
import { ForumPostSource } from "@/lib/api/schemas/posts";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";
import { formatPostSource } from "@/utils/strings";

import { PostNavigation } from "@satoshi/components/ContentNavigation";

import {
  ContentBox,
  ContentBoxBody,
  ContentBoxFooter,
  ContentBoxHeader,
} from "../../../components/ContentBox";
import { ContentPageHeader } from "../../../components/ContentPageHeader";

export const dynamicParams = false;

const generateHref =
  (source: ForumPostSource, satoshiId: string) => (l: Locale) =>
    urls(l).satoshi.posts.sourcePost(source, satoshiId);

export async function generateMetadata({
  params: { locale, source, satoshiId },
}: LocaleParams<{
  source: ForumPostSource;
  satoshiId: string;
}>): Promise<Metadata> {
  const postData = await getForumPost(source, satoshiId);
  const languages = generateHrefLangs(
    [...locales],
    generateHref(source, satoshiId),
  );

  return {
    title: postData.post.subject,
    alternates: {
      canonical: generateHref(source, satoshiId)(locale),
      languages,
    },
  };
}

export default async function PostDetail({
  params: { source, satoshiId, locale },
}: LocaleParams<{ source: ForumPostSource; satoshiId: string }>) {
  const postData = await getForumPost(source, satoshiId);
  if (!postData) {
    return notFound();
  }

  const { t } = await i18nTranslation(locale);
  const { next, previous, post } = postData;

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
      <ContentPageHeader
        source={formatPostSource(post.source)}
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
      </ContentPageHeader>

      <ContentBox>
        <ContentBoxHeader
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
