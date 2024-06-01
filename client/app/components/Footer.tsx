import { TFunction } from "i18next";
import Image from "next/image";
import Link from "next/link";
import { Trans } from "react-i18next/TransWithoutContext";

import { cdnUrl, urls } from "@/lib/urls";

type FooterProps = {
  t: TFunction<string, string>;
  locale: Locale;
};

export async function Footer({ t, locale }: FooterProps) {
  const links = [
    { label: t("about"), url: urls(locale).about },
    { label: t("contact"), url: urls(locale).contact },
    { label: t("donate"), url: urls(locale).donate.index },
    { label: t("get_involved"), url: urls(locale).getInvolved },
    { label: t("feed"), url: urls(locale).mempool.atom },
    { label: t("newsletter"), url: urls(locale).substack },
    { label: t("github"), url: urls(locale).github },
  ];

  return (
    <footer className="mt-auto border-t-1 border-dotted border-night px-3">
      <div className="twbs-container py-3 text-sm">
        <ul className="align-center my-3 flex flex-col justify-between gap-2 sm:flex-row sm:text-center">
          {links.map(({ label, url }) => (
            <li key={label}>
              <Link href={url}>{label}</Link>
            </li>
          ))}
        </ul>
        <div className="mt-4 flex flex-col text-gray-500 sm:flex-row sm:items-center">
          <Link
            className="my-auto flex-shrink-0"
            rel="license"
            href="http://creativecommons.org/licenses/by-sa/4.0/"
          >
            <Image
              alt="Creative Commons License"
              src={cdnUrl("/img/cc-4-0-by-sa.png")}
              width={88}
              height={31}
            />
          </Link>
          <span className="block sm:ml-4 sm:inline">
            <Trans
              t={t}
              i18nKey="sni_cc_license"
              components={{
                a: (
                  <Link
                    rel="license"
                    href="http://creativecommons.org/licenses/by-sa/4.0/"
                  />
                ),
              }}
            />
          </span>
        </div>
      </div>
    </footer>
  );
}
