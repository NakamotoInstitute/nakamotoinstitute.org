import Link from "next/link";
import { PageLayout } from "@/app/components";
import { ForumPostSource, getForumPost, getSatoshiPosts } from "@/lib/api";
import { getLocaleParams, i18nTranslation } from "@/lib/i18n";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";
import { formatPostSource } from "@/utils/strings";
import { notFound } from "next/navigation";
import { PostNavigation } from "@satoshi/components/ContentNavigation";

export default async function PostDetail({
  params: { source, satoshiId, locale },
}: LocaleParams<{ source: ForumPostSource; satoshiId: string }>) {
  const { t } = await i18nTranslation(locale);
  const postData = await getForumPost(source, satoshiId);

  if (!postData) {
    return notFound();
  }

  const { next, previous, post } = postData;
  const generateHref = (l: Locale) =>
    urls(l).satoshi.posts.sourcePost(source, satoshiId);

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PostNavigation locale={locale} previous={previous} next={next} />
      <div>
        <h2 className="text-2xl">{formatPostSource(post.source)}</h2>
        <h1 className="text-4xl">{post.subject}</h1>
        <p className="text-xl">
          <time dateTime={post.date.toISOString()}>
            {formatDate(locale, post.date, {
              dateStyle: "long",
              timeStyle: "long",
              hourCycle: "h24",
            })}
          </time>
        </p>
        <div className="flex gap-2">
          <Link href={post.url}>{t("Original post")}</Link> •{" "}
          <Link
            href={{
              pathname: urls(locale).satoshi.posts.sourceThreadsDetail(
                post.source,
                post.threadId.toString(),
              ),
              hash: post.sourceId.toString(),
            }}
          >
            {t("View in thread")}
          </Link>
        </div>
      </div>
      <hr className="my-4" />
      <div
        dangerouslySetInnerHTML={{
          __html: post.text,
        }}
      />
      <PostNavigation locale={locale} previous={previous} next={next} />
    </PageLayout>
  );
}

export async function generateStaticParams() {
  const posts = await getSatoshiPosts();
  return getLocaleParams((locale) =>
    posts
      .filter((p) => p.satoshiId)
      .map((p) => ({
        locale,
        source: p.source,
        satoshiId: p.satoshiId!.toString(),
      })),
  );
}
