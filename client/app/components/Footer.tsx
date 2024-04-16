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
    { label: t("About"), url: urls(locale).about },
    { label: t("Contact"), url: urls(locale).contact },
    { label: t("Donate"), url: urls(locale).donate.index },
    { label: t("Feed"), url: urls(locale).mempool.atom },
    { label: t("Newsletter"), url: urls(locale).substack },
    { label: t("GitHub"), url: urls(locale).github },
  ];

  return (
    <footer className="mt-auto bg-neutral-100 px-3">
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
              i18nKey="Satoshi Nakamoto Institute is licensed under a <a>Creative Commons Attribution-ShareAlike 4.0 International License</a>. Some works may be subject to other licenses."
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
