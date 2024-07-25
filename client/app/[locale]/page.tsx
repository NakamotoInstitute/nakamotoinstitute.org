import clsx from "clsx";
import { Metadata } from "next";
import Link from "next/link";

import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { getLatestMempoolPost } from "@/lib/api/mempool";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";

import { ArrowRight } from "../components/ArrowRight";
import { ButtonLink } from "../components/Button";

const generateHref = (loc: Locale) => urls(loc).home;

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
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

export default async function HomePage({ params: { locale } }: LocaleParams) {
  const { t } = await i18nTranslation(locale);
  const latest = await getLatestMempoolPost(locale);

  return (
    <PageLayout
      t={t}
      locale={locale}
      size="xl"
      className="pb-0"
      generateHref={generateHref}
    >
      <div className="-mx-4 grid grid-cols-1 md:grid-cols-[1fr,3fr] md:grid-rows-2">
        <GridItem className="px-5 py-12 text-center text-3xl font-semibold md:px-8 md:py-7 md:text-left md:max-lg:text-2xl lg:text-3xl">
          The Satoshi Nakamoto Institute is advancing and preserving bitcoin
          knowledge
        </GridItem>
        <GridItem className="md:grid-rows[1fr_1fr_1fr_1fr_auto] grid grid-cols-1 md:row-span-2 md:grid-cols-2 md:border-l md:border-r lg:grid-cols-3">
          <GridItem className="border-b pb-8 md:col-span-2 md:p-5 lg:col-span-3">
            Update about something new
          </GridItem>
          <Box
            title="The Complete Satoshi"
            className="border-b px-5 py-10 md:px-4 md:py-5"
            link={{ label: "View all", href: urls(locale).satoshi.index }}
          >
            <div>
              <div className="mb-2">
                <h4>
                  <Link
                    className="text-cardinal hover:underline"
                    href={urls(locale).library.doc("bitcoin")}
                  >
                    The Whitepaper
                  </Link>
                </h4>
                <p className="text-xs">The original vision</p>
              </div>
              <div className="mb-2">
                <h4>
                  <Link
                    className="text-cardinal hover:underline"
                    href={urls(locale).satoshi.emails.index}
                  >
                    Emails
                  </Link>
                </h4>
                <p className="text-xs">It all began here</p>
              </div>
              <div>
                <h4>
                  <Link
                    className="text-cardinal hover:underline"
                    href={urls(locale).satoshi.posts.index}
                  >
                    Forum Posts
                  </Link>
                </h4>
                <p className="text-xs">Where an idea flourished</p>
              </div>
            </div>
          </Box>
          <Box
            title="Library"
            className="border-b px-5 py-10 md:border-l md:px-4 md:py-5"
            link={{ label: "View all", href: urls(locale).library.index }}
          >
            <p>{t("bitcoin_context")}</p>
          </Box>
          <Box
            title="The Mempool"
            className="border-b px-5 py-10 md:px-4 md:py-5 lg:border-l"
            link={{ label: "View all", href: urls(locale).mempool.index }}
          >
            <p>
              Where ideas wait to be mined into the blockchain of the collective
              conscience. Some transactions may be invalid.
            </p>
          </Box>

          <Box
            title="Crash Course"
            className="border-b px-5 py-10 md:px-4 md:py-5 md:max-lg:border-l"
            link={{ label: "Read more", href: urls(locale).crashCourse }}
          >
            <p>
              A partial annotated bibliography of the Mempool, building the case
              for why bitcoin will displace all competing currencies, including
              altcoins, fiat money, and precious metals.
            </p>
          </Box>
          <Box
            title="The Skeptics"
            className="border-b px-5 py-10 md:px-4 md:py-5 lg:border-l"
            link={{ label: "Read more", href: urls(locale).skeptics }}
          >
            <p>A tribute to bold assertions.</p>
          </Box>
          <Box
            title="Tribute to Hal Finney"
            className="border-b px-5 py-10 md:border-l md:px-4 md:py-5"
            link={{ label: "Read more", href: urls(locale).finney.index }}
          >
            <p>Celebrating the cypherpunk and early bitcoin developer</p>
            <div>
              <h4>
                <Link
                  className="text-cardinal hover:underline"
                  href={urls(locale).finney.rpow}
                >
                  RPOW - Reusable Proofs of Work
                </Link>
              </h4>
              <p className="text-xs">See the original code and website</p>
            </div>
          </Box>
          <Box
            title="Podcast"
            className="border-b px-5 py-10 md:border-b-0 md:px-4 md:py-5"
            link={{ label: "Read more", href: urls(locale).podcast.index }}
          >
            <p>
              Recorded in 2014 and 2015, the Crypto-Mises Podcast featured
              discussions on bitcoin economics.
            </p>
          </Box>
          <Box
            title="Get Involved"
            className="border-b px-5 py-10 md:border-b-0 md:border-l md:px-4 md:py-5"
            link={{ label: "Read more", href: urls(locale).getInvolved }}
          >
            <p>Help us educate the world about bitcoin.</p>
          </Box>
          <GridItem className="md:min-h-48 lg:border-l" />
          <GridItem className="hidden md:block md:min-h-48" />
        </GridItem>
        <GridItem className="px-6">
          <div className="flex flex-col gap-4">
            <div className="flex gap-4 border border-dashed border-taupe-light p-4">
              <div>
                <h4 className="font-semibold">Read our newsletter</h4>
                <p className="text-sm text-taupe">
                  Receive email updates about the Satoshi Nakamoto Institute
                </p>
              </div>
              <ArrowRight className="min-w-fit" />
            </div>
            <div className="border-l-[3px] border-cardinal bg-white p-4 shadow-sm">
              <div className="text-xs text-taupe">
                <h4 className="mb-2 text-base font-semibold text-dark">
                  Support SNI
                </h4>
                <p className="mb-2">
                  Donate to help us advance and preserve bitcoin knowledge. The
                  Satoshi Nakamoto Institute is a qualified 501(c)(3) nonprofit
                  organization.
                </p>
                <p className="italic">
                  Contributions to SNI are <strong>tax-deductible</strong> and
                  support the proliferation of bitcoin education worldwide.
                </p>
              </div>
              <hr className="my-4 border-taupe-light" />
              <div>
                <ButtonLink
                  className="flex gap-1"
                  href={urls(locale).donate.index}
                >
                  <span>Donate</span>
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
