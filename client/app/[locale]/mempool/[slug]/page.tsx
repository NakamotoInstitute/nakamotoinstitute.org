import { Metadata } from "next";
import { Rehype } from "@/app/components/Rehype";
import { getMempoolPost, getMempoolParams } from "@/lib/api/mempool";
import { PageLayout } from "@/app/components/PageLayout";
import { getDir } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { PostHeader } from "../components/PostHeader";

export const dynamicParams = false;

export async function generateMetadata({
  params: { locale, slug },
}: LocaleParams<{ slug: string }>): Promise<Metadata> {
  const post = await getMempoolPost(slug, locale);
  return {
    title: post.title,
  };
}

export default async function MempoolPost({
  params: { slug, locale },
}: LocaleParams<{ slug: string }>) {
  const post = await getMempoolPost(slug, locale);

  const generateHref = (l: Locale) => {
    const translation = post.translations?.find((t) => t.locale === l);
    if (translation) {
      return urls(l).mempool.post(translation.slug);
    }
    return urls(l).mempool.index;
  };

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <article>
        <PostHeader locale={locale} post={post} />
        <section className="prose mx-auto" dir={getDir(locale)}>
          <Rehype hasMath={post.hasMath}>{post.content}</Rehype>
        </section>
      </article>
    </PageLayout>
  );
}

export async function generateStaticParams() {
  return getMempoolParams();
}
