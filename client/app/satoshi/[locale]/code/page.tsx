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
    title: t("code"),
    alternates: {
      canonical: generateHref(locale),
      languages,
    },
  };
}

export default async function SatoshiCode({
  params: { locale },
}: LocaleParams) {
  const { t } = await i18nTranslation(locale);

  return (
    <PageLayout t={t} locale={locale} generateHref={generateHref}>
      <PageHeader title={t("code")}>
        <p>
          <Trans
            t={t}
            i18nKey="version_control_description"
            components={{
              a: <Link href="https://github.com/bitcoin/bitcoin/" />,
            }}
          />
        </p>
      </PageHeader>
      <section>
        <CodeTable
          t={t}
          locale={locale}
          title={t("bitcoin_pre_release")}
          date={new Date(2008, 10, 16)}
          downloads={{
            release: {
              text: "bitcoin-nov08.tgz",
              href: "https://s3.amazonaws.com/nakamotoinstitute/code/bitcoin-nov08.tgz",
              note: t("compressed_by_sni"),
            },
            md5: { hash: "e9492e326512b55208c7d9f1db23e35a" },
            sha1: { hash: "466e67a3ce0f7e0ca3661e6fb5e72b874015b0b7" },
          }}
          source="https://bitcointalk.org/index.php?topic=382374.0"
        />
        <CodeTable
          t={t}
          locale={locale}
          title={t("bitcoin_v010")}
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
          t={t}
          locale={locale}
          title={t("bitcoin_v013")}
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
              note: t("calculated_by_sni"),
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
