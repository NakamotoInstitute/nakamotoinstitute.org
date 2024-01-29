import Link from "next/link";

import { Markdown } from "@/app/components/Markdown";
import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { getPage } from "@/lib/content";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { getLocaleParams } from "@/lib/i18n/utils";
import { cdnUrl, urls } from "@/lib/urls";

type SatoshiSectionProps = {
  label: string;
  href: string;
  children: string;
};

const SatoshiSection = ({ label, href, children }: SatoshiSectionProps) => {
  return (
    <div>
      <Link href={href} className="text-xl font-medium">
        {label}
      </Link>
      <p>{children}</p>
    </div>
  );
};

export default async function SatoshiIndex({
  params: { locale },
}: LocaleParams) {
  const { t } = await i18nTranslation(locale);
  const content = await getPage("complete-satoshi", locale);
  const generateHref = (l: Locale) => urls(l).satoshi.index;

  return (
    <PageLayout
      className="text-center"
      locale={locale}
      generateHref={generateHref}
    >
      <PageHeader title={t("The Complete Satoshi")}>
        <Markdown>{content}</Markdown>
      </PageHeader>
      <section>
        <p>
          Read the original whitepaper,{" "}
          <Link href={urls(locale).library.doc("bitcoin")}>
            &ldquo;Bitcoin: A Peer-to-Peer Electronic Cash System.&rdquo;
          </Link>
        </p>
        <p>
          PDF available in{" "}
          <Link href={cdnUrl("/docs/bitcoin.pdf")}>English</Link>,{" "}
          <Link href={cdnUrl("/docs/bitcoin-zh-cn.pdf")}>
            Chinese (Simplified)
          </Link>
          ,{" "}
          <Link href={cdnUrl("/docs/bitcoin-zh-tw.pdf")}>
            Chinese (Traditional)
          </Link>
          , <Link href={cdnUrl("/docs/bitcoin-he.pdf")}>Hebrew</Link>,{" "}
          <Link href={cdnUrl("/docs/bitcoin-it.pdf")}>Italian</Link>,{" "}
          <Link href={cdnUrl("/docs/bitcoin-jp.pdf")}>Japanese</Link>,{" "}
          <Link href={cdnUrl("/docs/bitcoin-ru.pdf")}>Russian</Link>,{" "}
          <Link href={cdnUrl("/docs/bitcoin-es.pdf")}>Spanish</Link>, and{" "}
          <Link href={cdnUrl("/docs/bitcoin-vn.pdf")}>Vietnamese</Link>
        </p>
        <p>
          <Link href="/satoshinakamoto.asc">
            Satoshi Nakamoto&rsquo;s PGP Key
          </Link>
        </p>
      </section>
      <hr className="my-4" />
      <section className="mx-auto flex flex-col gap-4">
        <SatoshiSection label="Emails" href={urls(locale).satoshi.emails.index}>
          It all began here.
        </SatoshiSection>
        <SatoshiSection
          label="Forum Posts"
          href={urls(locale).satoshi.posts.index}
        >
          Where an idea flourished.
        </SatoshiSection>
        <SatoshiSection label="Code" href={urls(locale).satoshi.code}>
          The vision distilled.
        </SatoshiSection>
        <SatoshiSection label="Quotes" href={urls(locale).satoshi.quotesIndex}>
          Indexed wisdom from the quotable Satoshi.
        </SatoshiSection>
      </section>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
