import { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { Trans } from "react-i18next/TransWithoutContext";

import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { getLatestMempoolPost } from "@/lib/api/mempool";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { cdnUrl, urls } from "@/lib/urls";

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

type HomeSectionProps = {
  title: string;
  button: AnchorProps;
  children: React.ReactNode;
};

const HomeSection = ({ title, button, children }: HomeSectionProps) => {
  return (
    <div className="flex flex-1 flex-col px-4">
      <div className="mb-4 text-neutral-800">
        <h2 className="mb-2 mt-0 break-after-avoid text-3xl font-medium">
          {title}
        </h2>
        {children}
      </div>
      <div className="mt-auto text-neutral-800">
        <p className="mb-4 mt-0">
          <a
            className="inline-block cursor-pointer select-none rounded border border-solid border-blue-500 bg-blue-500 px-3 py-1 text-center align-middle text-base font-normal leading-normal text-white hover:border-blue-600 hover:bg-blue-600 hover:text-white focus:border-blue-600 focus:bg-blue-600 focus:text-white"
            href={button.href}
            role="button"
          >
            {button.text} »
          </a>
        </p>
      </div>
    </div>
  );
};

type BannerProps = {
  children: React.ReactNode;
};

const Banner = ({ children }: BannerProps) => {
  return (
    <div className="mb-4 rounded bg-amber-100 px-5 py-3 text-center text-yellow-800">
      {children}
    </div>
  );
};

export default async function HomePage({ params: { locale } }: LocaleParams) {
  const { t } = await i18nTranslation(locale);
  const latest = await getLatestMempoolPost(locale);

  return (
    <PageLayout t={t} locale={locale} generateHref={generateHref}>
      <div className="mb-8 rounded bg-gray-200 px-4 py-8 text-center">
        <Image
          className="mx-auto"
          src={cdnUrl("/img/blockchain.png")}
          width={480}
          height={240}
          alt="Blockchain"
          priority
        />
        <p className="mb-4 text-xl font-light italic">{t("satoshi_quote")}</p>
        <a
          className="inline-block cursor-pointer select-none rounded border border-solid border-green-600 bg-green-600 px-3 py-1 text-white hover:border-green-700 hover:bg-green-700 hover:text-white focus:border-green-700 focus:bg-green-700 focus:text-white"
          href={urls(locale).library.doc("bitcoin")}
          role="button"
        >
          {t("read_white_paper")}
        </a>
      </div>
      <p className="my-6 text-center text-3xl font-medium">
        <Trans
          i18nKey="newsletter_signup"
          components={{
            a: <Link href={urls(locale).substack} />,
          }}
        />
      </p>
      <Banner>
        <Trans
          t={t}
          i18nKey="rpow_banner"
          components={{
            a: <Link className="font-bold" href={urls(locale).finney.rpow} />,
          }}
        />
      </Banner>
      <Banner>
        <Trans
          t={t}
          i18nKey="skeptics_banner"
          components={{
            a: <Link className="font-bold" href={urls(locale).skeptics} />,
          }}
        />
      </Banner>
      <Banner>
        <Trans
          t={t}
          i18nKey="crash_course_banner"
          components={{
            a: <Link className="font-bold" href={urls(locale).crashCourse} />,
          }}
        />
      </Banner>
      <div className="mt-6 flex text-left flex-col sm:flex-row">
        {latest ? (
          <HomeSection
            title={t("mempool")}
            button={{
              text: "Read more",
              href: urls(locale).mempool.post(latest.slug),
            }}
          >
            <h3 className="italic">{latest.title}</h3>
            <p>{latest.excerpt}</p>
          </HomeSection>
        ) : null}
        <HomeSection
          title={t("podcast")}
          button={{
            text: t("see_episodes"),
            href: urls(locale).podcast.index,
          }}
        >
          <p>{t("podcast_description")}</p>
        </HomeSection>
        <HomeSection
          title={t("support")}
          button={{ text: t("donate"), href: urls(locale).donate.index }}
        >
          <p>{t("donation_message")}</p>
        </HomeSection>
      </div>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
