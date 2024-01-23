import { cdnUrl, urls } from "@/lib/urls";
import Image from "next/image";
import Link from "next/link";

type FooterProps = {
  locale: Locale;
};

export function Footer({ locale }: FooterProps) {
  const links = [
    { label: "About", url: urls(locale).about },
    { label: "Contact", url: urls(locale).contact },
    { label: "Donate", url: urls(locale).donate },
    { label: "Feed", url: "#" },
    { label: "GitHub", url: urls(locale).github },
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
            Satoshi Nakamoto Institute is licensed under a{" "}
            <Link
              rel="license"
              href="http://creativecommons.org/licenses/by-sa/4.0/"
            >
              Creative Commons Attribution-ShareAlike 4.0 International License
            </Link>
            . Some works may be subject to other licenses.
          </span>
        </div>
      </div>
    </footer>
  );
}
