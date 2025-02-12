import { TFunction } from "i18next";
import Image from "next/image";
import Link from "next/link";
import { Trans } from "react-i18next/TransWithoutContext";

import { cdnUrl, externalUrls, urls } from "@/lib/urls";

type FooterProps = {
  t: TFunction<string, string>;
  locale: Locale;
};

export async function Footer({ t, locale }: FooterProps) {
  const links = [
    { label: t("about"), url: urls(locale).about },
    { label: t("contact"), url: urls(locale).contact },
    { label: t("podcasts"), url: urls(locale).podcasts.index },
    { label: t("feed"), url: urls(locale).mempool.atom },
    { label: t("newsletter"), url: externalUrls.substack },
    { label: t("donate"), url: urls(locale).donate.index },
    { label: t("get_involved"), url: urls(locale).getInvolved },
    { label: t("github"), url: externalUrls.github },
    { label: t("x"), url: externalUrls.x },
    { label: t("nostr"), url: externalUrls.nostr },
  ];

  return (
    <footer className="mt-auto w-full border-t border-dashed border-dark">
      <div className="mx-auto max-w-screen-1.5xl px-4 py-8">
        <ul className="align-center flex flex-wrap justify-center gap-8 text-center">
          {links.map(({ label, url }) => (
            <li key={label}>
              <Link className="text-dark underline" href={url}>
                {label}
              </Link>
            </li>
          ))}
        </ul>
        <div className="my-10">
          <Image
            className="mx-auto"
            alt="SNI logo"
            src={cdnUrl("/img/xxi-rough.svg")}
            width={24}
            height={38}
          />
          <div className="mt-3 text-center uppercase">
            <p>{t("sni_full")}</p>
            <p>{t("establish_block")}</p>
            <p>{t("established_block_num")}</p>
          </div>
        </div>
        <div className="mx-auto flex max-w-md flex-col gap-2">
          <Link
            rel="license"
            href="http://creativecommons.org/licenses/by-sa/4.0/"
          >
            <Image
              className="mx-auto"
              alt="Creative Commons License"
              src={cdnUrl("/img/cc-by-sa.svg")}
              width={42}
              height={12}
            />
          </Link>
          <p className="text-center text-xs">
            <Trans
              t={t}
              i18nKey="sni_cc_license"
              components={{
                a: (
                  <Link
                    className="text-dark underline"
                    rel="license"
                    href="http://creativecommons.org/licenses/by-sa/4.0/"
                  />
                ),
              }}
            />
          </p>
        </div>
      </div>
    </footer>
  );
}
