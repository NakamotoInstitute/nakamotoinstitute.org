import { Metadata } from "next";
import Link from "next/link";
import { Trans } from "react-i18next/TransWithoutContext";

import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { cdnUrl, urls } from "@/lib/urls";

import { CodeTable } from "./components/CodeTable";

const generateHref = (l: Locale) => urls(l).satoshi.code;

export async function generateMetadata(props: LocaleParams): Promise<Metadata> {
  const params = await props.params;

  const { locale } = params;

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

export default async function SatoshiCode(props: LocaleParams) {
  const params = await props.params;

  const { locale } = params;

  const { t } = await i18nTranslation(locale);

  return (
    <PageLayout
      t={t}
      locale={locale}
      generateHref={generateHref}
      breadcrumbs={[
        { label: t("complete_satoshi"), href: urls(locale).satoshi.index },
        { label: t("code"), href: urls(locale).satoshi.code },
      ]}
    >
      <PageHeader title={t("code")}>
        <p>
          <Trans
            t={t}
            i18nKey="version_control_description"
            components={{
              a: (
                <Link
                  className="text-cardinal hover:underline"
                  href="https://github.com/bitcoin/bitcoin/"
                />
              ),
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
              href: cdnUrl("/code/bitcoin-nov08.tgz"),
              note: t("compressed_by_sni"),
            },
            md5: { hash: "7971fa6df9d192e295cf5160d5e181db" },
            sha1: { hash: "27778468cf9bd4d16a8fe12412518bb9fe4dfffe" },
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
                href: cdnUrl("/code/bitcoin-0.1.0.rar"),
              },
              md5: { hash: "91e2dfa2af043eabbb38964cbf368500" },
              sha1: { hash: "ec9ed4ccbc990eceb922ff0c4d71d1ad466990dd" },
            },
            {
              release: {
                text: "bitcoin-0.1.0.tgz",
                href: cdnUrl("/code/bitcoin-0.1.0.tgz"),
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
          date={new Date(2009, 0, 13)}
          dateRef="https://bitcointalk.org/index.php?topic=49815.msg593132#msg593132"
          downloads={{
            release: {
              text: "bitcoin-0.1.3.rar",
              href: cdnUrl("/code/bitcoin-0.1.3.rar"),
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
