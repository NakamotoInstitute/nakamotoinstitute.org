import Big from "big.js";
import { TFunction } from "i18next";
import Link from "next/link";

import { Rehype } from "@/app/components/Rehype";
import { Price, Skeptic } from "@/lib/api/schemas/skeptics";
import { cdnUrl } from "@/lib/urls";
import { formatDate } from "@/utils/dates";
import { calculateDCA } from "@/utils/prices";
import { commafy } from "@/utils/strings";

import { SkepticPriceData } from "./PriceData";

const DAILY_BUY = new Big(1);

type SkepticProps = {
  t: TFunction<string, string>;
  locale: Locale;
  skeptic: Skeptic;
  prices: Price[];
};

export async function SkepticListing({
  t,
  locale,
  skeptic,
  prices,
}: SkepticProps) {
  const priceData = calculateDCA(skeptic.date, prices, DAILY_BUY);

  return (
    <article
      id={skeptic.slug}
      className="border-t border-dashed border-taupe py-4 last:border-b"
    >
      <header>
        <p className="text-lg">
          {formatDate(locale, skeptic.date)} • $
          {commafy(priceData.originalUsd.toFixed(2))}
        </p>
        <Link href={{ hash: skeptic.slug }}>
          <h2 className="text-2xl font-semibold">{skeptic.name}</h2>
        </Link>
        <p className="small-caps">{skeptic.title}</p>
      </header>
      <section className="mb-2 py-2">
        <SkepticPriceData t={t} priceData={priceData} />
      </section>
      <section>
        {skeptic.excerpt ? (
          <div className="mb-4 italic italic-regular-em">
            <Rehype>{skeptic.excerpt}</Rehype>
          </div>
        ) : null}
        {skeptic.twitterScreenshot ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            className="mx-auto mb-4"
            src={cdnUrl(`/img/skeptics/${skeptic.slug}.jpg`)}
            alt=""
          />
        ) : null}
        {skeptic.mediaEmbed ? (
          <div
            className="mb-4 flex items-center justify-center"
            dangerouslySetInnerHTML={{ __html: skeptic.mediaEmbed }}
          />
        ) : null}
        {skeptic.waybackLink ? (
          <p className="text-sm small-caps">
            <Link href={skeptic.waybackLink}>{t("archive_link")}</Link>
          </p>
        ) : null}
      </section>
    </article>
  );
}
