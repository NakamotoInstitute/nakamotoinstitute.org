import { Metadata } from "next";
import Link from "next/link";
import { Trans } from "react-i18next/TransWithoutContext";

import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";

import { CodeTable } from "./components/CodeTable";

const generateHref = (l: Locale) => urls(l).satoshi.code;

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs([...locales], generateHref);

  return {
    title: t("Code"),
    alternates: { languages },
  };
}

export default async function SatoshiCode({
  params: { locale },
}: LocaleParams) {
  const { t } = await i18nTranslation(locale);

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title={t("Code")}>
        <p>
          <Trans
            t={t}
            i18nKey="This page contains files for the first three available Bitcoin codebases written by Satoshi Nakamoto. Version control and releases from v0.1.5 onward can be viewed in the <a>Bitcoin GitHub repository</a>."
            components={{
              a: <Link href="https://github.com/bitcoin/bitcoin/" />,
            }}
          />
        </p>
      </PageHeader>
      <section>
        <CodeTable
          locale={locale}
          title={t("Bitcoin Pre-Release")}
          date={new Date(2008, 10, 16)}
          downloads={{
            release: {
              text: "bitcoin-nov08.tgz",
              href: "https://s3.amazonaws.com/nakamotoinstitute/code/bitcoin-nov08.tgz",
              note: t("(Compressed by SNI)"),
            },
            md5: { hash: "e9492e326512b55208c7d9f1db23e35a" },
            sha1: { hash: "466e67a3ce0f7e0ca3661e6fb5e72b874015b0b7" },
          }}
          source="https://bitcointalk.org/index.php?topic=382374.0"
        />
        <CodeTable
          locale={locale}
          title={t("Bitcoin v0.1.0")}
          date={new Date(2009, 0, 9)}
          downloads={[
            {
              release: {
                text: "bitcoin-0.1.0.rar",
                href: "https://s3.amazonaws.com/nakamotoinstitute/code/bitcoin-0.1.0.rar",
              },
              md5: { hash: "91e2dfa2af043eabbb38964cbf368500" },
              sha1: { hash: "ec9ed4ccbc990eceb922ff0c4d71d1ad466990dd" },
            },
            {
              release: {
                text: "bitcoin-0.1.0.tgz",
                href: "https://s3.amazonaws.com/nakamotoinstitute/code/bitcoin-0.1.0.tgz",
              },
              md5: { hash: "dca1095f053a0c2dc90b19c92bd1ec00" },
              sha1: { hash: "35f83eaa334e0e447ceea77a7cc955a4ccdd1a1d" },
            },
          ]}
          source="https://bitcointalk.org/index.php?topic=68121.0"
        />
        <CodeTable
          locale={locale}
          title={t("Bitcoin v0.1.3")}
          date={new Date(2008, 10, 16)}
          dateRef="https://bitcointalk.org/index.php?topic=49815.msg593132#msg593132"
          downloads={{
            release: {
              text: "bitcoin-0.1.3.rar",
              href: "https://s3.amazonaws.com/nakamotoinstitute/code/bitcoin-0.1.3.rar",
            },
            md5: { hash: "9a73e0826d5c069091600ca295c6d224" },
            sha1: {
              hash: "294c684fbaa13ae2662e612e98d288bde0ba2b88",
              note: t("(Calculated by SNI)"),
            },
          }}
          source="https://bitcointalk.org/index.php?topic=68121.msg814283#msg814283"
        />
      </section>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
