import clsx from "clsx";
import { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { Trans } from "react-i18next/TransWithoutContext";

import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { getHomeLibraryDocs } from "@/lib/api/library";
import { getLatestMempoolPosts } from "@/lib/api/mempool";
import { getHomePodcasts } from "@/lib/api/podcasts";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { cdnUrl, externalUrls, urls } from "@/lib/urls";

import { ArrowRight } from "../components/ArrowRight";
import { ButtonLink } from "../components/Button";
import { DocListingAuthors } from "./library/components/DocListing";
import { PostListingAuthors } from "./mempool/components/PostListing";

const generateHref = (loc: Locale) => urls(loc).home;

export async function generateMetadata(props: LocaleParams): Promise<Metadata> {
  const params = await props.params;

  const { locale } = params;

  const languages = generateHrefLangs([...locales], generateHref);

  return {
    alternates: {
      canonical: generateHref(locale),
      languages,
    },
  };
}

type GridItemProps = {
  className?: string;
  children?: React.ReactNode;
};

async function GridItem({ className, children }: GridItemProps) {
  return (
    <div className={clsx(className, "border-dashed border-dark")}>
      {children}
    </div>
  );
}

type BoxProps = {
  title?: string;
  className?: string;
  link?: {
    href: string;
    label: string;
  };
  children?: React.ReactNode;
};

async function Box({ title, className, link, children }: BoxProps) {
  return (
    <GridItem className={clsx(className, "flex flex-col gap-5")}>
      {title ? <h3 className="text-xl font-bold">{title}</h3> : null}
      {children}
      {link ? (
        <Link
          className="mt-auto inline-flex items-center gap-1 text-sm font-medium small-caps"
          href={link.href}
        >
          <span>{link.label}</span>
          <ArrowRight />
        </Link>
      ) : null}
    </GridItem>
  );
}

export default async function HomePage(props: LocaleParams) {
  const params = await props.params;

  const { locale } = params;

  const { t } = await i18nTranslation(locale);
  const [latest, docs, podcasts] = await Promise.all([
    getLatestMempoolPosts(locale),
    getHomeLibraryDocs(locale),
    getHomePodcasts(),
  ]);

  const viewAllLabel = t("view_all");
  const readMoreLabel = t("read_more");

  return (
    <PageLayout t={t} locale={locale} size="xl" generateHref={generateHref}>
      <div className="-mx-4 grid grid-cols-1 md:grid-cols-[1fr,3fr] md:grid-rows-[28rem_auto]">
        <GridItem className="px-5 py-12 md:py-7">
          <h1 className="text-center text-3xl font-semibold md:text-left md:max-lg:text-2xl lg:text-3xl">
            {t("mission_statement")}
          </h1>
        </GridItem>
        <GridItem className="md:grid-rows[1fr_1fr_1fr_1fr_auto] grid grid-cols-1 md:row-span-2 md:grid-cols-2 md:border-l lg:grid-cols-3 min-[1441px]:border-r">
          <GridItem className="border-b pb-8 md:col-span-2 md:p-5 lg:col-span-3">
            <div className="relative h-56 w-full">
              <Image
                src={cdnUrl(
                  "/img/library/gradually-then-suddenly/GTS-Painting.jpg",
                )}
                fill
                className="object-cover"
                alt="Gradually, Then Suddenly painting"
              />
            </div>
            <div className="mt-4 flex flex-col items-baseline gap-1 max-md:px-5 lg:flex-row lg:gap-3.5">
              <h3 className="text-xl font-bold">
                <Trans
                  i18nKey="gts_announcement"
                  components={{
                    i: <em />,
                  }}
                />
              </h3>
              <Link
                className="font-semibold text-cardinal hover:underline"
                href={urls("en").library.doc("gradually-then-suddenly")}
              >
                {t("read_more")}
              </Link>
            </div>
          </GridItem>
          <Box
            title={t("complete_satoshi")}
            className="border-b px-5 py-10 md:px-4 md:py-5"
            link={{ label: viewAllLabel, href: urls(locale).satoshi.index }}
          >
            <p>{t("complete_satoshi_tag")}</p>
            <div>
              <div className="mb-2">
                <h4>
                  <Link
                    className="text-cardinal hover:underline"
                    href={urls(locale).library.doc("bitcoin")}
                  >
                    {t("the_whitepaper")}
                  </Link>
                </h4>
                <p className="text-xs">{t("original_vision")}</p>
              </div>
              <div className="mb-2">
                <h4>
                  <Link
                    className="text-cardinal hover:underline"
                    href={urls(locale).satoshi.emails.index}
                  >
                    {t("emails")}
                  </Link>
                </h4>
                <p className="text-xs">{t("it_all_began_here")}</p>
              </div>
              <div>
                <h4>
                  <Link
                    className="text-cardinal hover:underline"
                    href={urls(locale).satoshi.posts.index}
                  >
                    {t("forum_posts")}
                  </Link>
                </h4>
                <p className="text-xs">{t("idea_flourished")}</p>
              </div>
            </div>
          </Box>
          <Box
            title={t("library")}
            className="border-b px-5 py-10 md:border-l md:px-4 md:py-5"
            link={{ label: viewAllLabel, href: urls(locale).library.index }}
          >
            <p>{t("bitcoin_context")}</p>
            <div>
              {docs.map((doc) => (
                <div key={doc.slug} className="mb-2 last:mb-0">
                  <Link
                    className="text-cardinal hover:underline"
                    href={urls(locale).library.doc(doc.slug)}
                  >
                    {doc.title}
                  </Link>
                  <DocListingAuthors locale={locale} doc={doc} small />
                </div>
              ))}
            </div>
          </Box>
          <Box
            title={t("memory_pool")}
            className="border-b px-5 py-10 md:px-4 md:py-5 lg:border-l"
            link={{ label: viewAllLabel, href: urls(locale).mempool.index }}
          >
            <p>{t("memory_pool_description")}</p>
            <div>
              {latest.map((post) => (
                <div key={post.slug} className="mb-2 last:mb-0">
                  <h4>
                    <Link
                      className="text-cardinal hover:underline"
                      href={urls(locale).mempool.post(post.slug)}
                    >
                      {post.title}
                    </Link>
                  </h4>
                  <PostListingAuthors locale={locale} post={post} small />
                </div>
              ))}
            </div>
          </Box>

          <Box
            title={t("crash_course")}
            className="border-b px-5 py-10 md:px-4 md:py-5 md:max-lg:border-l"
            link={{ label: readMoreLabel, href: urls(locale).crashCourse }}
          >
            <p>{t("crash_course_description")}</p>
          </Box>
          <Box
            title={t("the_skeptics")}
            className="border-b px-5 py-10 md:px-4 md:py-5 lg:border-l"
            link={{ label: readMoreLabel, href: urls(locale).skeptics }}
          >
            <p>{t("skeptics_tribute")}</p>
          </Box>
          <Box
            title={t("hal_finney_tribute")}
            className="border-b px-5 py-10 md:border-l md:px-4 md:py-5"
            link={{ label: readMoreLabel, href: urls(locale).finney.index }}
          >
            <p>{t("finney_tag")}</p>
            <div>
              <h4>
                <Link
                  className="text-cardinal hover:underline"
                  href={urls(locale).finney.rpow}
                >
                  {t("rpow_title")}
                </Link>
              </h4>
              <p className="text-xs">{t("rpow_tag")}</p>
            </div>
          </Box>
          <Box
            title={t("podcasts")}
            className="border-b px-5 py-10 md:border-b-0 md:px-4 md:py-5"
            link={{ label: viewAllLabel, href: urls(locale).podcasts.index }}
          >
            <p>{t("podcast_description")}</p>
            <div>
              {podcasts.map((podcast) => (
                <div key={podcast.slug} className="mb-2 last:mb-0">
                  <div className="flex items-center gap-2">
                    <h4 className="inline-block">
                      <Link
                        className="text-cardinal hover:underline"
                        href={urls(locale).podcasts.show(podcast.slug)}
                      >
                        {podcast.name}
                      </Link>
                    </h4>
                    {podcast.defunct && (
                      <span
                        className="text-xs text-gray-600"
                        dir={locale === "ar" ? "rtl" : "ltr"}
                      >
                        [{t("defunct")}]
                      </span>
                    )}
                  </div>
                  <p className="text-xs">
                    {podcast.descriptionShort ?? podcast.description}
                  </p>
                </div>
              ))}
            </div>
          </Box>
          <Box
            title={t("get_involved")}
            className="border-b px-5 py-10 md:border-b-0 md:border-l md:px-4 md:py-5"
            link={{ label: readMoreLabel, href: urls(locale).getInvolved }}
          >
            <p>{t("get_involved_call")}</p>
          </Box>
          <GridItem className="md:min-h-48 lg:border-l" />
          <GridItem className="hidden md:block md:min-h-48" />
        </GridItem>
        <GridItem className="px-5 py-4 md:pt-0">
          <div className="flex flex-col gap-4">
            <Link href={externalUrls.substack}>
              <div className="flex items-center justify-between gap-4 border border-dashed border-taupe-light p-4 md:items-start">
                <div>
                  <h4 className="font-semibold">{t("newsletter_call")}</h4>
                  <p className="text-sm text-taupe">{t("newsletter_signup")}</p>
                </div>
                <ArrowRight className="min-w-fit" />
              </div>
            </Link>
            <div className="border-l-[3px] border-cardinal bg-white p-4 shadow-sm">
              <div className="text-xs text-taupe">
                <h4 className="mb-2 text-base font-semibold text-dark">
                  {t("support")}
                </h4>
                <p className="mb-2">{t("donation_message")}</p>
                <p className="italic">
                  <Trans
                    i18nKey="donation_message_cont"
                    components={{
                      strong: <strong />,
                    }}
                  />
                </p>
              </div>
              <hr className="my-4 border-taupe-light" />
              <div>
                <ButtonLink
                  className="flex gap-1"
                  href={urls(locale).donate.zaprite}
                >
                  <span>{t("donate")}</span>
                  <ArrowRight />
                </ButtonLink>
              </div>
            </div>
          </div>
        </GridItem>
      </div>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
